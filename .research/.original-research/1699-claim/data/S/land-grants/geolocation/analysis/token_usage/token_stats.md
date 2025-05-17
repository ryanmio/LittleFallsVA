# Token usage analysis by method

Source: `analysis/full_results.csv`

### Per-method breakdown

| Method | Model | Entries | Located | Input tok | Output tok | Reasoning tok | Tokens per located | Tokens/1k located |
|---|---|---|---|---|---|---|---|---|
| H-1 | human-gis | 45 | 44 | 0 | 0 | 0 | 0.00 | 0 |
| M-1 | o4-mini-2025-04-16 | 45 | 43 | 6,653 | 124,901 | 123,776 | 5,937.91 | 5,937,907 |
| M-2 | o3-2025-04-16 | 45 | 43 | 6,653 | 146,085 | 144,960 | 6,923.21 | 6,923,209 |
| M-3 | o3-mini-2025-01-31 | 45 | 43 | 6,653 | 142,020 | 141,120 | 6,739.37 | 6,739,372 |
| M-4 | gpt-4.1-2025-04-14 | 45 | 43 | 6,698 | 900 | 0 | 176.70 | 176,698 |
| M-5 | chatgpt-4o-latest | 45 | 43 | 6,698 | 900 | 0 | 176.70 | 176,698 |
| M-6 | gpt-3.5-turbo | 45 | 43 | 6,773 | 820 | 0 | 176.58 | 176,581 |
| T-1 | o4-mini-2025-04-16 | 45 | 43 | 268,250 | 21,689 | 0 | 6,742.77 | 6,742,767 |
| T-4 | gpt-4.1-2025-04-14 | 45 | 43 | 135,560 | 3,293 | 0 | 3,229.14 | 3,229,140 |

### Roll-up: M vs T methods

| Category | Entries | Located | Input tok | Output tok | Reasoning tok | Tokens per located | Tokens/1k located |
|---|---|---|---|---|---|---|---|
| M-methods | 270 | 258 | 40,128 | 415,626 | 409,856 | 3,355.08 | 3,355,078 |
| T-methods | 90 | 86 | 403,810 | 24,982 | 0 | 4,985.95 | 4,985,953 |

### Roll-up: by model

| Model | Entries | Located | Input tok | Output tok | Reasoning tok | Tokens per located | Tokens/1k located |
|---|---|---|---|---|---|---|---|
| chatgpt-4o-latest | 45 | 43 | 6,698 | 900 | 0 | 176.70 | 176,698 |
| gpt-3.5-turbo | 45 | 43 | 6,773 | 820 | 0 | 176.58 | 176,581 |
| gpt-4.1-2025-04-14 | 90 | 86 | 142,258 | 4,193 | 0 | 1,702.92 | 1,702,919 |
| human-gis | 45 | 44 | 0 | 0 | 0 | 0.00 | 0 |
| o3-2025-04-16 | 45 | 43 | 6,653 | 146,085 | 144,960 | 6,923.21 | 6,923,209 |
| o3-mini-2025-01-31 | 45 | 43 | 6,653 | 142,020 | 141,120 | 6,739.37 | 6,739,372 |
| o4-mini-2025-04-16 | 90 | 86 | 274,903 | 146,590 | 123,776 | 6,340.34 | 6,340,337 |