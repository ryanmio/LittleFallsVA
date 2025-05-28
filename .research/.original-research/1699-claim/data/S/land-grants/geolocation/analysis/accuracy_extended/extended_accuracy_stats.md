# Extended accuracy analysis

Includes 95% bootstrap CIs, overall CDF data, top outliers, and cost-accuracy trade-off.

## Mean error with 95% CI (per method)

| Method | n | Mean km | 95% CI |
|---|---|---|---|
| H-1 | 43 | 71.40 | [59.06, 85.35] |
| H-2 | 43 | 79.02 | [55.90, 110.05] |
| M-1 | 43 | 41.65 | [34.10, 50.13] |
| M-2 | 43 | 23.39 | [17.84, 29.96] |
| M-3 | 43 | 50.25 | [43.15, 57.96] |
| M-4 | 43 | 28.51 | [22.89, 35.28] |
| M-5 | 43 | 27.93 | [22.49, 34.10] |
| M-6 | 43 | 43.05 | [33.07, 53.84] |
| T-1 | 43 | 37.65 | [30.67, 45.15] |
| T-4 | 43 | 37.23 | [30.38, 44.47] |

## Top outliers overall

| Row index | Method | Model | Error km |
|---|---|---|---|
| 2 | H-2 | stanford-ner | 448.66 |
| 42 | H-2 | stanford-ner | 415.08 |
| 37 | M-6 | gpt-3.5-turbo | 176.33 |
| 25 | H-2 | stanford-ner | 174.42 |
| 36 | H-1 | human-gis | 170.95 |
| 3 | H-2 | stanford-ner | 166.38 |
| 8 | M-6 | gpt-3.5-turbo | 166.23 |
| 45 | H-1 | human-gis | 143.18 |
| 24 | H-1 | human-gis | 141.53 |
| 3 | H-1 | human-gis | 139.59 |

## Cost-accuracy trade-off by model

| Model | Mean error km | ≤10 km hit-rate | Cost per 1k located (USD) | Cost per +1% ≤10 km hit (USD) |
|---|---|---|---|---|
| o3-2025-04-16 | 23.39 | 30.2% | $127.46 | $4.22 |
| chatgpt-4o-latest | 27.93 | 16.3% | $1.05 | $0.06 |
| gpt-4.1-2025-04-14 | 32.87 | 18.6% | $3.49 | $0.19 |
| o4-mini-2025-04-16 | 39.65 | 10.5% | $10.69 | $1.02 |
| gpt-3.5-turbo | 43.05 | 4.7% | $0.10 | $0.02 |
| o3-mini-2025-01-31 | 50.25 | 4.7% | $14.15 | $3.04 |
| human-gis | 71.40 | 4.7% | $3,255.81 | $700.00 |
| stanford-ner | 79.02 | 7.0% | $0.00 | $0.00 |

*Full CDF data saved to* `analysis/accuracy_extended/cdf_overall.csv`. Pareto points for plotting saved to `analysis/accuracy_extended/pareto_points.csv`.