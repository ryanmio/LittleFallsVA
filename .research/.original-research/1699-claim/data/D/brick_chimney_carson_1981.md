---
# Required fields
factor: "D"
dataset_id: "brick_chimney_carson_1981"
evidence_type: "Architectural literature review on chimney prevalence"

# Evidence characterization
qualitative_only: true

# Data fields - hyperprior approach
k:      # No explicit counts in this source
n:      # No explicit counts in this source
alpha0: 2    # Prior α based on literature narrative
beta0: 8     # Prior β (mean 0.20); will be updated with future counts

# Calculated fields (will be filled by analysis notebook)
alpha:  
beta:   
mean:   
ci_lower:
ci_upper:

# Documentation fields
sources:
  - "Carson, Cary, Norman F. Barka, William M. Kelso, Gary W. Stone, and Dell Upton. 1981. 'Impermanent Architecture in the Southern American Colonies.' *Winterthur Portfolio* 16 (2/3): 135–196. https://www.jstor.org/stable/1180773."

notes: |
  - **Scope.**  The article synthesises both archaeological excavations (e.g.,
    Flowerdew Hundred, Jamestown Back Street, Carter's Grove) and probate/tax
    documents to argue that most southern colonial dwellings through the first
    quarter of the 18th century were built for short‑term use and lacked costly
    masonry features.
  - **Chimney evidence.**  Case studies repeatedly mention *stick‑and‑clay*
    chimneys or wooden chimney‑stacks daubed with mud; brick stacks appear
    principally in the homes of the planter elite and in urban settings.
    Archaeological reports cited (Jamestown Structure 115, Kingsmill sites,
    Charlton's Coffeehouse) show brick chimney remains in a *minority* of
    excavated houses dating before 1720.
  - **Qualitative frequency.**  The authors use phrases such as "few," "rare,"
    and "exception rather than rule" when describing brick chimneys prior to
    ca. 1730, implying a prevalence well below 30% in ordinary dwellings.
  - **Transferability.**  Falls Church lies within the cultural orbit of the
    Chesapeake region covered by Carson et al.; timber‑frame techniques and
    social stratification were broadly comparable.  It is therefore reasonable
    to apply their conclusions when setting a prior for Factor D.
  - **Limitations.**  The review aggregates disparate excavation reports; it
    does not present a unified count of chimney types.  Quantitative inference
    is thus provisional and should be updated as systematic surveys (e.g.,
    Tidewater Brick Survey 2021) become available.
  - **Prior selection.** Based on the narrative evidence, we estimate that approximately 
    one in five "permanent" structures (20%) would have had a brick chimney circa 1699.
    We encode this as Beta(2,8) with mean 0.20 and 95% CI ≈ [0.02, 0.48].

---
### Summary

Carson, Barka, Kelso, Stone, and Upton (1981) argue that the architectural
landscape of the southern colonies before roughly 1730 was characterised by
**impermanence and cheap materials**.  Timber‑frame houses with mud‑and‑stick
chimneys predominated, especially among small‑to‑middling planters and
indentured servants.  Brick chimneys, by contrast, served as conspicuous
consumption markers: they required skilled masons, imported brick or on‑site
kilns, and a commitment to permanence inconsistent with the "disposable"
housing strategy many colonists adopted.

Key qualitative takeaways relevant to Factor D:

1. **Rarity of brick chimneys** – Across multiple case studies the article
   describes brick chimneys in *"a few"* elite dwellings, whereas the norm was
   lumber or clay‑lined stacks.
2. **Temporal pattern** – A substantive increase in brick usage appears only
   in the 1730s, coinciding with rising prosperity and urbanisation.
3. **Social stratification** – Where brick chimneys do occur early, they are
   overwhelmingly associated with gentry households; their presence therefore
   cannot be assumed for an average farmstead.

**Implication for Prior Setting** – The qualitative language suggests a
probability on the order of *one in five* for a brick chimney in a "permanent"
structure circa 1699.  Pending quantitative data, we encode this as a diffuse
Beta(2,8) prior (mean 0.20, 95% CI ≈ [0.02, 0.48]).  This choice remains
provisional and will be updated when hard counts become available. 