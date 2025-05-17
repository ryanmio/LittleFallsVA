---
factor: "R"  # Earliest settlement date in the region
dataset_id: "chesapeake_fall_line_expansion_1690s"  # Unique identifier
evidence_type: "Peer‑reviewed economic history synthesis"  # Article traces land development patterns

# Evidence characterization
qualitative_only: true  # Source provides descriptive narrative, no explicit settlement counts

# Hyperpriors for qualitative evidence (conservative)
alpha0: 4  # Mean 0.40, weight 10
beta0: 6

# Calculated fields (left blank for notebook)
alpha:
beta:
mean:
ci_lower:
ci_upper:

# Documentation fields
sources:
  - "Douglas Bradburn 2011, \"The Visible Fist: The Chesapeake Tobacco Trade in War and the Purpose of Empire, 1690–1715,\" William and Mary Quarterly 68(3): 361–386, esp. p. 381"

notes: |
  Bradburn (2011) discusses the rapid post‑1690 expansion of Virginia landownership and settlement:
  - p. 381: "land‑hungry men who began developing the last lands available up to the fall line in the 1690s and moving into the Piedmont after 1700."
  - Context: The fall‑line zone includes present‑day Falls Church; development up to this physical boundary by the 1690s implies European occupation was plausible in the immediate vicinity.
  
  Prior selection logic:
  - Bradburn provides qualitative—not quantitative—evidence that settlement reached the Falls Church vicinity by the late 1690s.
  - His phrasing ("began developing") suggests initial but not ubiquitous occupation—interpreted as ~40 % chance that any given fall‑line locality (like Falls Church) had at least one permanent European settler by 1699.
  - Following guidance, we encode this as Beta(4,6) → mean 0.40, weight 10, giving a wide 95 % CI (~0.12–0.73) to reflect uncertainty.
  
  Limitations:
  - Geographic: Article addresses Chesapeake generally; statement about the fall line is province‑wide, not site‑specific.
  - Temporal: Evidence bracket is the 1690s; assumes developments starting earlier in decade could include 1699.
  - No direct mention of Falls Church; inference relies on physical geography.
  - Qualitative narrative without counts; low weight keeps influence modest.

---
### Summary

Bradburn's synthesis of wartime economic dynamics notes that by the **1690s** Virginia land speculators and "land‑hungry men" were actively **developing parcels up to the fall line** (p. 381)—the physiographic boundary where Falls Church sits today. Although the passage does not enumerate settlers, it convincingly places agricultural and residential expansion into Northern Virginia just before 1700. This suggests a moderate (≈ 40 %) prior probability that Falls Church's specific locale could have hosted European habitation by **1699**, satisfying Factor R's requirement that the region was habitable and likely occupied. 