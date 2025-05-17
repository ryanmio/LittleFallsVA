---
# Required fields
factor: "V"
dataset_id: "date_cartouche_graham_2007"
evidence_type: "Archaeological evidence of date inscriptions"

# Evidence characterization
qualitative_only: true

# Data fields - hyperprior approach
k:      # No explicit counts extracted at this time
n:      # No explicit counts extracted at this time
alpha0: 2    # Prior α based on documented but rare practice
beta0: 18    # Yields mean of 0.10 with appropriate uncertainty range

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
  - **Concrete evidence.** The article provides photographic evidence of a "1662" date cartouche from the John and Alice Page House (Figure X, p. 480). This constitutes direct archaeological confirmation that the practice of inscribing construction dates on masonry structures existed in the Chesapeake region in the 17th century.
  
  - **Cultural context.** The article places date inscriptions within a broader tradition of "formal encoded messages carved into the fabric of buildings" (p. 483). The authors argue these inscriptions served as "cultural touchstones... for a small circle of educated, politically active immigrant planters" (p. 484), indicating that the practice was established but limited to elite construction.
  
  - **Geographic proximity.** The article documents examples in Virginia's Tidewater region, which is geographically proximate to Falls Church. Cultural practices would have diffused from the Tidewater to the Piedmont/Northern Virginia frontier.
  
  - **Qualitative frequency.** While the article provides photographic evidence of the practice, it characterizes such date inscriptions as "rare" and part of a "small circle" of elite building conventions. The authors note that "only a few colonists" (p. 478) engaged in high-status brick construction with these features.
  
  - **Prior selection.** Beta(2,18) encodes a mean of 0.10, reflecting that date cartouches were documented but uncommon. The 95% CI of approximately [0.01, 0.25] encodes substantial uncertainty while acknowledging the practice's existence. This prior is deliberately conservative (lower than might be suggested by the article) to account for frontier conditions in Falls Church versus the more developed Tidewater region where most documented examples were found.
  
  - **Settlement pattern relevance.** The authors note that most early buildings "leave faint archaeological signatures" (p. 455), making explicit date markers particularly valuable for settlement chronology when they do exist.
  
  - **Potential for refinement.** This evidence could be strengthened through: (1) systematic analysis of the prevalence of date inscriptions in the 200+ sites studied; (2) further excavation at the Falls Church site specifically targeting masonry remains; (3) comparative analysis of date inscription practices in other frontier regions.

---
### Summary

Graham et al. (2007) provide rigorous archaeological evidence that the practice of inscribing dates on brick buildings existed in 17th-century Virginia. Their article, which synthesizes findings from over 200 archaeological sites in the Chesapeake region, includes a photograph (Figure X, p. 480) of a "1662" date cartouche from the John and Alice Page House at Middle Plantation. This concrete artifact demonstrates that some builders in the region were inscribing construction dates on brick structures nearly forty years before the purported 1699 date at Falls Church.

The authors situate these date inscriptions within a broader cultural context of formal architectural messaging among elite colonists. They write that such inscriptions, along with other ornamental features like glazed headers and water tables, functioned as "cultural touchstones... for a small circle of educated, politically active immigrant planters" (p. 484). The practice appears linked to social signaling among higher-status colonists who were using brick construction to distinguish themselves from the widespread wooden earthfast building tradition.

The documented examples come primarily from the Tidewater region, where most early brick construction was concentrated. This is significant for the Falls Church claim, as the Northern Virginia area would have been further from the centers of elite construction. However, the existence of the practice in the broader Virginia colony does establish that inscribing dates was within the repertoire of colonial builders by the late 17th century.

While establishing the practice's existence, the article also indicates its rarity. The authors repeatedly characterize brick construction with decorative elements as limited to a "small circle" of elite builders. They note that "only a few colonists" engaged in high-status brick construction with these features, suggesting that date inscriptions would have been uncommon, particularly in frontier areas.

**Implication for Factor V**: The archaeological evidence confirms that the practice of inscribing dates on brick structures existed in 17th-century Virginia, making the purported 1699 date at Falls Church plausible but statistically uncommon. A reasonable estimate based on the article's characterization would place the probability that a brick chimney from this period would contain a date inscription at approximately 10% (encoded as Beta(2,18)). 