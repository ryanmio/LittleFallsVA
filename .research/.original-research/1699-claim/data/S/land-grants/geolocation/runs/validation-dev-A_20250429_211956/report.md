# Geolocation Experiment – Run Report

**Date:** 2025-04-29 21:20:56
**CLI command flags:** `--evalset=validation-dev-A.csv --methods_file=methods.yaml --prompts_file=prompts.yaml --seed=123 --verbose --max_rows=2`
**Evaluation set:** validation-dev-A.csv
**Dry-run:** No
**Rows evaluated:** 2
**Methods executed:** 5
**Runtime:** 59.67 s
**Total tokens:** 8375
**Estimated cost:** $0.2029
**Results CSV:** `results_validation-dev-A.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/validation-dev-A_20250429_211956`
**Rows in evaluation file:** 20
**Rows with ground truth evaluated:** 2 (filtered)

## Methods
| ID | Model | Pipeline | Params |
|---|---|---|---|
| M-3 | o3-mini-2025-01-31 | one_shot | reasoning_effort=medium, store=True |
| M-4 | gpt-4.1-2025-04-14 | one_shot | temperature=0.2, store=True |
| M-5 | chatgpt-4o-latest | one_shot | temperature=0.2, store=True |
| M-6 | gpt-3.5-turbo | one_shot | temperature=0.2, store=True |
| T-4 | gpt-4.1-2025-04-14 | tool_chain | temperature=0.2, store=True |

## Prompts
| Pipeline | Prompt ID | Version |
|---|---|---|
| one_shot | one_shot_dms_v1 | v1 |
| tool_chain | tool_chain_v0 | v1 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| M-3 | 2 | — | 5134 | 0.1946 |
| M-4 | 2 | 12.27 | 400 | 0.0010 |
| M-5 | 2 | 11.62 | 400 | 0.0024 |
| M-6 | 2 | — | 440 | 0.0003 |
| T-4 | 2 | 1.52 | 2001 | 0.0045 |

## Accuracy Summary
Average Haversine error: **8.47 km**
High (<1 km): 0 Medium (1–10 km): 2 Low (>10 km): 4