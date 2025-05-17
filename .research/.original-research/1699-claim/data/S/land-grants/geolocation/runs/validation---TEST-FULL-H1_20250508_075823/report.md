# Geolocation Experiment – Run Report

**Date:** 2025-05-08 10:26:20
**CLI command flags:** `--evalset=validation - TEST-FULL-H1.csv --methods_file=methods_sweep.yaml --prompts_file=prompts.yaml --seed=123`
**Evaluation set:** validation - TEST-FULL-H1.csv
**Dry-run:** No
**Rows evaluated:** 45
**Methods executed:** 11
**Runtime:** 8876.37 s
**Total tokens:** 566679
**Estimated token cost:** $19.7673
**Results CSV:** `results_validation - TEST-FULL-H1.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods_sweep.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation---TEST-FULL-H1_20250508_075823`
**Rows in evaluation file:** 125
**Rows with ground truth evaluated:** 45 (filtered)

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
| M2-low | 45 | 24.84 | 48994 | 1.7602 |
| M2-med | 45 | 24.92 | 143715 | 5.4089 |
| M2-high | 45 | 23.76 | 313186 | 12.3278 |
| M4-t0.0 | 45 | 33.98 | 7598 | 0.0206 |
| M4-t0.4 | 45 | 33.85 | 7598 | 0.0206 |
| M4-t0.8 | 45 | 31.67 | 7598 | 0.0206 |
| M4-t1.2 | 45 | 34.94 | 7598 | 0.0206 |
| M5-t0.0 | 45 | 32.08 | 7598 | 0.0470 |
| M5-t0.4 | 45 | 32.46 | 7598 | 0.0470 |
| M5-t0.8 | 45 | 33.03 | 7598 | 0.0470 |
| M5-t1.2 | 45 | 32.83 | 7598 | 0.0470 |

## Accuracy Summary
Average Haversine error: **30.76 km**
High (<1 km): 0 Medium (1–10 km): 102 Low (>10 km): 393