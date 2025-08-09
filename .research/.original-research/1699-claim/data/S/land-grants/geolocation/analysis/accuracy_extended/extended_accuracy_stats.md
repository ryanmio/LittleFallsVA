# Extended accuracy analysis

Includes 95% bootstrap CIs, overall CDF data, top outliers, and cost-accuracy trade-off.

## Mean error with 95% CI (per method)

| Method | n | Mean km | 95% CI |
|---|---|---|---|
| E-1 | 43 | 19.24 | [13.83, 25.70] |
| E-2 | 43 | 20.57 | [14.85, 27.20] |
| H-1 | 43 | 71.40 | [57.44, 84.97] |
| H-2 | 43 | 79.02 | [56.05, 109.62] |
| H-3 | 43 | 94.28 | [68.67, 123.69] |
| H-4 | 43 | 80.33 | [64.75, 95.92] |
| M-1 | 43 | 41.65 | [33.66, 49.51] |
| M-2 | 43 | 23.39 | [17.88, 29.10] |
| M-3 | 43 | 50.25 | [42.86, 58.08] |
| M-4 | 43 | 28.51 | [22.69, 34.96] |
| M-5 | 43 | 27.93 | [22.67, 34.49] |
| M-6 | 43 | 43.05 | [33.73, 53.96] |
| T-1 | 43 | 37.65 | [30.68, 45.47] |
| T-4 | 43 | 37.23 | [29.94, 44.92] |

## Top outliers overall

| Row index | Method | Model | Error km |
|---|---|---|---|
| 2 | H-2 | stanford-ner | 448.66 |
| 42 | H-2 | stanford-ner | 415.08 |
| 25 | H-3 | M3_PP | 383.18 |
| 41 | H-3 | M3_PP | 375.33 |
| 4 | H-3 | M3_PP | 294.99 |
| 21 | H-3 | M3_PP | 244.45 |
| 37 | H-3 | M3_PP | 218.39 |
| 23 | H-4 | CC | 187.61 |
| 23 | H-3 | M3_PP | 187.61 |
| 37 | M-6 | gpt-3.5-turbo | 176.33 |

## Cost-accuracy trade-off by model

| Model | Mean error km | ≤10 km hit-rate | Cost per 1k located (USD) | Cost per +1% ≤10 km hit (USD) |
|---|---|---|---|---|
| o3-2025-04-16 | 21.07 | 31.8% | $174.38 | $5.49 |
| chatgpt-4o-latest | 27.93 | 16.3% | $1.05 | $0.06 |
| gpt-4.1-2025-04-14 | 32.87 | 18.6% | $3.49 | $0.19 |
| o4-mini-2025-04-16 | 39.65 | 10.5% | $10.69 | $1.02 |
| gpt-3.5-turbo | 43.05 | 4.7% | $0.10 | $0.02 |
| o3-mini-2025-01-31 | 50.25 | 4.7% | $14.15 | $3.04 |
| human-gis | 71.40 | 4.7% | $3,255.81 | $700.00 |
| stanford-ner | 79.02 | 7.0% | $0.00 | $0.00 |
| CC | 80.33 | 4.7% | $0.00 | $0.00 |
| M3_PP | 94.28 | 7.0% | $0.00 | $0.00 |

*Full CDF data saved to* `analysis/accuracy_extended/cdf_overall.csv`. Pareto points for plotting saved to `analysis/accuracy_extended/pareto_points.csv`.