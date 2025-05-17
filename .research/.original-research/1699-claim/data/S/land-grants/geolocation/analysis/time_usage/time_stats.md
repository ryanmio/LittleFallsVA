# Time/latency analysis by method

Source: `analysis/full_results.csv` – `latency_s` is wall-clock time from request to final answer and therefore includes model thinking + any tool latency. `H-1` cost converted to **9.33 h** ( $140 / $15 ).

### Per-method breakdown

| Method | Model | Entries | Located | Total hours | Hours per located | Hours/1k located |
|---|---|---|---|---|---|---|
| H-1 | human-gis | 45 | 44 | 9.330 | 0.2120 | 212.045 |
| M-1 | o4-mini-2025-04-16 | 45 | 43 | 0.413 | 0.0096 | 9.603 |
| M-2 | o3-2025-04-16 | 45 | 43 | 0.572 | 0.0133 | 13.294 |
| M-3 | o3-mini-2025-01-31 | 45 | 43 | 0.378 | 0.0088 | 8.791 |
| M-4 | gpt-4.1-2025-04-14 | 45 | 43 | 0.013 | 0.0003 | 0.310 |
| M-5 | chatgpt-4o-latest | 45 | 43 | 0.008 | 0.0002 | 0.184 |
| M-6 | gpt-3.5-turbo | 45 | 43 | 0.010 | 0.0002 | 0.232 |
| T-1 | o4-mini-2025-04-16 | 45 | 43 | 0.163 | 0.0038 | 3.792 |
| T-4 | gpt-4.1-2025-04-14 | 45 | 43 | 0.065 | 0.0015 | 1.519 |

### Roll-up: M vs T methods

| Category | Entries | Located | Total hours | Hours per located | Hours/1k located |
|---|---|---|---|---|---|
| M-methods | 270 | 258 | 1.394 | 0.0054 | 5.402 |
| T-methods | 90 | 86 | 0.228 | 0.0027 | 2.655 |

### Roll-up: by model

| Model | Entries | Located | Total hours | Hours per located | Hours/1k located |
|---|---|---|---|---|---|
| chatgpt-4o-latest | 45 | 43 | 0.008 | 0.0002 | 0.184 |
| gpt-3.5-turbo | 45 | 43 | 0.010 | 0.0002 | 0.232 |
| gpt-4.1-2025-04-14 | 90 | 86 | 0.079 | 0.0009 | 0.915 |
| human-gis | 45 | 44 | 9.330 | 0.2120 | 212.045 |
| o3-2025-04-16 | 45 | 43 | 0.572 | 0.0133 | 13.294 |
| o3-mini-2025-01-31 | 45 | 43 | 0.378 | 0.0088 | 8.791 |
| o4-mini-2025-04-16 | 90 | 86 | 0.576 | 0.0067 | 6.698 |