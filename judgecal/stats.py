"""Agreement and bias statistics for ordinal scores."""
import numpy as np
from scipy.stats import rankdata, spearmanr

GRID = 0.5    # human pools average several raters, so scores fall on half points


def kappa(a, b):
    """Quadratic-weighted Cohen's kappa on the half-point grid from 1 to 5."""
    a, b = (np.rint((np.asarray(x) - 1) / GRID).astype(int) for x in (a, b))
    k = int(4 / GRID) + 1
    observed = np.zeros((k, k))
    np.add.at(observed, (a, b), 1)
    observed /= observed.sum()
    expected = np.outer(observed.sum(1), observed.sum(0))
    i, j = np.indices((k, k))
    w = (i - j) ** 2 / (k - 1) ** 2
    return float(1 - (w * observed).sum() / (w * expected).sum())


def spearman(a, b):
    return float(spearmanr(a, b).statistic)


def partial_spearman(x, y, z):
    """Rank correlation of x and y once z is held fixed (on ranks, linearly)."""
    rx, ry, rz = (rankdata(v) for v in (x, y, z))
    design = np.column_stack([np.ones_like(rz), rz])
    resid = lambda v: v - design @ np.linalg.lstsq(design, v, rcond=None)[0]
    return float(np.corrcoef(resid(rx), resid(ry))[0, 1])


def isotonic(x, y):
    """Pool-adjacent-violators: the non-decreasing step function of x closest to y. Returns a predictor."""
    order = np.argsort(x, kind="stable")
    xs, ys = np.asarray(x, float)[order], np.asarray(y, float)[order]
    blocks = []                                    # [sum, count, max x]
    for xv, yv in zip(xs, ys):
        blocks.append([yv, 1, xv])
        while len(blocks) > 1 and blocks[-2][0] / blocks[-2][1] >= blocks[-1][0] / blocks[-1][1]:
            s, n, m = blocks.pop()
            blocks[-1][0] += s
            blocks[-1][1] += n
            blocks[-1][2] = m
    edges = np.array([b[2] for b in blocks])
    values = np.array([b[0] / b[1] for b in blocks])
    return lambda q: values[np.minimum(np.searchsorted(edges, q, side="left"), len(values) - 1)]


def bootstrap(fn, n, reps=2000, seed=0):
    """95% interval of fn(indices) over resamples of n items."""
    rng = np.random.default_rng(seed)
    vals = [fn(rng.integers(n, size=n)) for _ in range(reps)]
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))
