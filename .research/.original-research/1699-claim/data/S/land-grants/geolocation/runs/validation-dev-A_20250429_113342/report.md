# Geolocation Experiment – Run Report

**Date:** 2025-04-29 11:36:45
**Evaluation set:** validation-dev-A.csv
**Dry-run:** Yes
**Rows evaluated:** 13
**Methods executed:** 10
**Runtime:** 183.83 s
**Total tokens:** 0
**Estimated cost:** $0.0000
**Results CSV:** `results_validation-dev-A.csv`

## Methods
| ID | Model | Pipeline | Params |
|---|---|---|---|
| M-1 | o4-mini-2025-04-16 | one_shot | reasoning_effort=medium, store=True, tools=[] |
| M-2 | o3-2025-04-16 | one_shot | reasoning_effort=medium, store=True, tools=[] |
| M-3 | o3-mini-2025-01-31 | one_shot | reasoning_effort=medium, store=True, tools=[] |
| M-4 | gpt-4.1-2025-04-14 | one_shot | temperature=0.2, store=True, tools=[] |
| M-5 | chatgpt-4o-latest | one_shot | temperature=0.2, store=True, tools=[] |
| T-1 | o4-mini-2025-04-16 | tool_chain | reasoning_effort=medium, store=True, tools=[] |
| T-2 | o3-2025-04-16 | tool_chain | reasoning_effort=medium, store=True, tools=[] |
| T-3 | o3-mini-2025-01-31 | tool_chain | reasoning_effort=medium, store=True, tools=[] |
| T-4 | gpt-4.1-2025-04-14 | tool_chain | temperature=0.2, store=True, tools=[] |
| T-5 | chatgpt-4o-latest | tool_chain | temperature=0.2, store=True, tools=[] |

## Prompts
| Pipeline | Prompt ID | Version |
|---|---|---|
| one_shot | one_shot_dms_v1 | v1 |
| tool_chain | tool_chain_v0 | v0 |

## Accuracy Summary
Average Haversine error: **6855.41 km**
High (<1 km): 0 Medium (1–10 km): 0 Low (>10 km): 65