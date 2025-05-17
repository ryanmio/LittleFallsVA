# Geolocation Experiment – Run Report

**Date:** 2025-05-05 16:22:47
**CLI command flags:** `--evalset=validation - TEST-FULL-H1.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --seed=123 --max_rows=1`
**Evaluation set:** validation - TEST-FULL-H1.csv
**Dry-run:** No
**Rows evaluated:** 1
**Methods executed:** 10
**Runtime:** 97.58 s
**Total tokens:** 11880
**Estimated cost:** $140.2708
**Results CSV:** `results_validation - TEST-FULL-H1.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation---TEST-FULL-H1_20250505_162109`
**Rows in evaluation file:** 125
**Rows with ground truth evaluated:** 1 (filtered)

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
| M-1 | 1 | 38.06 | 2543 | 0.0107 |
| M-2 | 1 | 5.33 | 2031 | 0.0767 |
| M-3 | 1 | 41.64 | 3946 | 0.1533 |
| M-4 | 1 | 18.56 | 171 | 0.0005 |
| M-5 | 1 | 15.12 | 171 | 0.0011 |
| M-6 | 1 | 22.22 | 171 | 0.0001 |
| T-1 | 1 | — | 0 | 0.0000 |
| T-3 | 1 | 1.81 | 1932 | 0.0265 |
| T-4 | 1 | 1.81 | 915 | 0.0019 |
| H-1 | 1 | 48.09 | 0 | 140.0000 |

## Accuracy Summary
Average Haversine error: **21.40 km**
High (<1 km): 0 Medium (1–10 km): 3 Low (>10 km): 6