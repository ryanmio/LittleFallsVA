# Geolocation Experiment – Run Report

**Date:** 2025-05-05 18:43:16
**CLI command flags:** `--evalset=validation - TEST-FULL-H1.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --seed=123 --max_rows=5`
**Evaluation set:** validation - TEST-FULL-H1.csv
**Dry-run:** No
**Rows evaluated:** 5
**Methods executed:** 10
**Runtime:** 1202.08 s
**Total tokens:** 121632
**Estimated token cost:** $141.6973
**Results CSV:** `results_validation - TEST-FULL-H1.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation---TEST-FULL-H1_20250505_182314`
**Rows in evaluation file:** 125
**Rows with ground truth evaluated:** 5 (filtered)

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
| T-3 | o3-mini-2025-01-31 | tool_chain | reasoning_effort=low, store=True |
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
| M-1 | 5 | 28.39 | 16565 | 0.0704 |
| M-2 | 5 | 14.18 | 15925 | 0.6142 |
| M-3 | 5 | 45.03 | 17564 | 0.6798 |
| M-4 | 5 | 28.00 | 865 | 0.0023 |
| M-5 | 5 | 22.31 | 865 | 0.0053 |
| M-6 | 5 | 25.06 | 868 | 0.0005 |
| T-1 | 5 | 32.11 | 43051 | 0.0574 |
| T-3 | 5 | 51.21 | 15711 | 0.2456 |
| T-4 | 5 | 29.94 | 10218 | 0.0219 |
| H-1 | 5 | 71.51 | 0 | 140.0000 |

## Accuracy Summary
Average Haversine error: **34.77 km**
High (<1 km): 0 Medium (1–10 km): 6 Low (>10 km): 44