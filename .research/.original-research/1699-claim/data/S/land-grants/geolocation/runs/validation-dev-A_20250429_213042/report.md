# Geolocation Experiment – Run Report

**Date:** 2025-04-29 21:31:30
**CLI command flags:** `--evalset=validation-dev-A.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --seed=123 --verbose --max_rows=1`
**Evaluation set:** validation-dev-A.csv
**Dry-run:** No
**Rows evaluated:** 1
**Methods executed:** 5
**Runtime:** 47.38 s
**Total tokens:** 4683
**Estimated cost:** $0.1219
**Results CSV:** `results_validation-dev-A.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation-dev-A_20250429_213042`
**Rows in evaluation file:** 20
**Rows with ground truth evaluated:** 1 (filtered)

## Methods
| ID | Model | Pipeline | Params |
|---|---|---|---|
| M-3 | o3-mini-2025-01-31 | one_shot | reasoning_effort=medium, store=True |
| M-4 | gpt-4.1-2025-04-14 | one_shot | temperature=0.2, store=True |
| M-5 | chatgpt-4o-latest | one_shot | temperature=0.2, store=True |
| M-6 | gpt-3.5-turbo | one_shot | temperature=0.2, store=True, max_output_tokens=60 |
| T-4 | gpt-4.1-2025-04-14 | tool_chain | temperature=0.2, store=True |

## Prompts
| Pipeline | Prompt ID | Version |
|---|---|---|
| one_shot | one_shot_dms_v1 | v1 |
| tool_chain | tool_chain_v0 | v1 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| M-3 | 1 | 16.41 | 3075 | 0.1178 |
| M-4 | 1 | 13.31 | 196 | 0.0005 |
| M-5 | 1 | 9.74 | 196 | 0.0012 |
| M-6 | 1 | — | 216 | 0.0001 |
| T-4 | 1 | 1.23 | 1000 | 0.0023 |

## Accuracy Summary
Average Haversine error: **10.17 km**
High (<1 km): 0 Medium (1–10 km): 2 Low (>10 km): 2