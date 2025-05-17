# Geolocation Experiment – Run Report

**Date:** 2025-05-06 08:38:53
**CLI command flags:** `--evalset=retry-3-calls.csv --methods_file=methods_patch_T1.yaml --prompts_file=prompts.yaml --seed=123`
**Evaluation set:** retry-3-calls.csv
**Dry-run:** No
**Rows evaluated:** 3
**Methods executed:** 1
**Runtime:** 18.53 s
**Total tokens:** 10056
**Estimated token cost:** $0.0134
**Results CSV:** `results_retry-3-calls.csv`

**Working directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation`
**Methods file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/methods_patch_T1.yaml`
**Prompts file:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/prompts.yaml`
**Results directory:** `/Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/runs/retry-3-calls_20250506_083835`
**Rows in evaluation file:** 3

## Methods
| ID | Model | Pipeline | Params |
|---|---|---|---|
| T-1 | o4-mini-2025-04-16 | tool_chain | reasoning_effort=low, service_tier=flex, store=True |

## Prompts
| Pipeline | Prompt ID | Version |
|---|---|---|
| one_shot | one_shot_dms_v1 | v1 |
| tool_chain | tool_chain_v0 | v5 |

## Method-level Summary
| Method | Calls | Avg error (km) | Tokens | Est. cost ($) |
|---|---|---|---|---|
| T-1 | 3 | 29.20 | 10056 | 0.0134 |

## Accuracy Summary
Average Haversine error: **29.20 km**
High (<1 km): 0 Medium (1–10 km): 0 Low (>10 km): 2