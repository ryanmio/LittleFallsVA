---
factor: "D"
dataset_id: "jamestown_brick_chimneys_1607_1676"
evidence_type: "Archaeological and documentary synthesis"

# Evidence characterization
qualitative_only: true

# For QUALITATIVE-ONLY evidence:
alpha0: 2  # Beta(2,8) implies mean 0.20 for "uncommon but present"
beta0: 8

# Documentation fields
sources:
  - "Harrington 1950, \"Seventeenth Century Brickmaking and Tilemaking at Jamestown, Virginia\", The Virginia Magazine of History and Biography 58(1): 16-39, pp.17-19"

notes: |
  Key excerpts (page numbers from journal pagination):
  - p.17: "The first bricks were undoubtedly used as nogging, or filler between structural timbers, **and for chimneys**, and it is probable that bricks were not made in any large quantities during the first few years at Jamestown."
  - p.17: "Even so, bricks were made in sufficient quantities to be exported to the Bermudas in 1621..."
  - p.18: "A legislative order, issued in 1662, called for the building of 32 brick houses and required that no more wooden houses were to be built at Jamestown."
  - p.18: "The 32 new brick houses were certainly not built, for at the time of Bacon's Rebellion in 1676, Jamestown was said by a contemporary writer to have 'some 16 or 18 houses, most as is the Church built of brick.'"

  Translation to probability:
  - Early 17th‑c Jamestown used bricks primarily for chimneys, implying that having a **brick chimney** on a structure was possible but not predominant.
  - By 1676, contemporary testimony says "most" of 16‑18 standing houses were brick—suggesting brick chimneys likely present on a majority of surviving dwellings in that urban context.
  - However, Jamestown was an administrative center, not a frontier cabin settlement like Falls Church would have been c.1700. Brick availability and labor specialization were higher here.

  Hyperprior choice: Using a conservative Beta(2,8) (mean=0.20, 95% CI ≈ 0.02–0.45) reflects that brick chimneys were **present but still relatively uncommon** across the broader Chesapeake frontier, despite Jamestown's urban bias. The weight=10 keeps the influence modest.

  Limitations:
  - Geographic transferability: Jamestown (James City County) is ~120 km from Falls Church; brickmaking capacity farther inland/Northern Neck may have been lower.
  - Socio‑economic: Jamestown's status as capital likely inflated brick usage relative to frontier farmsteads.
  - Temporal: Evidence spans 1607–1676; extrapolation to c.1699 Northern Virginia assumes slow diffusion of brick technology.
  - No explicit counts of chimneys; inference ties brick houses to brick chimneys, which may overstate prevalence.

---
### Summary
Jamestown documentary and archaeological synthesis shows that bricks were used for **chimneys from the colony's earliest years** (post‑1607) and that by 1676 a majority of the ~16–18 standing Jamestown houses were brick structures. While highlighting the technical feasibility and growing availability of brick chimneys in the Chesapeake, the source also implies they remained **uncommon outside urban centers**. A conservative Beta(2,8) prior (mean = 0.20) is assigned to Factor D (brick chimney prevalence) to capture this moderate likelihood under Falls Church conditions circa 1699. 