---
factor: "R"
dataset_id: "environmental_suitability_1650-1739"
evidence_type: "Environmental/geographical analysis"
k:            # successes (integer)
n:            # trials (integer)
alpha0: 1     # hyperprior α (default 1)
beta0: 1      # hyperprior β (default 1)
alpha:        # alpha0 + k
beta:         # beta0 + n - k
mean:         # alpha / (alpha + beta)
ci_lower:     # 2.5th percentile
ci_upper:     # 97.5th percentile
sources:
  # - "Environmental dataset X"
  # - "Historical climate study Y"
notes: |
  This analysis examines soil quality, water access, terrain, and other environmental factors.
---
### Summary
[INSERT EVIDENCE NARRATIVE HERE]

This dataset will assess environmental suitability for habitation in the Falls Church area during the target period (1669-1729), considering:

1. Water resources (streams, springs, wells)
2. Soil quality for agriculture
3. Topography and drainage
4. Timber resources
5. Historical climate conditions 