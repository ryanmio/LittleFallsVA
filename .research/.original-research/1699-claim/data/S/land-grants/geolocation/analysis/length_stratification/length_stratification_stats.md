# Length-stratified accuracy (LLM methods only)
Length proxy = word-count of raw_entry (median = 36 words)

## Short abstracts (n = 198)
Overall mean error: **39.81 km**  (95 % CI 35.03–45.77)

| Method | n | Mean km |
|---|---|---|
| H-2 | 22 | 74.35 |
| M-1 | 22 | 37.37 |
| M-2 | 22 | 24.07 |
| M-3 | 22 | 51.50 |
| M-4 | 22 | 27.07 |
| M-5 | 22 | 25.89 |
| M-6 | 22 | 46.71 |
| T-1 | 22 | 36.07 |
| T-4 | 22 | 35.26 |

## Long abstracts (n = 189)
Overall mean error: **42.18 km**  (95 % CI 36.45–49.12)

| Method | n | Mean km |
|---|---|---|
| H-2 | 21 | 83.92 |
| M-1 | 21 | 46.13 |
| M-2 | 21 | 22.69 |
| M-3 | 21 | 48.94 |
| M-4 | 21 | 30.01 |
| M-5 | 21 | 30.08 |
| M-6 | 21 | 39.22 |
| T-1 | 21 | 39.31 |
| T-4 | 21 | 39.30 |

## Continuous length–error relationship
Across **387** LLM predictions, an OLS fit yields:

error_km = 35.28  +  0.146 · length_words

Slope: **0.146 km per word**  (95 % CI -0.111–0.450)

Pearson r = 0.051;  R² = 0.003

![Length vs Error](../figures/length_vs_error.png){#fig:length-vs-error width="80%"}
