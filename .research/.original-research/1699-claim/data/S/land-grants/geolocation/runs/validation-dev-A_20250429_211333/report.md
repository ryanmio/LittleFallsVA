# Geolocation Experiment – Run Report

**Date:** 2025-04-29 21:13:42
**CLI command flags:** `--evalset=validation-dev-A.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --seed=123 --verbose --max_rows=2`
**Evaluation set:** validation-dev-A.csv
**Dry-run:** No
**Rows evaluated:** 2
**Methods executed:** 2
**Runtime:** 8.93 s
**Total tokens:** 2401
**Estimated cost:** $0.0056
**Results CSV:** `results_validation-dev-A.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation-dev-A_20250429_211333`
**Rows in evaluation file:** 20
**Rows with ground truth evaluated:** 2 (filtered)

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
| M-4 | 2 | 12.42 | 400 | 0.0010 |
| T-4 | 2 | 1.52 | 2001 | 0.0045 |

## Accuracy Summary
Average Haversine error: **6.97 km**
High (<1 km): 0 Medium (1–10 km): 2 Low (>10 km): 2