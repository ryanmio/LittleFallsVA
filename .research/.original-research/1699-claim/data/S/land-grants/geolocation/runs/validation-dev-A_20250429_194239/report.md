# Geolocation Experiment – Run Report

**Date:** 2025-04-29 19:42:52
**CLI command flags:** `--evalset=validation-dev-A.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --dry_run --seed=123 --max_rows=1`
**Evaluation set:** validation-dev-A.csv
**Dry-run:** Yes
**Rows evaluated:** 1
**Methods executed:** 11
**Runtime:** 13.21 s
**Total tokens:** 0
**Estimated cost:** $0.0000
**Results CSV:** `results_validation-dev-A.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation-dev-A_20250429_194239`
**Rows in evaluation file:** 20
**Rows with ground truth evaluated:** 1 (filtered)

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
| tool_chain | tool_chain_v0 | v1 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| M-1 | 1 | 6824.40 | 280 | 0.0000 |
| M-2 | 1 | 6822.44 | 196 | 0.0000 |
| M-3 | 1 | 6823.17 | 230 | 0.0000 |
| M-4 | 1 | 6824.05 | 254 | 0.0000 |
| M-5 | 1 | 6822.41 | 194 | 0.0000 |
| M-6 | 1 | 6822.71 | 216 | 0.0000 |
| T-1 | 1 | — | 404 | 0.0000 |
| T-2 | 1 | — | 354 | 0.0000 |
| T-3 | 1 | — | 386 | 0.0000 |
| T-4 | 1 | — | 360 | 0.0000 |
| T-5 | 1 | — | 394 | 0.0000 |

## Accuracy Summary
Average Haversine error: **6823.20 km**
High (<1 km): 0 Medium (1–10 km): 0 Low (>10 km): 6