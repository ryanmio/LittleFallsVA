# Geolocation Experiment – Run Report

**Date:** 2025-05-05 08:43:11
**CLI command flags:** `--evalset=validation-dev-A.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --seed=123 --verbose --max_rows=10`
**Evaluation set:** validation-dev-A.csv
**Dry-run:** No
**Rows evaluated:** 10
**Methods executed:** 8
**Runtime:** 978.02 s
**Total tokens:** 164072
**Estimated cost:** $2.7668
**Results CSV:** `results_validation-dev-A.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation-dev-A_20250505_082652`
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
| tool_chain | tool_chain_v0 | v5 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| M-1 | 10 | 22.45 | 25321 | 0.1056 |
| M-2 | 10 | 14.88 | 26473 | 1.0057 |
| M-3 | 10 | 30.30 | 29239 | 1.1163 |
| M-5 | 10 | 19.78 | 1985 | 0.0119 |
| M-6 | 10 | 31.03 | 1992 | 0.0012 |
| T-3 | 10 | 37.71 | 28384 | 0.3837 |
| T-4 | 10 | 19.61 | 19841 | 0.0424 |
| T-5 | 10 | 18.06 | 30837 | 0.1000 |

## Accuracy Summary
Average Haversine error: **24.23 km**
High (<1 km): 2 Medium (1–10 km): 18 Low (>10 km): 60