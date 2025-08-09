# Geolocation Experiment – Run Report

**Date:** 2025-08-07 21:20:49
**CLI command flags:** `--evalset=validation - TEST-FULL-H1-final.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --seed=123 --verbose`
**Evaluation set:** validation - TEST-FULL-H1-final.csv
**Dry-run:** No
**Rows evaluated:** 45
**Methods executed:** 2
**Runtime:** 4169.46 s
**Total tokens:** 299540
**Estimated token cost:** $2.8790
**Results CSV:** `results_validation - TEST-FULL-H1-final.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation---TEST-FULL-H1-final_20250807_201120`
**Rows in evaluation file:** 125
**Rows with ground truth evaluated:** 45 (filtered)

## Methods
| ID | Model | Pipeline | Params |
|---|---|---|---|
| M-7 | gpt-5-2025-08-07 | one_shot | reasoning_effort=medium, store=True |
| M-8 | gpt-5-mini-2025-08-07 | one_shot | reasoning_effort=medium, store=True |

## Prompts
| Pipeline | Prompt ID | Version |
|---|---|---|
| one_shot | one_shot_dms_v1 | v1 |
| tool_chain | tool_chain_v0 | v5 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| M-7 | 45 | 26.52 | 227892 | 2.2207 |
| M-8 | 45 | 38.62 | 71648 | 0.6583 |

## Accuracy Summary
Average Haversine error: **31.33 km**
High (<1 km): 0 Medium (1–10 km): 15 Low (>10 km): 58