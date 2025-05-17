# Geolocation Experiment – Run Report

**Date:** 2025-05-04 17:02:14
**CLI command flags:** `--evalset=validation-dev-A.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --seed=123 --verbose --max_rows=1`
**Evaluation set:** validation-dev-A.csv
**Dry-run:** No
**Rows evaluated:** 1
**Methods executed:** 8
**Runtime:** 109.66 s
**Total tokens:** 12684
**Estimated cost:** $0.2131
**Results CSV:** `results_validation-dev-A.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation-dev-A_20250504_170025`
**Rows in evaluation file:** 20
**Rows with ground truth evaluated:** 1 (filtered)

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
| tool_chain | tool_chain_v0 | v1 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| M-1 | 1 | 13.57 | 4809 | 0.0206 |
| M-2 | 1 | — | 0 | 0.0000 |
| M-3 | 1 | 15.85 | 4356 | 0.1690 |
| M-5 | 1 | 12.84 | 197 | 0.0012 |
| M-6 | 1 | 6.25 | 196 | 0.0001 |
| T-3 | 1 | 1.23 | 1132 | 0.0166 |
| T-4 | 1 | 1.23 | 1000 | 0.0023 |
| T-5 | 1 | 1.23 | 994 | 0.0034 |

## Accuracy Summary
Average Haversine error: **7.46 km**
High (<1 km): 0 Medium (1–10 km): 4 Low (>10 km): 3