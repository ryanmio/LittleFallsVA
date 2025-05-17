# Geolocation Experiment – Run Report

**Date:** 2025-05-05 09:02:42
**CLI command flags:** `--evalset=validation-dev-A.csv --methods_file=methods.yaml --prompts_file=prompts_v6.yaml --seed=123 --verbose --max_rows=10`
**Evaluation set:** validation-dev-A.csv
**Dry-run:** No
**Rows evaluated:** 10
**Methods executed:** 2
**Runtime:** 101.03 s
**Total tokens:** 61253
**Estimated cost:** $0.1267
**Results CSV:** `results_validation-dev-A.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts_v6.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation-dev-A_20250505_090101`
**Rows in evaluation file:** 20
**Rows with ground truth evaluated:** 10 (filtered)

## Methods
| ID | Model | Pipeline | Params |
|---|---|---|---|
| M-6 | gpt-3.5-turbo | one_shot | temperature=0.2, store=True |
| T-4 | gpt-4.1-2025-04-14 | tool_chain | temperature=0.2, store=True |

## Prompts
| Pipeline | Prompt ID | Version |
|---|---|---|
| one_shot | one_shot_dms_v1 | v1 |
| tool_chain | tool_chain_v0 | v6 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| M-6 | 10 | 31.17 | 1990 | 0.0012 |
| T-4 | 10 | 20.03 | 59263 | 0.1256 |

## Accuracy Summary
Average Haversine error: **25.60 km**
High (<1 km): 0 Medium (1–10 km): 5 Low (>10 km): 15