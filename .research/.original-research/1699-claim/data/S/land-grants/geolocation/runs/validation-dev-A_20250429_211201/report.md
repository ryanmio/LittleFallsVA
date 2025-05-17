# Geolocation Experiment – Run Report

**Date:** 2025-04-29 21:12:07
**CLI command flags:** `--evalset=validation-dev-A.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --seed=123 --verbose --max_rows=1`
**Evaluation set:** validation-dev-A.csv
**Dry-run:** No
**Rows evaluated:** 1
**Methods executed:** 2
**Runtime:** 5.09 s
**Total tokens:** 1196
**Estimated cost:** $0.0028
**Results CSV:** `results_validation-dev-A.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation-dev-A_20250429_211201`
**Rows in evaluation file:** 20
**Rows with ground truth evaluated:** 1 (filtered)

## Methods
| ID | Model | Pipeline | Params |
|---|---|---|---|
| M-4 | gpt-4.1-2025-04-14 | one_shot | temperature=0.2, store=True |
| T-4 | gpt-4.1-2025-04-14 | tool_chain | temperature=0.2, store=True |

## Prompts
| Pipeline | Prompt ID | Version |
|---|---|---|
| one_shot | one_shot_dms_v1 | v1 |
| tool_chain | tool_chain_v0 | v1 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| M-4 | 1 | 13.52 | 196 | 0.0005 |
| T-4 | 1 | 1.23 | 1000 | 0.0023 |

## Accuracy Summary
Average Haversine error: **7.37 km**
High (<1 km): 0 Medium (1–10 km): 1 Low (>10 km): 1