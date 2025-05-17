factor: "D"
dataset_id: "chimney_materials_carson_2008"
evidence_type: "Peer‑reviewed article on colonial building culture (architectural history synthesis)"

qualitative_only: true

# Data fields – qualitative evidence only
alpha0: 1   # Beta(1,9) encodes ~10% mean probability for brick chimneys, low weight 10
beta0: 9
k:          # not applicable
n:          # not applicable

# Calculated fields – to be auto‑filled by analysis notebook
alpha:
beta:
mean:
ci_lower:
ci_upper:

sources:
  - "Cary Carson, Joanne Bowen, Willie Graham, Martha McCartney, and Lorena Walsh. 2008. 'New World, Real World: Improvising English Culture in Seventeenth‑Century Virginia.' The Journal of Southern History 74 (1): 31–88, p. 59."

notes: |
  - **Direct quotes with verified page numbers:**
    1. "…considerably less expense than making and burning a kiln‑load of bricks for a chimney." (p. 59)
    2. "Chimneys, too, were wooden affairs—timber framed, parged with clay for fireproofing, and weatherized with the same riven boards used to cover walls and roofs." (p. 59)
  - **Interpretation:** These statements indicate that in the mid‑17th‑century Chesapeake, brick chimneys were comparatively expensive and therefore uncommon; most vernacular dwellings relied on wooden chimneys. This supports a **low prior probability (<15%)** that a structure built in or near Falls Church in 1699 would include a brick chimney (Factor D).
  - **Hyperprior rationale:** We translate the qualitative description "brick chimneys were costly and thus avoided" to a conservative Beta(1,9) prior (mean = 0.10, 95 % CI ≈ 0.002–0.45). The low weight (α+β = 10) reflects moderate confidence and allows future quantitative data to update the estimate.
  - **Cross‑reference:** Reinforces existing qualitative evidence (e.g., Graham 2007, Loth 1974, Shammas 2007) that places brick‑chimney prevalence below ~15 % before 1720.
  - **Limitations:** The article surveys the wider Chesapeake region, not Falls Church specifically; topography and access to brickmakers in northern Virginia could differ. The evidence is descriptive with no explicit counts.

---
### Summary
This peer‑reviewed synthesis argues that Chesapeake settlers adopted inexpensive timber‑frame "Virginia houses" with wooden, clay‑parged chimneys because firing bricks was cost‑prohibitive. The narrative implies brick chimneys were **rare** in the 1600s, offering qualitative support for assigning a low prior probability (≈10 %) that any 1699 Falls Church structure would have been built with a brick chimney. 