# Geolocation Experiment – Run Report

**Date:** 2025-05-04 23:31:00
**CLI command flags:** `--evalset=validation-dev-A.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --seed=123 --verbose --max_rows=10`
**Evaluation set:** validation-dev-A.csv
**Dry-run:** No
**Rows evaluated:** 10
**Methods executed:** 8
**Runtime:** 9544.13 s
**Total tokens:** 188932
**Estimated cost:** $3.0426
**Results CSV:** `results_validation-dev-A.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation-dev-A_20250504_205155`
**Rows in evaluation file:** 20
**Rows with ground truth evaluated:** 10 (filtered)

## Methods
| ID | Model | Pipeline | Params |
|---|---|---|---|
| M-1 | o4-mini-2025-04-16 | one_shot | reasoning_effort=medium, service_tier=flex, store=True |
| M-2 | o3-2025-04-16 | one_shot | reasoning_effort=medium, service_tier=flex, store=True |
| M-3 | o3-mini-2025-01-31 | one_shot | reasoning_effort=medium, store=True |
| M-5 | chatgpt-4o-latest | one_shot | temperature=0.2, store=True |
| M-6 | gpt-3.5-turbo | one_shot | temperature=0.2, store=True |
| T-3 | o3-mini-2025-01-31 | tool_chain | reasoning_effort=low, store=True |
| T-4 | gpt-4.1-2025-04-14 | tool_chain | temperature=0.2, store=True |
| T-5 | computer-use-preview-2025-03-11 | tool_chain | temperature=0.2, store=True |

## Prompts
| Pipeline | Prompt ID | Version |
|---|---|---|
| one_shot | one_shot_dms_v1 | v1 |
| tool_chain | tool_chain_v0 | v3 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| M-1 | 10 | 23.18 | 23465 | 0.0974 |
| M-2 | 10 | 16.55 | 28137 | 1.0722 |
| M-3 | 10 | 28.74 | 32247 | 1.2366 |
| M-5 | 10 | 20.31 | 1985 | 0.0119 |
| M-6 | 10 | 31.29 | 1988 | 0.0012 |
| T-3 | 10 | 36.75 | 29382 | 0.4296 |
| T-4 | 10 | 20.95 | 37805 | 0.0821 |
| T-5 | 10 | 21.16 | 33923 | 0.1115 |

## Accuracy Summary
Average Haversine error: **24.87 km**
High (<1 km): 1 Medium (1–10 km): 20 Low (>10 km): 59