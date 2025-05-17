# Geolocation Experiment – Run Report

**Date:** 2025-05-17 08:51:33
**CLI command flags:** `--evalset=validation - TEST-FULL-H1-final.csv --methods_file=methods-h1-rerun.yaml --prompts_file=prompts.yaml --seed=123 --verbose`
**Evaluation set:** validation - TEST-FULL-H1-final.csv
**Dry-run:** No
**Rows evaluated:** 45
**Methods executed:** 1
**Runtime:** 0.01 s
**Total tokens:** 0
**Estimated token cost:** $0.0000
**Results CSV:** `results_validation - TEST-FULL-H1-final.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods-h1-rerun.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation---TEST-FULL-H1-final_20250517_085133`
**Rows in evaluation file:** 125
**Rows with ground truth evaluated:** 45 (filtered)

## Methods
| ID | Model | Pipeline | Params |
|---|---|---|---|
| H-1 | human-gis | static | fixed_cost_usd=140.0, billed_hours=6.0, store=True |

## Prompts
| Pipeline | Prompt ID | Version |
|---|---|---|
| one_shot | one_shot_dms_v1 | v1 |
| tool_chain | tool_chain_v0 | v5 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| H-1 | 45 | 72.19 | 0 | 140.0000 |

## Accuracy Summary
Average Haversine error: **72.19 km**
High (<1 km): 0 Medium (1–10 km): 2 Low (>10 km): 43