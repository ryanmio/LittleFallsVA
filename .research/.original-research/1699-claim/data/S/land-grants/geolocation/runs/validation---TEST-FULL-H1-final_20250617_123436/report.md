# Geolocation Experiment – Run Report

**Date:** 2025-06-17 12:34:59
**CLI command flags:** `--evalset=validation - TEST-FULL-H1-final.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --dry_run --seed=123 --max_rows=2`
**Evaluation set:** validation - TEST-FULL-H1-final.csv
**Dry-run:** Yes
**Rows evaluated:** 2
**Methods executed:** 2
**Runtime:** 23.05 s
**Total tokens:** 0
**Estimated token cost:** $0.0000
**Results CSV:** `results_validation - TEST-FULL-H1-final.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation---TEST-FULL-H1-final_20250617_123436`
**Rows in evaluation file:** 125
**Rows with ground truth evaluated:** 2 (filtered)

## Methods
| ID | Model | Pipeline | Params |
|---|---|---|---|
| o3_ensemble5 | o3-2025-04-16 | one_shot | repeats=5, reasoning_effort=low, service_tier=flex, consensus_rule=dbscan, store=True |
| o3_ensemble5_redact | o3-2025-04-16 | one_shot | repeats=5, reasoning_effort=medium, service_tier=flex, consensus_rule=dbscan, redact_names=True, store=True |

## Prompts
| Pipeline | Prompt ID | Version |
|---|---|---|
| one_shot | one_shot_dms_v1 | v1 |
| tool_chain | tool_chain_v0 | v5 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| o3_ensemble5 | 2 | 6823.77 | 2770 | 0.0000 |
| o3_ensemble5_redact | 2 | 6823.45 | 2730 | 0.0000 |

## Accuracy Summary
Average Haversine error: **6823.61 km**
High (<1 km): 0 Medium (1–10 km): 0 Low (>10 km): 4