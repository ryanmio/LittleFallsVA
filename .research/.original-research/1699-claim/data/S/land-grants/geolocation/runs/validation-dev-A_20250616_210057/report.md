# Geolocation Experiment – Run Report

**Date:** 2025-06-16 22:09:55
**CLI command flags:** `--evalset=validation-dev-A.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --seed=123 --verbose`
**Evaluation set:** validation-dev-A.csv
**Dry-run:** No
**Rows evaluated:** 13
**Methods executed:** 2
**Runtime:** 4138.20 s
**Total tokens:** 135178
**Estimated token cost:** $4.7267
**Results CSV:** `results_validation-dev-A.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation-dev-A_20250616_210057`
**Rows in evaluation file:** 20
**Rows with ground truth evaluated:** 13 (filtered)

## Methods
| ID | Model | Pipeline | Params |
|---|---|---|---|
| o3_ensemble5_db05 | o3-2025-04-16 | one_shot | repeats=5, reasoning_effort=low, service_tier=flex, consensus_rule=dbscan, store=True |
| o3_ensemble5_ttc | o3-2025-04-16 | one_shot | repeats=5, reasoning_effort=low, service_tier=flex, consensus_rule=ttc, store=True |

## Prompts
| Pipeline | Prompt ID | Version |
|---|---|---|
| one_shot | one_shot_dms_v1 | v1 |
| tool_chain | tool_chain_v0 | v5 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| o3_ensemble5_db05 | 13 | 13.48 | 65765 | 2.2904 |
| o3_ensemble5_ttc | 13 | 14.35 | 69413 | 2.4363 |

## Accuracy Summary
Average Haversine error: **13.92 km**
High (<1 km): 3 Medium (1–10 km): 8 Low (>10 km): 15