# Time/latency analysis by method

Source: `analysis/full_results.csv` – `latency_s` is wall-clock time from request to final answer and therefore includes model thinking + any tool latency. `H-1` cost converted to **9.33 h** ( $140 / $15 ).

### Per-method breakdown

| Method | Model | Entries | Located | Total hours | Hours per located | Hours/1k located |
|---|---|---|---|---|---|---|
| E-1 | o3-2025-04-16 | 43 | 43 | 0.551 | 0.0128 | 12.819 |
| E-2 | o3-2025-04-16 | 43 | 43 | 0.552 | 0.0128 | 12.838 |
| H-1 | human-gis | 43 | 43 | 9.330 | 0.2170 | 216.977 |
| H-2 | stanford-ner | 43 | 43 | 0.000 | 0.0000 | 0.000 |
| H-3 | M3_PP | 43 | 43 | 0.000 | 0.0000 | 0.000 |
| H-4 | CC | 43 | 43 | 0.000 | 0.0000 | 0.000 |
| M-1 | o4-mini-2025-04-16 | 43 | 43 | 0.393 | 0.0091 | 9.145 |
| M-2 | o3-2025-04-16 | 43 | 43 | 0.519 | 0.0121 | 12.060 |
| M-3 | o3-mini-2025-01-31 | 43 | 43 | 0.366 | 0.0085 | 8.523 |
| M-4 | gpt-4.1-2025-04-14 | 43 | 43 | 0.013 | 0.0003 | 0.295 |
| M-5 | chatgpt-4o-latest | 43 | 43 | 0.008 | 0.0002 | 0.178 |
| M-6 | gpt-3.5-turbo | 43 | 43 | 0.010 | 0.0002 | 0.225 |
| T-1 | o4-mini-2025-04-16 | 43 | 43 | 0.159 | 0.0037 | 3.704 |
| T-4 | gpt-4.1-2025-04-14 | 43 | 43 | 0.054 | 0.0013 | 1.255 |

### Roll-up: M vs T methods

| Category | Entries | Located | Total hours | Hours per located | Hours/1k located |
|---|---|---|---|---|---|
| M-methods | 258 | 258 | 1.308 | 0.0051 | 5.071 |
| T-methods | 86 | 86 | 0.213 | 0.0025 | 2.479 |

### Roll-up: by model

| Model | Entries | Located | Total hours | Hours per located | Hours/1k located |
|---|---|---|---|---|---|
| CC | 43 | 43 | 0.000 | 0.0000 | 0.000 |
| M3_PP | 43 | 43 | 0.000 | 0.0000 | 0.000 |
| chatgpt-4o-latest | 43 | 43 | 0.008 | 0.0002 | 0.178 |
| gpt-3.5-turbo | 43 | 43 | 0.010 | 0.0002 | 0.225 |
| gpt-4.1-2025-04-14 | 86 | 86 | 0.067 | 0.0008 | 0.775 |
| human-gis | 43 | 43 | 9.330 | 0.2170 | 216.977 |
| o3-2025-04-16 | 129 | 129 | 1.622 | 0.0126 | 12.572 |
| o3-mini-2025-01-31 | 43 | 43 | 0.366 | 0.0085 | 8.523 |
| o4-mini-2025-04-16 | 86 | 86 | 0.552 | 0.0064 | 6.424 |
| stanford-ner | 43 | 43 | 0.000 | 0.0000 | 0.000 |