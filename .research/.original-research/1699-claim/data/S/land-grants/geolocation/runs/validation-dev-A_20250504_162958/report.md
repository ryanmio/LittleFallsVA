# Geolocation Experiment – Run Report

**Date:** 2025-05-04 16:30:10
**CLI command flags:** `--evalset=validation-dev-A.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --dry_run --seed=123 --verbose --max_rows=3`
**Evaluation set:** validation-dev-A.csv
**Dry-run:** Yes
**Rows evaluated:** 3
**Methods executed:** 3
**Runtime:** 11.16 s
**Total tokens:** 0
**Estimated cost:** $0.0000
**Results CSV:** `results_validation-dev-A.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation-dev-A_20250504_162958`
**Rows in evaluation file:** 20
**Rows with ground truth evaluated:** 3 (filtered)

## Methods
| ID | Model | Pipeline | Params |
|---|---|---|---|
| T-3 | o3-mini-2025-01-31 | tool_chain | reasoning_effort=low, store=True |
| T-4 | gpt-4.1-2025-04-14 | tool_chain | temperature=0.2, store=True |
| T-5 | computer-use-preview-2025-03-11 | tool_chain | temperature=0.2, store=True |

## Prompts
| Pipeline | Prompt ID | Version |
|---|---|---|
| one_shot | one_shot_dms_v1 | v1 |
| tool_chain | tool_chain_v0 | v1 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| T-3 | 3 | 6854.25 | 1218 | 0.0000 |
| T-4 | 3 | 6853.90 | 1140 | 0.0000 |
| T-5 | 3 | 6854.03 | 1170 | 0.0000 |

## Accuracy Summary
Average Haversine error: **6854.06 km**
High (<1 km): 0 Medium (1–10 km): 0 Low (>10 km): 9