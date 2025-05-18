# Length-stratified accuracy (LLM methods only)
Length proxy = word-count of raw_entry (median = 36)

## Short abstracts (n = 48)
Overall mean error: **36.75 km**  (95 % CI 29.84–43.52)

| Method | n | Mean km |
|---|---|---|
| M-1 | 6 | 44.74 |
| M-2 | 6 | 29.64 |
| M-3 | 6 | 48.79 |
| M-4 | 6 | 27.44 |
| M-5 | 6 | 27.46 |
| M-6 | 6 | 36.90 |
| T-1 | 6 | 39.95 |
| T-4 | 6 | 39.08 |

## Long abstracts (n = 104)
Overall mean error: **34.93 km**  (95 % CI 30.45–39.75)

| Method | n | Mean km |
|---|---|---|
| M-1 | 13 | 44.78 |
| M-2 | 13 | 17.64 |
| M-3 | 13 | 52.60 |
| M-4 | 13 | 25.63 |
| M-5 | 13 | 23.74 |
| M-6 | 13 | 35.37 |
| T-1 | 13 | 38.32 |
| T-4 | 13 | 41.34 |

## Continuous length–error relationship
Across **152** LLM predictions, an OLS fit yields:

error_km = 42.28  +  -0.175 · length_words

Slope: **-0.175 km per word**  (95 % CI -0.601–0.308)

Pearson r = -0.061;  R² = 0.004

![Length vs Error](../figures/length_vs_error.png){#fig:length-vs-error width="80%"}
