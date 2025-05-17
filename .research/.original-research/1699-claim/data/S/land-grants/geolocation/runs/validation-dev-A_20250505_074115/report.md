# Geolocation Experiment – Run Report

**Date:** 2025-05-05 07:58:29
**CLI command flags:** `--evalset=validation-dev-A.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --seed=123 --verbose --max_rows=10`
**Evaluation set:** validation-dev-A.csv
**Dry-run:** No
**Rows evaluated:** 10
**Methods executed:** 8
**Runtime:** 1033.55 s
**Total tokens:** 225323
**Estimated cost:** $3.6307
**Results CSV:** `results_validation-dev-A.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation-dev-A_20250505_074115`
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
| tool_chain | tool_chain_v0 | v4 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| M-1 | 10 | 26.42 | 24297 | 0.1010 |
| M-2 | 10 | 19.68 | 30953 | 1.1849 |
| M-3 | 10 | 30.66 | 36281 | 1.3980 |
| M-5 | 10 | 19.91 | 1985 | 0.0119 |
| M-6 | 10 | 31.23 | 1992 | 0.0012 |
| T-3 | 10 | 22.19 | 46938 | 0.7068 |
| T-4 | 10 | 19.58 | 39112 | 0.0842 |
| T-5 | 10 | 19.72 | 43765 | 0.1426 |

## Accuracy Summary
Average Haversine error: **23.73 km**
High (<1 km): 0 Medium (1–10 km): 18 Low (>10 km): 61