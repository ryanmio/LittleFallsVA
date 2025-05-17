# Geolocation Experiment – Run Report

**Date:** 2025-04-29 16:00:52
**Evaluation set:** validation-dev-A.csv
**Dry-run:** Yes
**Rows evaluated:** 13
**Methods executed:** 11
**Runtime:** 205.42 s
**Total tokens:** 0
**Estimated cost:** $0.0000
**Results CSV:** `results_validation-dev-A.csv`

## Methods
| ID | Model | Pipeline | Params |
|---|---|---|---|
| M-1 | o4-mini-2025-04-16 | one_shot | reasoning_effort=medium, store=True, tools=[] |
| M-2 | o3-2025-04-16 | one_shot | reasoning_effort=medium, store=True, tools=[] |
| M-3 | o3-mini-2025-01-31 | one_shot | reasoning_effort=medium, store=True, tools=[] |
| M-4 | gpt-4.1-2025-04-14 | one_shot | temperature=0.2, store=True, tools=[] |
| M-5 | chatgpt-4o-latest | one_shot | temperature=0.2, store=True, tools=[] |
| M-6 | gpt-3.5-turbo | one_shot | temperature=0.2, store=True, tools=[] |
| T-1 | o4-mini-2025-04-16 | tool_chain | reasoning_effort=medium, store=True, tools=[] |
| T-2 | o3-2025-04-16 | tool_chain | reasoning_effort=medium, store=True, tools=[] |
| T-3 | o3-mini-2025-01-31 | tool_chain | reasoning_effort=medium, store=True, tools=[] |
| T-4 | gpt-4.1-2025-04-14 | tool_chain | temperature=0.2, store=True, tools=[] |
| T-5 | chatgpt-4o-latest | tool_chain | temperature=0.2, store=True, tools=[] |

## Prompts
| Pipeline | Prompt ID | Version |
|---|---|---|
| one_shot | one_shot_dms_v1 | v1 |
| tool_chain | tool_chain_v0 | v0 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| M-1 | 13 | 6856.17 | 4056 | 0.0000 |
| M-2 | 13 | 6854.10 | 2860 | 0.0000 |
| M-3 | 13 | 6855.08 | 3536 | 0.0000 |
| M-4 | 13 | 6853.85 | 2886 | 0.0000 |
| M-5 | 13 | 6854.15 | 2912 | 0.0000 |
| M-6 | 13 | 6854.67 | 3146 | 0.0000 |
| T-1 | 13 | — | 4758 | 0.0000 |
| T-2 | 13 | — | 4966 | 0.0000 |
| T-3 | 13 | — | 5434 | 0.0000 |
| T-4 | 13 | — | 5772 | 0.0000 |
| T-5 | 13 | — | 5876 | 0.0000 |

## Accuracy Summary
Average Haversine error: **6854.67 km**
High (<1 km): 0 Medium (1–10 km): 0 Low (>10 km): 78