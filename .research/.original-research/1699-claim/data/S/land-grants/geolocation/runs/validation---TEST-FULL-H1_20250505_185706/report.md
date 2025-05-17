# Geolocation Experiment – Run Report

**Date:** 2025-05-05 18:58:44
**CLI command flags:** `--evalset=validation - TEST-FULL-H1.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --seed=123 --max_rows=1`
**Evaluation set:** validation - TEST-FULL-H1.csv
**Dry-run:** No
**Rows evaluated:** 1
**Methods executed:** 10
**Runtime:** 97.98 s
**Total tokens:** 20151
**Estimated token cost:** $0.3435
**Results CSV:** `results_validation - TEST-FULL-H1.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation---TEST-FULL-H1_20250505_185706`
**Rows in evaluation file:** 125
**Rows with ground truth evaluated:** 1 (filtered)

## Methods
| ID | Model | Pipeline | Params |
|---|---|---|---|
| M-1 | o4-mini-2025-04-16 | one_shot | reasoning_effort=medium, service_tier=flex, store=True |
| M-2 | o3-2025-04-16 | one_shot | reasoning_effort=medium, service_tier=flex, store=True |
| M-3 | o3-mini-2025-01-31 | one_shot | reasoning_effort=medium, store=True |
| M-4 | gpt-4.1-2025-04-14 | one_shot | temperature=0.2, store=True |
| M-5 | chatgpt-4o-latest | one_shot | temperature=0.2, store=True |
| M-6 | gpt-3.5-turbo | one_shot | temperature=0.2, store=True |
| T-1 | o4-mini-2025-04-16 | tool_chain | reasoning_effort=low, service_tier=flex, store=True |
| T-3 | o3-mini-2025-01-31 | tool_chain | reasoning_effort=low, store=True |
| T-4 | gpt-4.1-2025-04-14 | tool_chain | temperature=0.2, store=True |
| H-1 | human-gis | static | fixed_cost_usd=140.0, billed_hours=6.0, store=True |

## Prompts
| Pipeline | Prompt ID | Version |
|---|---|---|
| one_shot | one_shot_dms_v1 | v1 |
| tool_chain | tool_chain_v0 | v5 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| M-1 | 1 | 3.45 | 1775 | 0.0073 |
| M-2 | 1 | 6.43 | 3631 | 0.1407 |
| M-3 | 1 | 43.81 | 3242 | 0.1252 |
| M-4 | 1 | 25.64 | 171 | 0.0005 |
| M-5 | 1 | 21.65 | 171 | 0.0011 |
| M-6 | 1 | 13.50 | 171 | 0.0001 |
| T-1 | 1 | 2.78 | 5803 | 0.0086 |
| T-3 | 1 | 7.98 | 4272 | 0.0582 |
| T-4 | 1 | 1.81 | 915 | 0.0019 |
| H-1 | 1 | 48.09 | 0 | 140.0000 |

## Accuracy Summary
Average Haversine error: **17.51 km**
High (<1 km): 0 Medium (1–10 km): 5 Low (>10 km): 5