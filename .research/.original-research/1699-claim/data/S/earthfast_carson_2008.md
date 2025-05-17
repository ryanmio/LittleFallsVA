factor: "S"
dataset_id: "earthfast_carson_2008"
evidence_type: "Peer‑reviewed article on colonial building culture (architectural history synthesis)"

qualitative_only: true

# Data fields – qualitative evidence only
alpha0: 4   # Beta(4,6) encodes ~40% mean probability for permanent structures, low weight 10
beta0: 6
k:          # not applicable
n:          # not applicable

# Calculated fields – to be auto‑filled by analysis notebook
alpha:
beta:
mean:
ci_lower:
ci_upper:

sources:
  - "Cary Carson, Joanne Bowen, Willie Graham, Martha McCartney, and Lorena Walsh. 2008. 'New World, Real World: Improvising English Culture in Seventeenth‑Century Virginia.' The Journal of Southern History 74 (1): 31–88, pp. 51, 56, 59."

notes: |
  - **Direct quotes with verified page numbers:**
    1. "Variations on this economical construction technique [earthfast/post-in-ground] remained in common use into the eighteenth century." (p. 51)
    2. "Over the course of the seventeenth century, newcomers and seasoned colonists alike relied on one or another earthfast construction method for houses, barns, and frequently even public buildings." (p. 51)
    3. John Smith criticized "extravagant building, [which] put an entire enterprise at risk, be it a brand-new plantation or, as at Jamestown in 1608, an entire colony." (p. 56)
    4. "Its design was a masterful solution to the typical homesteader's—the 'ordinary beginner's'—need to manage his risks." (p. 59)
  
  - **Interpretation:** These statements indicate that throughout the 17th century, buildings with deliberately non-permanent "earthfast" construction (posts set directly into the ground) dominated Virginia's architectural landscape. Even well-established colonists, not just newcomers, preferred these economical solutions. This supports a **moderate prior probability (≈40%)** that a structure built near Falls Church in 1699 would have been constructed as a truly permanent (long-lasting) building (Factor S).
  
  - **Hyperprior rationale:** We translate the qualitative descriptions of widespread earthfast construction to a conservative Beta(4,6) prior (mean = 0.40, 95% CI ≈ 0.15–0.70). The low weight (α+β = 10) reflects moderate confidence and allows future quantitative data to update the estimate.
  
  - **Cross‑reference:** Consistent with archaeological evidence showing that even public buildings often used post-in-ground construction well into the early 18th century.
  
  - **Limitations:** 
    - The article focuses on the wider Chesapeake region, not Falls Church specifically
    - Northern Virginia settlement patterns might have differed from Tidewater areas
    - The evidence is descriptive with no explicit counts of permanent vs. impermanent structures
    - "Permanent" is a relative term—earthfast structures could last 10-20 years with maintenance

---
### Summary

This peer‑reviewed synthesis demonstrates that "earthfast" (post-in-ground) construction dominated Virginia's architectural landscape throughout the 17th century, with colonists deliberately choosing impermanent building methods to manage financial risks. The article shows this approach was economical and remained common into the early 18th century, even for public buildings.

Archaeological and historical evidence indicates most colonists—even those of means—chose cost-effective building solutions with shorter lifespans, allowing resources to be directed toward income-generating activities. As the authors note, colonists were "traditionalists by instinct and improvisers of necessity" (p. 31), adapting English building traditions to local conditions and economic realities.

This evidence supports assigning a prior probability of approximately 40% (Beta(4,6)) that any Falls Church structure dating to 1699 would have been built with truly permanent construction methods, rather than the more typical earthfast techniques that dominated the era. 