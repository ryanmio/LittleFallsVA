---
factor: "D"          # Brick vs. wood chimneys prevalence
dataset_id: "hallowes_site_brick_chimney_1640s"  # Unique identifier
evidence_type: "Archaeological site re‑analysis (qualitative case study)"

# Evidence characterization
qualitative_only: true  # No explicit counts

# Hyperprior for qualitative evidence suggesting rarity but possibility
alpha0: 1   # Beta(1,9) → mean 0.10 (rare) 
beta0: 9

# Calculated fields (leave blank)
alpha:               
beta:                
mean:                
ci_lower:            
ci_upper:            

# Documentation fields
sources:
  - "Hatch, D. Brad, Benjamin J. Heath, and Lauren K. McMillan. 2014. \"Reassessing the Hallowes Site: Conflict and Settlement in the Seventeenth‑Century Potomac Valley.\" Historical Archaeology 48 (4): 46–75."

notes: |
  - **Key quotation (p. verify):** "Located slightly off center of the interior of the structure were the remains of an H‑shaped, partially robbed, brick chimney base." This clearly documents a brick chimney in a mid‑17th‑century vernacular dwelling on Virginia's Northern Neck.
  - The site re‑analysis dates the building's occupation to c. 1647–1680, demonstrating that brick chimneys were technologically and economically feasible in frontier contexts decades before 1699.
  - Because the article discusses only a single excavated structure, it does **not** provide population‑level frequency statistics. We therefore treat it as **qualitative evidence** that brick chimneys *existed* but were likely uncommon.
  - Translating "rare but attested" to probability, we retain a conservative Beta(1,9) hyperprior (mean=10 %), keeping weight low (α+β=10) so that broader quantitative surveys can dominate.
  - **Geographic transferability:** The Hallowes Site lies ~90 mi south of Falls Church and closer to navigable waterways. While still a frontier setting, building materials might have been more accessible than at Falls Church in 1699. Therefore, applicability is moderate and uncertainties remain.
  - **Limitations:** Single case study; no comparative denominator; possible socio‑economic bias (John Hallowes was relatively wealthy). Future survey data across multiple Potomac frontier sites are needed.

---
### Summary

The Hallowes Site (44WM6) excavation revealed a hall‑and‑parlor earthfast dwelling (c. 1647) containing an **H‑shaped brick chimney base**. Although only one structure, this finding confirms that brick chimneys were *possible* in mid‑17th‑century frontier Virginia. The evidence suggests a non‑zero, yet still low, prevalence for brick chimneys in similar contexts, supporting a conservative prior mean of 10 % for Factor D. 