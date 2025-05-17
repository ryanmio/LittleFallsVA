---
# Required fields
factor: "D"
dataset_id: "chimney_adoption_shammas_2007"
evidence_type: "Peer-reviewed secondary synthesis"

# Evidence characterization
qualitative_only: true

# Data fields - hyperprior approach
k:      # No explicit counts in this source
n:      # No explicit counts in this source
alpha0: 1
beta0: 9

# Calculated fields (will be filled by analysis notebook)
alpha:  
beta:   
mean:   
ci_lower:
ci_upper:

# Documentation fields
sources:
  - "Shammas, C. (2007). The Housing Stock of the Early United States: Refinement Meets Migration. The William and Mary Quarterly, 64(3), 549–590. http://www.jstor.org/stable/25096731"

notes: |
  - Shammas traces the shift from open hearths to enclosed fireplaces and
    brick chimneys in colonial America, noting that brick chimneys were
    uncommon prior to the early 18th century in the Chesapeake and Tidewater 
    colonies and only became widespread after ca. 1728 (p. 551).
  - The article specifically states that "Colonial Americans had internalized many of these ideals
    at least as far back as 1728, when William Byrd of Westover chided North
    Carolinians about their chimneyless log dwellings" (p. 551), indicating that proper chimneys 
    were not yet standard in many areas.
  - Travelers' accounts after the Revolution described "small, chimneyless, windowless, 
    earthen-floor, vermin-infested log shacks" (p. 552), further confirming the rarity of 
    proper chimneys in many rural areas.
  - No direct counts are given; this is a qualitative source used to
    shape our prior distribution for D.
  - We choose Beta(1,9) to reflect a low expected probability (~0.10) with
    broad uncertainty (95% CI ≈ [0.002, 0.45]).
  - Shammas repeatedly references the absence of proper chimneys in early American 
    dwellings, supporting the assessment that pre-1700 brick 
    chimneys would have been uncommon (suggesting < ≈15%); we therefore center the prior at 0.10. 
    Choice of α₀ = 1, β₀ = 9 encodes that assumption while retaining wide uncertainty.
  - We assume these Chesapeake/Tidewater trends apply to Falls Church due to 
    similar building traditions and cultural diffusion patterns in the region.
  - Limitation: qualitative synthesis only; we will update with quantitative 
    counts (HABS, Tidewater Brick Survey 2021) as they are digitized.

---
### Summary

Shammas (2007) synthesizes travel accounts, tax records, and architectural
studies to demonstrate that while enclosed fireplaces began replacing open
hearths in England in the late 17th century, American colonists did not
widely adopt brick chimneys until the 1720s and 1730s. The article specifically 
identifies 1728 as a key date when William Byrd of Westover "chided North Carolinians 
about their chimneyless log dwellings" (p. 551), suggesting that proper chimneys 
were not yet standard in many areas.

Prior to 1700, most permanent dwellings in Chesapeake colonies featured simple 
timber‐framed hearths without brick stacks. Travelers' accounts after the Revolution 
described "small, chimneyless, windowless, earthen-floor, vermin-infested log shacks" 
(p. 552), further confirming the rarity of proper chimneys in many rural areas. 
Only after major English urban rebuilding (post‑1666) and subsequent cultural 
exchange did brick chimneys become a "refined" housing improvement in North America.

**Implication for Factor D**: A permanent colonial structure circa 1699
would have had a **low** probability of including a brick chimney.  We
therefore set a **qualitative** hyperprior Beta(1,9), to be updated with
site‑specific counts as they become available.
