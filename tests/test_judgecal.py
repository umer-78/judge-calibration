import numpy as np

from judgecal.bench import family_effect, quantile_map
from judgecal.judge import judge_prompt, position_flip_rate
from judgecal.stats import isotonic, kappa, partial_spearman


def test_kappa_perfect_chance_and_offset():
    a = np.array([1, 2, 3, 4, 5] * 20)
    assert kappa(a, a) == 1.0
    rng = np.random.default_rng(0)
    assert abs(kappa(rng.integers(1, 6, 5000), rng.integers(1, 6, 5000))) < 0.05
    assert kappa(a, np.minimum(a + 1, 5)) < kappa(a, a)


def test_partial_correlation_removes_the_shared_cause():
    rng = np.random.default_rng(1)
    quality = rng.normal(size=4000)
    length = quality + rng.normal(size=4000)
    score = quality + 0.1 * rng.normal(size=4000)
    assert np.corrcoef(score, length)[0, 1] > 0.5
    assert abs(partial_spearman(score, length, quality)) < 0.1


def test_isotonic_is_monotone_and_quantile_map_matches_the_distribution():
    x = np.array([1, 1, 2, 2, 3, 3, 4, 4, 5, 5], float)
    y = np.array([2, 2, 1, 3, 4, 3, 5, 4, 5, 5], float)
    f = isotonic(x, y)
    assert np.all(np.diff(f(np.array([1, 2, 3, 4, 5], float))) >= 0)
    harsh = np.repeat([2, 3, 4], 100).astype(float)
    kind = harsh + 1
    assert np.allclose(quantile_map(harsh, kind)(harsh), kind)


def test_family_effect_finds_a_planted_preference():
    rng = np.random.default_rng(2)
    human = rng.integers(1, 6, 3000).astype(float)
    model = rng.choice(["gpt-4", "command-xlarge"], 3000)
    judge = human + 0.5 * (model == "gpt-4") + 0.1 * rng.normal(size=3000)
    assert abs(family_effect(judge, human, model, ("gpt-4",)) - 0.5) < 0.05


def test_judge_prompt_and_position_flips():
    prompt = judge_prompt("Say hi", "Hello!")
    assert "reasoning first" in prompt and "Helpfulness" in prompt and "5:" in prompt
    always_first = lambda instruction, first, second: "first"
    assert position_flip_rate([("q", "a", "b"), ("q", "c", "d")], always_first) == 1.0
    longer = lambda instruction, first, second: "first" if len(first) >= len(second) else "second"
    assert position_flip_rate([("q", "short", "much longer")], longer) == 0.0
