# Geolocation Experiment – Run Report

**Date:** 2025-05-05 14:34:46
**CLI command flags:** `--evalset=validation - TEST-FULL-H1.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --dry_run --seed=123 --max_rows=5`
**Evaluation set:** validation - TEST-FULL-H1.csv
**Dry-run:** Yes
**Rows evaluated:** 5
**Methods executed:** 3
**Runtime:** 11.98 s
**Total tokens:** 0
**Estimated cost:** $0.0000
**Results CSV:** `results_validation - TEST-FULL-H1.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation - TEST-FULL-H1_20250505_143434`
**Rows in evaluation file:** 125
**Rows with ground truth evaluated:** 5 (filtered)

## Methods
| ID | Model | Pipeline | Params |
|---|---|---|---|
| M-6 | gpt-3.5-turbo | one_shot | temperature=0.2, store=True |
| T-4 | gpt-4.1-2025-04-14 | tool_chain | temperature=0.2, store=True |
| H-1 | human-gis | static | fixed_cost_usd=140.0, billed_hours=6.0, store=True |

## Prompts
| Pipeline | Prompt ID | Version |
|---|---|---|
| one_shot | one_shot_dms_v1 | v1 |
| tool_chain | tool_chain_v0 | v5 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| M-6 | 5 | 6813.78 | 940 | 0.0000 |
| T-4 | 5 | 6816.16 | 2160 | 0.0000 |
| H-1 | 5 | 71.51 | 0 | 0.0000 |

## Accuracy Summary
Average Haversine error: **4567.15 km**
High (<1 km): 0 Medium (1–10 km): 0 Low (>10 km): 15