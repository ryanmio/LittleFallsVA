# Extended accuracy analysis

Includes 95% bootstrap CIs, overall CDF data, top outliers, and cost-accuracy trade-off.

## Mean error with 95% CI (per method)

| Method | n | Mean km | 95% CI |
|---|---|---|---|
| H-1 | 21 | 75.08 | [56.80, 93.84] |
| M-1 | 43 | 41.65 | [33.65, 50.04] |
| M-2 | 43 | 23.39 | [17.57, 29.54] |
| M-3 | 43 | 50.25 | [43.22, 57.86] |
| M-4 | 43 | 28.51 | [22.33, 34.79] |
| M-5 | 43 | 27.93 | [22.37, 34.23] |
| M-6 | 43 | 43.05 | [33.57, 54.72] |
| T-1 | 43 | 37.65 | [30.61, 45.32] |
| T-4 | 43 | 37.23 | [30.34, 44.24] |

## Top outliers overall

| Row index | Method | Model | Error km |
|---|---|---|---|
| 37 | M-6 | gpt-3.5-turbo | 176.33 |
| 8 | M-6 | gpt-3.5-turbo | 166.23 |
| 3 | H-1 | human-gis | 139.59 |
| 17 | H-1 | human-gis | 136.76 |
| 26 | M-3 | o3-mini-2025-01-31 | 123.04 |

## Cost-accuracy trade-off by model

| Model | Mean error km | ≤10 km hit-rate | Cost per 1k located (USD) | Cost per +1% ≤10 km hit (USD) |
|---|---|---|---|---|
| o3-2025-04-16 | 23.39 | 30.2% | $127.46 | $4.22 |
| chatgpt-4o-latest | 27.93 | 16.3% | $1.05 | $0.06 |
| gpt-4.1-2025-04-14 | 32.87 | 18.6% | $3.49 | $0.19 |
| o4-mini-2025-04-16 | 39.65 | 10.5% | $10.69 | $1.02 |
| gpt-3.5-turbo | 43.05 | 4.7% | $0.10 | $0.02 |
| o3-mini-2025-01-31 | 50.25 | 4.7% | $14.15 | $3.04 |
| human-gis | 75.08 | 4.8% | $6,666.67 | $1,400.00 |

*Full CDF data saved to* `analysis/accuracy_extended/cdf_overall.csv`. Pareto points for plotting saved to `analysis/accuracy_extended/pareto_points.csv`.