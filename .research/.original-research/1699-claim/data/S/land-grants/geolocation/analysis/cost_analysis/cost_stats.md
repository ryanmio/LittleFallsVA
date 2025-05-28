# Cost analysis by method

Prices sourced from `analysis/pricing.yaml`. Costs include all entries (regardless of accuracy).

### Per-method breakdown

| Method | Underlying model | Entries | Located | Input tok | Output tok | Total cost (USD) | Cost per located grant | Cost per 1k located |
|---|---|---|---|---|---|---|---|---|
| H-1 | human-gis | 45 | 43 | 0 | 0 | $140.00 | $3.255814 | $3,255.81 |
| H-2 | stanford-ner | 45 | 43 | 0 | 0 | $0.00 | $0.000000 | $0.00 |
| M-1 | o4-mini-2025-04-16 | 45 | 43 | 6,653 | 124,901 | $0.56 | $0.012951 | $12.95 |
| M-2 | o3-2025-04-16 | 45 | 43 | 6,653 | 146,085 | $5.91 | $0.137440 | $137.44 |
| M-3 | o3-mini-2025-01-31 | 45 | 43 | 6,653 | 142,020 | $0.63 | $0.014702 | $14.70 |
| M-4 | gpt-4.1-2025-04-14 | 45 | 43 | 6,698 | 900 | $0.02 | $0.000479 | $0.48 |
| M-5 | chatgpt-4o-latest | 45 | 43 | 6,698 | 900 | $0.05 | $0.001093 | $1.09 |
| M-6 | gpt-3.5-turbo | 45 | 43 | 6,773 | 820 | $0.00 | $0.000107 | $0.11 |
| T-1 | o4-mini-2025-04-16 | 45 | 43 | 268,250 | 21,689 | $0.39 | $0.009082 | $9.08 |
| T-4 | gpt-4.1-2025-04-14 | 45 | 43 | 135,560 | 3,293 | $0.30 | $0.006918 | $6.92 |

### Roll-up: M vs T methods

| Category | Entries | Located | Total cost (USD) | Cost per located grant | Cost per 1k located |
|---|---|---|---|---|---|
| M-methods | 270 | 258 | $7.17 | $0.027795 | $27.80 |
| T-methods | 90 | 86 | $0.69 | $0.008000 | $8.00 |

### Roll-up: by model (all methods)

| Model | Entries | Located | Total cost (USD) | Cost per located grant | Cost per 1k located |
|---|---|---|---|---|---|
| chatgpt-4o-latest | 45 | 43 | $0.05 | $0.001093 | $1.09 |
| gpt-3.5-turbo | 45 | 43 | $0.00 | $0.000107 | $0.11 |
| gpt-4.1-2025-04-14 | 90 | 86 | $0.32 | $0.003698 | $3.70 |
| human-gis | 45 | 43 | $140.00 | $3.255814 | $3,255.81 |
| o3-2025-04-16 | 45 | 43 | $5.91 | $0.137440 | $137.44 |
| o3-mini-2025-01-31 | 45 | 43 | $0.63 | $0.014702 | $14.70 |
| o4-mini-2025-04-16 | 90 | 86 | $0.95 | $0.011016 | $11.02 |
| stanford-ner | 45 | 43 | $0.00 | $0.000000 | $0.00 |