# Geolocation Experiment – Run Report

**Date:** 2025-06-19 15:32:32
**CLI command flags:** `--evalset=validation - TEST-FULL-H1-final.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --seed=123`
**Evaluation set:** validation - TEST-FULL-H1-final.csv
**Dry-run:** No
**Rows evaluated:** 45
**Methods executed:** 2
**Runtime:** 4165.86 s
**Total tokens:** 491624
**Estimated token cost:** $17.6877
**Results CSV:** `results_validation - TEST-FULL-H1-final.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation---TEST-FULL-H1-final_20250619_142306`
**Rows in evaluation file:** 125
**Rows with ground truth evaluated:** 45 (filtered)

## Methods
| ID | Model | Pipeline | Params |
|---|---|---|---|
| o3_ensemble5 | o3-2025-04-16 | one_shot | repeats=5, reasoning_effort=low, service_tier=flex, consensus_rule=dbscan, store=True |
| o3_ensemble5_redact | o3-2025-04-16 | one_shot | repeats=5, reasoning_effort=low, service_tier=flex, consensus_rule=dbscan, redact_names=True, store=True |

## Prompts
| Pipeline | Prompt ID | Version |
|---|---|---|
| one_shot | one_shot_dms_v1 | v1 |
| tool_chain | tool_chain_v0 | v5 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| o3_ensemble5 | 45 | 23.42 | 243946 | 8.7599 |
| o3_ensemble5_redact | 45 | 24.36 | 247678 | 8.9278 |

## Accuracy Summary
Average Haversine error: **23.89 km**
High (<1 km): 1 Medium (1–10 km): 28 Low (>10 km): 61