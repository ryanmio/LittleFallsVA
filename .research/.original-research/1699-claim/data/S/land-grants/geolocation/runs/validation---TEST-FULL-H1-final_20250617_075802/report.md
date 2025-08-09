# Geolocation Experiment – Run Report

**Date:** 2025-06-17 08:45:22
**CLI command flags:** `--evalset=validation - TEST-FULL-H1-final.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --seed=123`
**Evaluation set:** validation - TEST-FULL-H1-final.csv
**Dry-run:** No
**Rows evaluated:** 45
**Methods executed:** 1
**Runtime:** 2839.24 s
**Total tokens:** 244586
**Estimated token cost:** $8.7855
**Results CSV:** `results_validation - TEST-FULL-H1-final.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation---TEST-FULL-H1-final_20250617_075802`
**Rows in evaluation file:** 125
**Rows with ground truth evaluated:** 45 (filtered)

## Methods
| ID | Model | Pipeline | Params |
|---|---|---|---|
| o3_ensemble5 | o3-2025-04-16 | one_shot | repeats=5, reasoning_effort=low, service_tier=flex, consensus_rule=dbscan, store=True |

## Prompts
| Pipeline | Prompt ID | Version |
|---|---|---|
| one_shot | one_shot_dms_v1 | v1 |
| tool_chain | tool_chain_v0 | v5 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| o3_ensemble5 | 45 | 22.64 | 244586 | 8.7855 |

## Accuracy Summary
Average Haversine error: **22.64 km**
High (<1 km): 0 Medium (1–10 km): 17 Low (>10 km): 28