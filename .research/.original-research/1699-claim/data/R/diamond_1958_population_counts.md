---
factor: "R"
dataset_id: "jamestown_population_diamond_1958"
evidence_type: "Peer‑reviewed sociological analysis of 17th‑century Virginia demographics"

# Evidence characterization
qualitative_only: true

# Data fields – qualitative evidence only
alpha0: 6   # Beta(6,4) encodes ~60% mean probability, low weight 10
beta0: 4
k:
n:

# Calculated fields – to be auto‑filled by analysis notebook
alpha:
beta:
mean:
ci_lower:
ci_upper:

# Documentation fields
sources:
  - "Diamond, Sigmund. 1958. 'From Organization to Society: Virginia in the Seventeenth Century.' American Journal of Sociology 63 (5): 457‑475."

notes: |
  - **Key quantitative statements with verified page references:**
    1. *p. 458*: "In 1607, when the Virginia Company established a settlement at Jamestown, its population numbered **105**; and in 1624, when the crown revoked the charter of the Company, the population of Virginia amounted to *just over 1,200*, **despite** the fact that the Company had sent **more than 5,000 emigrants** during that seventeen‑year period."  
    2. *p. 470*: "About **4,800 emigrants** departed from England between November 1619 and February 1625, **nearly twice** as many as had gone during the entire period from 1607 to 1619."  
    3. *p. 459*: At the 1699 May‑Day exercises a student proclaimed, "*O happy Virginia*," which the author cites as evidence that **by 1699 Virginia had become a full-fledged society** rather than a mere company outpost.
  
  - **Interpretation for Factor R (Regional Occupation circa 1699):**  
    These population figures underscore the *slow* and *geographically concentrated* pace of English settlement in the first half of the 17th century. Even with thousands of immigrants, mortality and dispersion left fewer than 1,300 colonists by 1624, almost all in Tidewater. The later surge to ~4,800 arrivals by 1625 shows growth potential but still signals sparse occupation outside core riverine settlements. The author's observation that Virginia was regarded as a "society" by **1699** indicates that sustained habitation had taken hold by the end of the century, yet the earlier low numbers caution against assuming dense or universal settlement across all sub‑regions (e.g., Falls Church).
  
    Taken together, the evidence supports a **moderate prior probability (~60%)** that the Falls Church area was *habitable and plausibly occupied* by Europeans at some point between 1669‑1729, while acknowledging substantial uncertainty.
  
  - **Prior selection logic:**  
    We encode these mixed signals with a conservative Beta(6,4): mean = 0.60, weight = 10. This respects the indication that English Virginians were present and expanding by 1699 but avoids overstating certainty given the Tidewater focus and lack of direct evidence for Northern Virginia.
  
  - **Limitations & Transferability:**  
    • Geographic focus is primarily Jamestown and Tidewater; the Falls Church region (Northern Virginia) is not discussed.  
    • Quantitative data end in 1625, requiring cautious extrapolation to 1699.  
    • Figures pertain solely to European settlers; Indigenous occupancy patterns are outside the article's scope.
--- 