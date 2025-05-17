# Geolocation Experiment – Run Report

**Date:** 2025-05-08 07:57:33
**CLI command flags:** `--evalset=validation - TEST-FULL-H1.csv --methods_file=methods_sweep.yaml --prompts_file=prompts.yaml --seed=123 --max_rows=1`
**Evaluation set:** validation - TEST-FULL-H1.csv
**Dry-run:** No
**Rows evaluated:** 1
**Methods executed:** 11
**Runtime:** 80.50 s
**Total tokens:** 6949
**Estimated token cost:** $0.2158
**Results CSV:** `results_validation - TEST-FULL-H1.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods_sweep.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation---TEST-FULL-H1_20250508_075612`
**Rows in evaluation file:** 125
**Rows with ground truth evaluated:** 1 (filtered)

## Methods
| ID | Model | Pipeline | Params |
|---|---|---|---|
| M2-low | o3-2025-04-16 | one_shot | reasoning_effort=low, service_tier=flex, store=True |
| M2-med | o3-2025-04-16 | one_shot | reasoning_effort=medium, service_tier=flex, store=True |
| M2-high | o3-2025-04-16 | one_shot | reasoning_effort=high, service_tier=flex, store=True |
| M4-t0.0 | gpt-4.1-2025-04-14 | one_shot | temperature=0.0, store=True |
| M4-t0.4 | gpt-4.1-2025-04-14 | one_shot | temperature=0.4, store=True |
| M4-t0.8 | gpt-4.1-2025-04-14 | one_shot | temperature=0.8, store=True |
| M4-t1.2 | gpt-4.1-2025-04-14 | one_shot | temperature=1.2, store=True |
| M5-t0.0 | chatgpt-4o-latest | one_shot | temperature=0.0, store=True |
| M5-t0.4 | chatgpt-4o-latest | one_shot | temperature=0.4, store=True |
| M5-t0.8 | chatgpt-4o-latest | one_shot | temperature=0.8, store=True |
| M5-t1.2 | chatgpt-4o-latest | one_shot | temperature=1.2, store=True |

## Prompts
| Pipeline | Prompt ID | Version |
|---|---|---|
| one_shot | one_shot_dms_v1 | v1 |
| tool_chain | tool_chain_v0 | v5 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| M2-low | 1 | 0.94 | 751 | 0.0255 |
| M2-med | 1 | 4.28 | 2031 | 0.0767 |
| M2-high | 1 | 2.94 | 2799 | 0.1075 |
| M4-t0.0 | 1 | 26.38 | 171 | 0.0005 |
| M4-t0.4 | 1 | 19.79 | 171 | 0.0005 |
| M4-t0.8 | 1 | 22.93 | 171 | 0.0005 |
| M4-t1.2 | 1 | 15.95 | 171 | 0.0005 |
| M5-t0.0 | 1 | 15.12 | 171 | 0.0011 |
| M5-t0.4 | 1 | 25.00 | 171 | 0.0011 |
| M5-t0.8 | 1 | 12.47 | 171 | 0.0011 |
| M5-t1.2 | 1 | 14.62 | 171 | 0.0011 |

## Accuracy Summary
Average Haversine error: **14.58 km**
High (<1 km): 1 Medium (1–10 km): 2 Low (>10 km): 8