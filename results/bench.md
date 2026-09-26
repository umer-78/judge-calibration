1,399 outputs, each rated by the GPT-4 judge and both human pools.

## Agreement (quadratic-weighted kappa; Spearman in brackets)

| Criterion | Judge vs MTurk | Judge vs Scale | MTurk vs Scale (ceiling) | Mean score: judge / MTurk / Scale |
|---|---|---|---|---|
| Helpfulness | 0.43 (0.43) | 0.30 (0.30) | 0.41 (0.31) | 3.81 / 4.24 / 4.39 |
| Understandability | 0.38 (0.30) | 0.26 (0.24) | 0.31 (0.24) | 4.93 / 4.82 / 4.74 |
| Completeness | 0.61 (0.57) | 0.50 (0.50) | 0.48 (0.43) | 4.26 / 4.32 / 4.41 |
| Conciseness | 0.32 (0.32) | 0.28 (0.28) | 0.30 (0.26) | 3.68 / 4.45 / 4.26 |
| Harmlessness | 0.30 (0.28) | 0.29 (0.28) | 0.14 (0.14) | 4.98 / 4.98 / 4.96 |

## Biases

Length: partial rank correlation of score with output length, one human pool's score held fixed. Family effect: how much higher a rater scores GPT-family outputs than Cohere's at the same score from one human pool. Self-preference: the judge's family effect beyond the other human pool's.

| Criterion | Length: judge | Length: other human pool | Judge's family effect | Beyond the human pools' (self-preference) | 95% interval |
|---|---|---|---|---|---|
| Helpfulness | +0.10 | +0.19 | +0.33 | -0.06 | -0.14 to +0.03 |
| Understandability | +0.01 | -0.05 | +0.15 | +0.07 | +0.02 to +0.13 |
| Completeness | +0.37 | +0.22 | +0.82 | +0.38 | +0.27 to +0.49 |
| Conciseness | -0.23 | -0.35 | +0.33 | +0.26 | +0.17 to +0.35 |
| Harmlessness | -0.00 | -0.03 | +0.01 | +0.01 | -0.01 to +0.03 |

## Calibration (kappa against the human pool the mapping never saw; mean absolute error in brackets)

| Criterion | Raw judge | Quantile map | Isotonic | Isotonic + length + family |
|---|---|---|---|---|
| Helpfulness | 0.36 (0.74) | 0.44 (0.53) | 0.29 (0.64) | 0.35 (0.53) |
| Understandability | 0.32 (0.22) | 0.32 (0.22) | 0.18 (0.40) | 0.20 (0.31) |
| Completeness | 0.56 (0.56) | 0.56 (0.51) | 0.48 (0.61) | 0.49 (0.53) |
| Conciseness | 0.30 (0.89) | 0.35 (0.67) | 0.26 (0.68) | 0.32 (0.57) |
| Harmlessness | 0.30 (0.04) | 0.28 (0.03) | 0.27 (0.07) | 0.24 (0.05) |
