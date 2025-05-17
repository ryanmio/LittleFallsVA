---
factor: "S"          # Settlement vs. structure permanence
dataset_id: "hallowes_earthfast_structure_1647"  # Unique identifier
=evidence_type: "Archaeological site re‑analysis of house construction (qualitative)"

# Evidence characterization
qualitative_only: true

# Hyperprior – earthfast example implies permanent structures were **uncommon** in frontier Potomac, so low mean (≈20%) and low weight
alpha0: 2   # Beta(2,8) mean 0.20, weight 10
beta0: 8

# Calculated fields – leave blank for notebook
alpha:
beta:
mean:
ci_lower:
ci_upper:

sources:
  - "Hatch, D. Brad, Benjamin J. Heath, and Lauren K. McMillan. 2014. \"Reassessing the Hallowes Site: Conflict and Settlement in the Seventeenth‑Century Potomac Valley.\" Historical Archaeology 48 (4): 46–75."

notes: |
  - **Direct quotes with verified page numbers:**
    1. "The structure was a hall‑and‑parlor plan of **earthfast construction** with an off‑center brick hearth." (p. 52)
    2. "The average lifespan of a post‑in‑ground structure in the Chesapeake was about **20 years** …" (p. 53)
    3. "The posts were not replaced during the life of the structure, supporting the argument that the site was occupied for a relatively short time." (p. 53)
  - **Interpretation:** Even a dwelling owned by a relatively prosperous planter (John Hallowes) on the Potomac frontier remained earthfast and short‑lived. This reinforces that truly permanent, long‑lasting construction was **uncommon** in the mid‑17th‑century Northern Neck and, by extension, likely rare near Falls Church c. 1699.
  - **Hyperprior rationale:** A single example cannot yield frequencies, but it demonstrates the viability—and prevalence—of impermanent solutions. We translate this to a conservative Beta(2,8) (mean = 0.20) indicating only a 20 % chance a 1699 Falls Church dwelling would have been built for long‑term durability.
  - **Geographic transferability:** The Hallowes Site lies ~90 mi south of Falls Church but in a comparable frontier ecological zone. Social status bias may inflate durability expectations, making this evidence, if anything, conservative for Falls Church.
  - **Limitations:** Single site; no comparison count; prosperity of owner may not represent typical settlers; assumes continuity of building norms from 1640s‑60s into 1699 era.

---
### Summary

Reanalysis of the Hallowes Site (44WM6) shows a ca. 1647 earthfast hall‑and‑parlor house whose posts lasted ~30 years at most. The short life expectancy and absence of post replacement confirm the structure was not intended as a long‑term, permanent building. This qualitative evidence supports a low prior (~20 %) for the probability that any Falls Church structure erected in 1699 would have been designed for lasting permanence (Factor S). 