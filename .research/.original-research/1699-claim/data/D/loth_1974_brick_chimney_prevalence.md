---
factor: "D"          # Brick vs. wood chimneys prevalence
dataset_id: "loth_1974_brick_chimney_prevalence"
evidence_type: "Peer‑reviewed synthesis of chimney forms in Virginia brickwork"

# Evidence characterization
qualitative_only: true  # No explicit counts provided

# For QUALITATIVE-ONLY evidence:
alpha0: 5  # "Classic" and "always" suggest common but not universal (mean ≈0.33)
beta0: 10  # Weight = 15 (moderate confidence in descriptive evidence)

# Calculated fields - To be filled by analysis notebook
alpha:               
beta:                
mean:                
ci_lower:            
ci_upper:            

# Documentation fields
sources:             
  - "Loth, Calder. 1974. \"Notes on the Evolution of Virginia Brickwork from the Seventeenth Century to the Late Nineteenth Century.\" Bulletin of the Association for Preservation Technology 6(2):82‑120, esp. pp. 101–103."

notes: |
  # QUALITATIVE EVIDENCE: Document prior selection logic
  
  **Key phrases used by author suggesting frequency:**
  1. "Because of its resistance to heat, **brick has always been an ideal material for fireplaces and chimneys**." (p. 101)
  2. "The pyramidal chimney on Pear Valley is one of the earliest of Virginia chimney forms; it is **rarely found on buildings erected after the 1710's**." (p. 101)
  3. "This chimney … is the **classic chimney type** for simple colonial Virginia dwellings from the 1720's to the 1780's." (p. 103, Liberty Hall example)
  
  **How language was translated to probability:**
  The phrases "always been an ideal material" and "classic chimney type" suggest that brick chimneys were common—but not universal—on permanent dwellings. Translating these qualitative descriptors to a probability, I assign a mean of approximately 33% (0.33).
  
  **Justification for alpha0/beta0 values:**
  Beta(5,10) gives a mean of 0.333 with weight = 15, reflecting moderate confidence in the descriptive evidence while acknowledging uncertainty. This prior suggests brick chimneys were reasonably common but not predominant, and could vary by region and socioeconomic status.
  
  **Regional transferability considerations:**
  Falls Church lies in northern Virginia; while Loth's examples come mainly from Tidewater and the Valley, they cover statewide trends, supporting transferability. The author presents this as a general pattern across Virginia.
  
  **Limitations and future data needs:**
  - Focus on surviving brick structures creates survivorship bias toward masonry examples.
  - No direct comparison to wooden‑chimney frequency.
  - Descriptions span c. 1660–1780; prevalence likely varied by region and decade.
  - Quantitative archaeological surveys of period chimneys (brick vs. wood) would strengthen this evidence.
---
### Summary

Calder Loth's statewide review of Virginia brickwork includes significant discussion of chimney forms spanning the 17th and 18th centuries. His qualitative descriptions provide evidence on the prevalence of brick chimneys during the period relevant to the Falls Church 1699 claim.

The author describes brick as "always been an ideal material for fireplaces and chimneys" (p. 101) and identifies specific brick chimney forms as "classic" for colonial Virginia dwellings. He presents multiple case studies of brick chimneys from the period, including early examples like Pear Valley (c. 1660), Winona (late 17th century), and the Wishart House (c. 1680).

While Loth does not provide quantitative frequencies comparing brick chimneys to wooden alternatives, his language implies that brick chimneys were commonly adopted in permanent structures by the late 17th century—particularly for buildings intended to last. This supports a moderate prior probability for Factor D, encoded as Beta(5,10) with mean ≈33% and weight = 15.

The article's focus on studying intact brick structures creates an inherent bias toward buildings with masonry elements, leaving uncertainty about the relative proportion of wooden chimneys in more vernacular or temporary structures. Future archaeological evidence from a wider range of settlement sites would help refine this estimate. 