# Geolocation Experiment – Run Report

**Date:** 2025-06-16 20:57:23
**CLI command flags:** `--evalset=validation-dev-A.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --dry_run --seed=123 --max_rows=1`
**Evaluation set:** validation-dev-A.csv
**Dry-run:** Yes
**Rows evaluated:** 1
**Methods executed:** 2
**Runtime:** 12.01 s
**Total tokens:** 0
**Estimated token cost:** $0.0000
**Results CSV:** `results_validation-dev-A.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation-dev-A_20250616_205711`
**Rows in evaluation file:** 20
**Rows with ground truth evaluated:** 1 (filtered)

## Methods
| ID | Model | Pipeline | Params |
|---|---|---|---|
| o3_ensemble5_db05 | o3-2025-04-16 | one_shot | repeats=5, reasoning_effort=medium, service_tier=flex, consensus_rule=dbscan, store=True |
| o3_ensemble5_ttc | o3-2025-04-16 | one_shot | repeats=5, reasoning_effort=medium, service_tier=flex, consensus_rule=ttc, store=True |

## Prompts
| Pipeline | Prompt ID | Version |
|---|---|---|
| one_shot | one_shot_dms_v1 | v1 |
| tool_chain | tool_chain_v0 | v5 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| o3_ensemble5_db05 | 1 | 6832.78 | 1130 | 0.0000 |
| o3_ensemble5_ttc | 1 | 6828.58 | 1210 | 0.0000 |

## Accuracy Summary
Average Haversine error: **6830.68 km**
High (<1 km): 0 Medium (1–10 km): 0 Low (>10 km): 2