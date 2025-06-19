# Geolocation Experiment – Run Report

**Date:** 2025-06-17 17:45:50
**CLI command flags:** `--evalset=validation - TEST-FULL-H1-final.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --seed=123`
**Evaluation set:** validation - TEST-FULL-H1-final.csv
**Dry-run:** No
**Rows evaluated:** 45
**Methods executed:** 1
**Runtime:** 12027.11 s
**Total tokens:** 668670
**Estimated token cost:** $25.6253
**Results CSV:** `results_validation - TEST-FULL-H1-final.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation---TEST-FULL-H1-final_20250617_142523`
**Rows in evaluation file:** 125
**Rows with ground truth evaluated:** 45 (filtered)

## Methods
| ID | Model | Pipeline | Params |
|---|---|---|---|
| o3_ensemble5_redact | o3-2025-04-16 | one_shot | repeats=5, reasoning_effort=medium, service_tier=flex, consensus_rule=dbscan, redact_names=True, store=True |

## Prompts
| Pipeline | Prompt ID | Version |
|---|---|---|
| one_shot | one_shot_dms_v1 | v1 |
| tool_chain | tool_chain_v0 | v5 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| o3_ensemble5_redact | 45 | 22.93 | 668670 | 25.6253 |

## Accuracy Summary
Average Haversine error: **22.93 km**
High (<1 km): 0 Medium (1–10 km): 19 Low (>10 km): 26