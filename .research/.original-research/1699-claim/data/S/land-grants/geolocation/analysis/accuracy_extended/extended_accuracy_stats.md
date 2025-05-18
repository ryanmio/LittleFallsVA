# Extended accuracy analysis

Includes 95% bootstrap CIs, overall CDF data, top outliers, and cost-accuracy trade-off.

## Mean error with 95% CI (per method)

| Method | n | Mean km | 95% CI |
|---|---|---|---|
| H-1 | 43 | 71.40 | [57.94, 85.91] |
| M-1 | 43 | 41.65 | [34.02, 50.13] |
| M-2 | 43 | 23.39 | [17.80, 29.66] |
| M-3 | 43 | 50.25 | [42.73, 57.71] |
| M-4 | 43 | 28.51 | [22.88, 35.02] |
| M-5 | 43 | 27.93 | [22.20, 34.10] |
| M-6 | 43 | 43.05 | [32.97, 54.29] |
| T-1 | 43 | 37.65 | [30.88, 44.97] |
| T-4 | 43 | 37.23 | [29.91, 44.36] |

## Top outliers overall

| Row index | Method | Model | Error km |
|---|---|---|---|
| 37 | M-6 | gpt-3.5-turbo | 176.33 |
| 36 | H-1 | human-gis | 170.95 |
| 8 | M-6 | gpt-3.5-turbo | 166.23 |
| 45 | H-1 | human-gis | 143.18 |
| 24 | H-1 | human-gis | 141.53 |
| 3 | H-1 | human-gis | 139.59 |
| 17 | H-1 | human-gis | 136.76 |
| 32 | H-1 | human-gis | 128.88 |
| 26 | M-3 | o3-mini-2025-01-31 | 123.04 |
| 9 | H-1 | human-gis | 121.43 |

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

*Full CDF data saved to* `analysis/accuracy_extended/cdf_overall.csv`. Pareto points for plotting saved to `analysis/accuracy_extended/pareto_points.csv`.