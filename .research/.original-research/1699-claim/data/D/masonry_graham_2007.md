---
# Required fields
factor: "D"
dataset_id: "masonry_graham_2007"
evidence_type: "Archaeological synthesis with percentage estimates"

# Evidence characterization
qualitative_only: true

# Data fields - hyperprior approach
k:      # No explicit counts extracted at this time
n:      # No explicit counts extracted at this time
alpha0: 3    # Prior α based on "less than 15%" for rural areas
beta0: 17    # Yields mean of 0.15 with reasonable uncertainty range

# Calculated fields (will be filled by analysis notebook)
alpha:  
beta:   
mean:   
ci_lower:
ci_upper:

# Documentation fields
sources:
  - "Graham, W., Hudgins, C. L., Lounsbury, C. R., Neiman, F. D., & Whittenburg, J. P. (2007). Adaptation and Innovation: Archaeological and Architectural Perspectives on the Seventeenth-Century Chesapeake. The William and Mary Quarterly, 64(3), 451–522. http://www.jstor.org/stable/25096728"

notes: |
  - **Data scope.** The article synthesizes findings from approximately 200+ archaeological sites in the Chesapeake region spanning 1607-1720, representing a ten-fold increase in the archaeological dataset compared to earlier studies like Carson et al. (1981).
  
  - **Explicit statistics.** The authors quantitatively state that masonry-walled buildings "still constituted about one-quarter [25%] of the buildings constructed from 1607 to 1720" but when urban centers (Jamestown, Saint Marys City, Annapolis, Williamsburg) are excluded, "the inventory of masonry-walled buildings in the Chesapeake dating from the first century of settlement is less than 15 percent" (p. 481).
  
  - **Rural focus justified.** Since Falls Church would have been a rural area in the Northern Virginia frontier circa 1699, we employ the rural percentage (<15%) rather than the aggregate including urban centers.
  
  - **Masonry-chimney relationship.** While the stated percentages refer to masonry walls rather than specifically brick chimneys, the article consistently treats masonry construction as an integrated package—if a building had masonry walls, it had masonry chimneys. The article notes that "fragments of brick and mortar turn up on seventeenth-century sites throughout the Chesapeake in sparing amounts, as if they were precious resources" (p. 478).
  
  - **Prior selection.** Beta(3,17) encodes "less than 15%" with a deliberate mean of 0.15 (3/20) and 95% CI ≈ [0.04, 0.31]. We chose this as a slightly conservative implementation of the "less than 15%" bound.
  
  - **Social distribution.** The article documents that brick construction was strongly associated with elite status and represented "costly signaling" primarily undertaken by "governors, councilors, and newly arrived immigrants with political and economic ties to Britain" (p. 484).
  
  - **Potential for upgrading.** This prior could be updated to fully quantitative if we obtain access to the complete dataset from the 200+ excavated sites analyzed in the article, particularly the site-by-site breakdown in Table I (p. 464) and any appendices.

---
### Summary

Graham et al. (2007) conducted a comprehensive quantitative analysis of over 200 archaeological sites across the Chesapeake region dating from 1607-1720. Their research determined that while masonry construction gradually increased in the last quarter of the 17th century, it "still constituted about one-quarter of the buildings constructed from 1607 to 1720." More relevantly for our analysis of Falls Church, they found that when urban centers (Jamestown, Saint Marys City, Annapolis, and Williamsburg) are excluded from the count, "the inventory of masonry-walled buildings in the Chesapeake dating from the first century of settlement is less than 15 percent" (p. 481). For truly rural areas, they note the percentage of brick dwellings was "negligible."

The authors document that brick construction was concentrated among elite plantation owners, merchants, and provincial officials who used it as a form of "costly signaling" to demonstrate wealth and status. Their statistical analysis of construction methods shows that nearly 60 percent of all buildings from 1607-1720 used earthfast (post-in-ground) construction (Table I, p. 464). Outside urban centers, the predominant construction method was the "Virginia house" – a wooden earthfast structure with riven clapboard siding. The article states: "Though a few colonists used bricks for foundations, cellars, and chimneys, brick-walled buildings first appeared in the 1640s and 1650s at only a few sites" (p. 478). Furthermore, most of these early brick structures were built by "well-connected immigrants...who had the financial wherewithal and the desire to build well and conspicuously soon after they arrived" (p. 478).

The authors also note that brick construction was particularly rare in newly settled frontier areas. Since the Falls Church area would have been on the frontier fringe in 1699, any structure there would have been especially unlikely to feature brick construction compared to areas along the James and York rivers where most early brick buildings were concentrated.

**Implication for Factor D**: The prevalence of brick chimneys in rural areas circa 1699 would have been low (less than 15%), providing a strong prior that any permanent structure in the Falls Church area would most likely have had wooden rather than brick chimneys. 