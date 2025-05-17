# Geolocation Experiment – Run Report

**Date:** 2025-05-08 20:24:56
**CLI command flags:** `--evalset=validation - TEST-FULL-H1.csv --methods_file=methods-cost-optimized.yaml --prompts_file=prompts.yaml --seed=123`
**Evaluation set:** validation - TEST-FULL-H1.csv
**Dry-run:** No
**Rows evaluated:** 45
**Methods executed:** 3
**Runtime:** 148.56 s
**Total tokens:** 23127
**Estimated token cost:** $0.0068
**Results CSV:** `results_validation - TEST-FULL-H1.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods-cost-optimized.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation---TEST-FULL-H1_20250508_202227`
**Rows in evaluation file:** 125
**Rows with ground truth evaluated:** 45 (filtered)

## Methods
| ID | Model | Pipeline | Params |
|---|---|---|---|
| C-1 | gpt-4.1-mini | one_shot | temperature=0.2, store=True |
| C-2 | gpt-4.1-nano | one_shot | temperature=0.2, store=True |
| C-3 | gpt-4o-mini | one_shot | temperature=0.2, store=True |

## Prompts
| Pipeline | Prompt ID | Version |
|---|---|---|
| one_shot | one_shot_dms_v1 | v1 |
| tool_chain | tool_chain_v0 | v5 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| C-1 | 45 | 54.98 | 7601 | 0.0041 |
| C-2 | 45 | — | 7916 | 0.0012 |
| C-3 | 45 | 42.71 | 7610 | 0.0016 |

## Accuracy Summary
Average Haversine error: **48.92 km**
High (<1 km): 0 Medium (1–10 km): 7 Low (>10 km): 80