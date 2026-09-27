"""python -m judgecal.demo   write the live demo's data (docs/data.json): results/summary.json, plus per
criterion how the judge's scores line up with each human pool's (counts) and each model's mean score
from every rater. No prompts or outputs."""
import json
from collections import Counter
from pathlib import Path

from . import data

ROOT = Path(__file__).resolve().parent.parent


def build(out=ROOT / "docs"):
    summary = json.loads((ROOT / "results" / "summary.json").read_text())
    rows = data.load()
    models = sorted({r["model"] for r in rows})
    detail = {}
    for c in data.CRITERIA:
        grids = {pool: Counter((r["gpt4"][c], r[pool][c]) for r in rows) for pool in ("mturk", "scale")}
        detail[c] = {"grid": {pool: [[j, h, n] for (j, h), n in sorted(g.items())] for pool, g in grids.items()},
                     "models": {m: {k: round(sum(r[k][c] for r in rows if r["model"] == m) / sum(r["model"] == m for r in rows), 3)
                                    for k in data.RATERS} for m in models}}
    counts = Counter(r["model"] for r in rows)
    out.mkdir(exist_ok=True)
    (out / "data.json").write_text(json.dumps({"summary": summary, "detail": detail, "outputs_per_model": counts}, indent=1))
    print(f"wrote {out / 'data.json'}: {len(rows)} outputs")


if __name__ == "__main__":
    build()
