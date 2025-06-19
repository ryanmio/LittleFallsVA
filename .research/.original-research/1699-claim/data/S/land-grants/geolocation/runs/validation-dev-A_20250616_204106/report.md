# Geolocation Experiment – Run Report

**Date:** 2025-06-16 20:42:12
**CLI command flags:** `--evalset=validation-dev-A.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --dry_run --seed=123 --verbose --max_rows=2`
**Evaluation set:** validation-dev-A.csv
**Dry-run:** Yes
**Rows evaluated:** 2
**Methods executed:** 12
**Runtime:** 65.38 s
**Total tokens:** 0
**Estimated token cost:** $0.0000
**Results CSV:** `results_validation-dev-A.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation-dev-A_20250616_204106`
**Rows in evaluation file:** 20
**Rows with ground truth evaluated:** 2 (filtered)

## Methods
| ID | Model | Pipeline | Params |
|---|---|---|---|
| M-1 | o4-mini-2025-04-16 | one_shot | reasoning_effort=medium, service_tier=flex, store=True |
| M-2 | o3-2025-04-16 | one_shot | reasoning_effort=medium, service_tier=flex, store=True |
| M-3 | o3-mini-2025-01-31 | one_shot | reasoning_effort=medium, store=True |
| M-4 | gpt-4.1-2025-04-14 | one_shot | temperature=0.2, store=True |
| M-5 | chatgpt-4o-latest | one_shot | temperature=0.2, store=True |
| M-6 | gpt-3.5-turbo | one_shot | temperature=0.2, store=True |
| T-1 | o4-mini-2025-04-16 | tool_chain | reasoning_effort=low, service_tier=flex, store=True |
| T-4 | gpt-4.1-2025-04-14 | tool_chain | temperature=0.2, store=True |
| H-1 | human-gis | static | fixed_cost_usd=140.0, billed_hours=6.0, store=True |
| o3_ensemble5 | o3-2025-04-16 | one_shot | repeats=5, reasoning_effort=medium, service_tier=flex, store=True |
| o3_ensemble5_db05 | o3-2025-04-16 | one_shot | repeats=5, temperature=0.6, consensus_rule=dbscan, store=True |
| o3_ensemble5_ttc | o3-2025-04-16 | one_shot | repeats=5, temperature=0.6, consensus_rule=ttc, store=True |

## Prompts
| Pipeline | Prompt ID | Version |
|---|---|---|
| one_shot | one_shot_dms_v1 | v1 |
| tool_chain | tool_chain_v0 | v5 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| M-1 | 2 | 6843.85 | 426 | 0.0000 |
| M-2 | 2 | 6844.01 | 450 | 0.0000 |
| M-3 | 2 | 6844.63 | 502 | 0.0000 |
| M-4 | 2 | 6844.88 | 498 | 0.0000 |
| M-5 | 2 | 6844.71 | 514 | 0.0000 |
| M-6 | 2 | 6844.80 | 486 | 0.0000 |
| T-1 | 2 | 6844.20 | 778 | 0.0000 |
| T-4 | 2 | 6843.93 | 738 | 0.0000 |
| H-1 | 2 | — | 0 | 0.0000 |
| o3_ensemble5 | 2 | 6852.90 | 2110 | 0.0000 |
| o3_ensemble5_db05 | 2 | 6852.84 | 2070 | 0.0000 |
| o3_ensemble5_ttc | 2 | 6849.18 | 2410 | 0.0000 |

## Accuracy Summary
Average Haversine error: **6846.36 km**
High (<1 km): 0 Medium (1–10 km): 0 Low (>10 km): 22