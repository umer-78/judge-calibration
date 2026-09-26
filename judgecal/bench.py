"""Measuring the GPT-4 judge against human raters on HELM Instruct.

Agreement: quadratic-weighted kappa and Spearman, judge against each human pool, next to the
two human pools against each other, the ceiling a judge can be expected to reach.

Biases, with the three models' outputs rated by all three raters:
- length: does the score rise with the output's length once a human pool's score is held
  fixed? Asked of the judge and of the other human pool given the same control;
- self-preference: does the GPT-4 judge rate outputs from its own family (GPT-4, GPT-3.5)
  above a competitor's (Cohere) at the same score from one human pool, by more than the other
  human pool does? Subtracting the second pool matters: human scores are noisy, so at the same
  observed score the better model's outputs are genuinely better, and any rater, human or
  not, rates them higher.
- position: needs pairwise verdicts in both orders; this data is pointwise, so it is not
  measured here (judge.position_flip_rate runs it against a live judge).

Calibration, cross-fitted over five folds: the judge's scores are mapped onto one human
pool's scale (quantile matching; isotonic regression; isotonic plus a linear correction for
length and model family) and measured against the other pool, which the mapping never saw.
"""
import json
from pathlib import Path

import numpy as np

from . import data
from .stats import bootstrap, isotonic, kappa, partial_spearman, spearman

RESULTS = Path(__file__).resolve().parent.parent / "results"
OWN_FAMILY = ("gpt-3.5-turbo", "gpt-4")


def scores(rows, rater, criterion):
    return np.array([r[rater][criterion] for r in rows])


def agreement(rows, c):
    j, m, s = (scores(rows, k, c) for k in data.RATERS)
    return {"kappa": {"judge_mturk": kappa(j, m), "judge_scale": kappa(j, s), "mturk_scale": kappa(m, s)},
            "spearman": {"judge_mturk": spearman(j, m), "judge_scale": spearman(j, s), "mturk_scale": spearman(m, s)},
            "mean": {"judge": float(j.mean()), "mturk": float(m.mean()), "scale": float(s.mean())}}


def length_bias(rows, c):
    j, m, s = (scores(rows, k, c) for k in data.RATERS)
    w = np.array([r["words"] for r in rows])
    return {"judge": float(np.mean([partial_spearman(j, w, m), partial_spearman(j, w, s)])),
            "humans": float(np.mean([partial_spearman(s, w, m), partial_spearman(m, w, s)]))}


def family_effect(j, human, model, own):
    """How much higher the judge rates own-family outputs than the competitor's at the same human score."""
    x = np.column_stack([np.ones_like(human), human, np.isin(model, own)])
    return float(np.linalg.lstsq(x, j, rcond=None)[0][2])


def self_preference(rows, c):
    j, m, s = (scores(rows, k, c) for k in data.RATERS)
    model = np.array([r["model"] for r in rows])

    def excess(i):     # the judge's family effect minus the other human pool's, each pool taking a turn as the control
        return np.mean([family_effect(j[i], m[i], model[i], OWN_FAMILY) - family_effect(s[i], m[i], model[i], OWN_FAMILY),
                        family_effect(j[i], s[i], model[i], OWN_FAMILY) - family_effect(m[i], s[i], model[i], OWN_FAMILY)])
    everyone = np.arange(len(rows))
    lo, hi = bootstrap(excess, len(rows), reps=1000)
    judge_only = np.mean([family_effect(j, m, model, OWN_FAMILY), family_effect(j, s, model, OWN_FAMILY)])
    return {"effect": float(excess(everyone)), "interval": [lo, hi], "judge_family_effect": float(judge_only)}


def calibration(rows, c, folds=5, seed=0):
    j = scores(rows, "gpt4", c)
    words = np.log1p([r["words"] for r in rows])
    own = np.isin([r["model"] for r in rows], OWN_FAMILY).astype(float)
    fold = np.random.default_rng(seed).permutation(len(rows)) % folds
    out = {"raw": [], "quantile": [], "isotonic": [], "isotonic+length+family": []}
    mae = {k: [] for k in out}
    for fit_pool, eval_pool in (("mturk", "scale"), ("scale", "mturk")):
        target, truth = scores(rows, fit_pool, c), scores(rows, eval_pool, c)
        pred = {k: np.zeros(len(rows)) for k in out}
        for f in range(folds):
            tr, te = fold != f, fold == f
            iso = isotonic(j[tr], target[tr])
            pred["raw"][te] = j[te]
            pred["quantile"][te] = quantile_map(j[tr], target[tr])(j[te])
            pred["isotonic"][te] = iso(j[te])
            x = lambda idx: np.column_stack([np.ones(idx.sum()), iso(j[idx]), words[idx], own[idx]])
            beta = np.linalg.lstsq(x(tr), target[tr], rcond=None)[0]
            pred["isotonic+length+family"][te] = np.clip(x(te) @ beta, 1, 5)
        for k in out:
            out[k].append(kappa(pred[k], truth))
            mae[k].append(float(np.abs(pred[k] - truth).mean()))
    return {k: {"kappa": float(np.mean(out[k])), "mae": float(np.mean(mae[k]))} for k in out}


def quantile_map(judge, human):
    """Each judge score to the human score at the same quantile (the middle of its share), so the
    judge's scores take on the human pool's distribution without losing their order."""
    levels = np.unique(judge)
    cdf = np.array([(judge <= v).mean() for v in levels])
    mid = cdf - np.diff(np.concatenate([[0], cdf])) / 2
    table = dict(zip(levels, np.quantile(human, mid)))
    return lambda q: np.array([table.get(v, v) for v in q])


def disagreements(rows, c="Helpfulness", n=20):
    gap = scores(rows, "gpt4", c) - (scores(rows, "mturk", c) + scores(rows, "scale", c)) / 2
    lines = [f"# The {n} largest judge-human disagreements on {c}", ""]
    for i in np.argsort(-np.abs(gap))[:n]:
        r = rows[i]
        lines += [f"## {r['scenario']} / {r['model']} / {r['id']}: judge {r['gpt4'][c]:g}, "
                  f"MTurk {r['mturk'][c]:g}, Scale {r['scale'][c]:g}", "",
                  "**Instruction:** " + r["prompt"][:500].replace("\n", " "), "",
                  "**Output:** " + r["output"][:700].replace("\n", " "), ""]
    return "\n".join(lines)


def bench():
    rows = data.load()
    result = {"outputs": len(rows), "criteria": {}}
    lines = [f"{len(rows):,} outputs, each rated by the GPT-4 judge and both human pools.", "",
             "## Agreement (quadratic-weighted kappa; Spearman in brackets)", "",
             "| Criterion | Judge vs MTurk | Judge vs Scale | MTurk vs Scale (ceiling) | Mean score: judge / MTurk / Scale |",
             "|---|---|---|---|---|"]
    for c in data.CRITERIA:
        a, lb, sp, cal = agreement(rows, c), length_bias(rows, c), self_preference(rows, c), calibration(rows, c)
        result["criteria"][c] = {"agreement": a, "length_bias": lb, "self_preference": sp, "calibration": cal}
        k, s, mu = a["kappa"], a["spearman"], a["mean"]
        lines.append(f"| {c} | {k['judge_mturk']:.2f} ({s['judge_mturk']:.2f}) | {k['judge_scale']:.2f} ({s['judge_scale']:.2f}) | "
                     f"{k['mturk_scale']:.2f} ({s['mturk_scale']:.2f}) | {mu['judge']:.2f} / {mu['mturk']:.2f} / {mu['scale']:.2f} |")
    crit = result["criteria"]
    lines += ["", "## Biases", "",
              "Length: partial rank correlation of score with output length, one human pool's score held fixed. "
              "Family effect: how much higher a rater scores GPT-family outputs than Cohere's at the same score from one human pool. "
              "Self-preference: the judge's family effect beyond the other human pool's.", "",
              "| Criterion | Length: judge | Length: other human pool | Judge's family effect | Beyond the human pools' (self-preference) | 95% interval |",
              "|---|---|---|---|---|---|"]
    lines += [f"| {c} | {crit[c]['length_bias']['judge']:+.2f} | {crit[c]['length_bias']['humans']:+.2f} | "
              f"{crit[c]['self_preference']['judge_family_effect']:+.2f} | {crit[c]['self_preference']['effect']:+.2f} | "
              f"{crit[c]['self_preference']['interval'][0]:+.2f} to "
              f"{crit[c]['self_preference']['interval'][1]:+.2f} |" for c in data.CRITERIA]
    lines += ["", "## Calibration (kappa against the human pool the mapping never saw; mean absolute error in brackets)", "",
              "| Criterion | Raw judge | Quantile map | Isotonic | Isotonic + length + family |", "|---|---|---|---|---|"]
    lines += [f"| {c} | " + " | ".join(f"{crit[c]['calibration'][k]['kappa']:.2f} ({crit[c]['calibration'][k]['mae']:.2f})"
                                        for k in ("raw", "quantile", "isotonic", "isotonic+length+family")) + " |" for c in data.CRITERIA]
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "bench.md").write_text("\n".join(lines) + "\n")
    (RESULTS / "summary.json").write_text(json.dumps(result, indent=1))
    (RESULTS / "disagreements.md").write_text(disagreements(rows) + "\n")
    return "\n".join(lines)
