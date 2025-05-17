factor: "V"
dataset_id: "city_point_chimney_inscription_1763"
evidence_type: "Archaeological excavation report"

# Evidence characterization
qualitative_only: true

# For QUALITATIVE-ONLY evidence:
alpha0: 2          # mean 0.10, weight 20, reflects rarity of date inscriptions
beta0: 18

# Calculated fields - leave blank for notebook to fill
alpha:
beta:
mean:
ci_lower:
ci_upper:

# Documentation fields
sources:
  - "Orr, David G., Douglas Campana, and Brooke S. Blades. 1985. 'Uncovering Early Colonial City Point, Virginia.' Archaeology 38 (3): 64–65, 78. Quote on p. 64 referencing inscribed chimney brick (please verify exact pagination)."

notes: |
  The article briefly states that Richard Eppes rebuilt Appomattox Manor in 1763, "as indicated by a chimney brick inscribed with his initials and that date."  This constitutes **direct physical evidence** that brick chimney construction in colonial Virginia could include date inscriptions, albeit in the mid-eighteenth century.  Because the article gives only one example and offers no denominator of total chimneys examined, the data are treated as *qualitative-only* evidence bearing on the **existence but rarity** of date cartouches (Factor V).
  
  Prior selection rationale:
  - The observation confirms the *possibility* of inscribing dates on chimney bricks, so the mean should not be near zero.
  - However, a single example does not establish frequency; contemporary scholarship (e.g., Loth 1974) describes the practice as "rare."  A conservative Beta(2,18) prior (mean = 0.10, weight = 20) encodes this rarity while allowing future quantitative surveys to dominate.
  
  Limitations:
  - Geographic: City Point lies ~110 km south of Falls Church in the Lower James River region; cultural transferability to Northern Virginia is plausible but not certain.
  - Temporal: The brick dates to **1763**, more than six decades after the 1699 claim; technological practices may have evolved.
  - Methodological: The report does not enumerate other chimneys or bricks, so no prevalence rate can be computed.
  - Verification: Exact page number of the quoted sentence should be confirmed against the print layout.

---
### Summary

The National Park Service's 1983 excavation at City Point identified Appomattox Manor, built by Richard Eppes in 1763.  The authors note: *"Richard Eppes built this house in 1763, as indicated by a chimney brick inscribed with his initials and that date."*  (p. 64, verify).  This single explicit reference demonstrates that brick chimneys **could** bear inscription cartouches in colonial Virginia.  While later than the Falls Church claim, the example supports a non-zero prior probability for Factor V (existence of an inscribed brick) but, due to its singular nature, warrants a low-weight, low-mean prior such as Beta(2,18). 