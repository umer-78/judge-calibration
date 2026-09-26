"""Recorded judgments from HELM Instruct (v1.0.0): model outputs to open-ended instructions,
each rated 1 to 5 on five criteria by GPT-4 acting as a judge and by two pools of human
raters (Amazon Mechanical Turk and Scale AI; each pool's score is its raters' mean).

Five scenarios (grammar, koala, open_assistant, self_instruct, vicuna) and three models
(Cohere Command, GPT-3.5 Turbo, GPT-4). Downloaded on first use into JUDGECAL_DATA
(default ~/.cache/judgecal).
"""
import json
import os
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

BUCKET = "https://storage.googleapis.com/crfm-helm-public/instruct/benchmark_output/runs/instruction_following"
LISTING = "https://storage.googleapis.com/storage/v1/b/crfm-helm-public/o"
SCENARIOS = ("grammar", "koala", "open_assistant", "self_instruct", "vicuna")
MODELS = {"cohere_command-xlarge-beta": "command-xlarge", "openai_gpt-3.5-turbo-0613": "gpt-3.5-turbo",
          "openai_gpt-4-0314": "gpt-4"}
RATERS = ("gpt4", "mturk", "scale")
CRITERIA = ("Helpfulness", "Understandability", "Completeness", "Conciseness", "Harmlessness")


def cache_dir():
    path = Path(os.environ.get("JUDGECAL_DATA", Path.home() / ".cache" / "judgecal"))
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_json(url, path, tries=4):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        for attempt in range(tries):
            try:
                with urllib.request.urlopen(url, timeout=120) as r:
                    body = r.read()
                break
            except OSError:
                if attempt == tries - 1:
                    raise
                time.sleep(2 ** attempt)
        path.write_bytes(body)
    return json.loads(path.read_text())


def runs():
    q = {"prefix": "instruct/benchmark_output/runs/instruction_following/", "delimiter": "/", "maxResults": 1000}
    page = get_json(f"{LISTING}?{urllib.parse.urlencode(q)}", cache_dir() / "listing.json")
    out = []
    for p in page.get("prefixes", []):
        run = p.rstrip("/").rsplit("/", 1)[1]
        args = dict(a.split("=", 1) for a in run.split(":", 1)[1].split(",") if "=" in a)
        if run.split(":")[0] in SCENARIOS and args.get("model") in MODELS and args.get("evaluator") in RATERS:
            out.append((run, run.split(":")[0], MODELS[args["model"]], args["evaluator"]))
    return out


def load():
    """[{"scenario", "model", "id", "prompt", "output", "words", "gpt4": {criterion: score}, "mturk": {...}, "scale": {...}}]
    for outputs every rater scored on every criterion."""
    def fetch(job):
        run = job[0]
        base, local = f"{BUCKET}/{urllib.parse.quote(run, safe='')}", cache_dir() / urllib.parse.quote(run, safe="")
        return job, get_json(f"{base}/display_predictions.json", local / "p.json"), get_json(f"{base}/instances.json", local / "i.json")

    rows = {}
    with ThreadPoolExecutor(8) as pool:
        for (run, scenario, model, rater), preds, instances in pool.map(fetch, runs()):
            text = {i["id"]: i["input"]["text"] for i in instances}
            for p in preds:
                if all(c in p["stats"] for c in CRITERIA):
                    r = rows.setdefault((scenario, model, p["instance_id"]), {
                        "scenario": scenario, "model": model, "id": p["instance_id"], "prompt": text.get(p["instance_id"], ""),
                        "output": p["predicted_text"], "words": len(p["predicted_text"].split())})
                    r[rater] = {c: float(p["stats"][c]) for c in CRITERIA}
    return [r for _, r in sorted(rows.items()) if all(k in r for k in RATERS)]
