"""The judge: a rubric with every score point defined, an LLM that reasons before it scores,
and a check for position bias in pairwise verdicts.

These call an OpenAI-compatible endpoint and are not measured in this repository (it runs
without API keys); the measurements use HELM's recorded GPT-4 judgments.
"""
import json
import urllib.request
from pathlib import Path

import yaml

RUBRIC = Path(__file__).with_name("rubric.yaml")


def chat(prompt, model, base_url, api_key, timeout=60):
    body = {"model": model, "temperature": 0, "response_format": {"type": "json_object"},
            "messages": [{"role": "user", "content": prompt}]}
    req = urllib.request.Request(base_url.rstrip("/") + "/chat/completions", json.dumps(body).encode(),
                                 {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(json.loads(r.read())["choices"][0]["message"]["content"])


def judge_prompt(instruction, output, rubric=None):
    rubric = rubric or yaml.safe_load(RUBRIC.read_text())
    lines = [f"{name}:\n" + "\n".join(f"  {k}: {v}" for k, v in sorted(points.items())) for name, points in rubric.items()]
    return ("Rate the response against each criterion. Write your reasoning first, then the scores.\n\n"
            + "\n".join(lines) + f"\n\nInstruction:\n{instruction}\n\nResponse:\n{output}\n\n"
            'Reply with JSON: {"reasoning": "...", "scores": {"Criterion": 1-5, ...}}')


def judge(instruction, output, **endpoint):
    return chat(judge_prompt(instruction, output), **endpoint)


def position_flip_rate(pairs, pick):
    """pairs: [(instruction, a, b)]; pick(instruction, first, second) returns "first" or "second".
    Asks each pair in both orders; the share of pairs whose winner changes with the order."""
    flips = 0
    for instruction, a, b in pairs:
        one = a if pick(instruction, a, b) == "first" else b
        two = b if pick(instruction, b, a) == "first" else a
        flips += one != two
    return flips / len(pairs)
