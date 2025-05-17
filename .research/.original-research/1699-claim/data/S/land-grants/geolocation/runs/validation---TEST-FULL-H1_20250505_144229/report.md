# Geolocation Experiment – Run Report

**Date:** 2025-05-05 14:43:04
**CLI command flags:** `--evalset=validation - TEST-FULL-H1.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --seed=123 --max_rows=5`
**Evaluation set:** validation - TEST-FULL-H1.csv
**Dry-run:** No
**Rows evaluated:** 5
**Methods executed:** 3
**Runtime:** 35.62 s
**Total tokens:** 12510
**Estimated cost:** $140.0254
**Results CSV:** `results_validation - TEST-FULL-H1.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation---TEST-FULL-H1_20250505_144229`
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
| M-6 | 5 | 28.95 | 866 | 0.0005 |
| T-4 | 5 | 32.21 | 11644 | 0.0249 |
| H-1 | 5 | 71.51 | 0 | 140.0000 |

## Accuracy Summary
Average Haversine error: **44.22 km**
High (<1 km): 0 Medium (1–10 km): 2 Low (>10 km): 13