---
factor: "R"
dataset_id: "indigenous_population_fausz_1987"
evidence_type: "Peer-reviewed historical review essay synthesizing population estimates"

# Evidence characterization
qualitative_only: true

# Data fields - hyperprior approach
k:      # No explicit success counts; qualitative synthesis
n:      # No explicit total counts
alpha0: 7    # Supports a high probability (70%) given widespread indigenous habitation
beta0: 3     # Conservative weight 10

# Calculated fields (to be filled by analysis notebook)
alpha:
beta:
mean:
ci_lower:
ci_upper:

# Documentation fields
sources:
  - "Fausz, J. Frederick. 1987. 'The Invasion of Virginia: Indians, Colonialism, and the Conquest of Cant: A Review Essay on Anglo‑Indian Relations in the Chesapeake.' *The Virginia Magazine of History and Biography* 95 (2): 133‑156."

notes: |
  - **Key passages supporting regional habitation:**
    - p. 134: "these lands at the confluence of the Pamunkey and Mattaponi Rivers contained one of the most significant Indian village complexes along the Atlantic coast when Euro‑Americans first arrived in Tidewater Virginia."
    - p. 142: "Christian F. Feest ... estimated Tidewater Algonquian populations of **some 14,000 – 22,000 for Virginia in 1607** and **12,000 for Maryland about 1634**."
  - **Interpretation.** The quoted figures and descriptions demonstrate dense, continuous Indigenous occupation of the Tidewater/Potomac corridor well before and during the late‑17th‑century window relevant to Falls Church (1669 – 1729). This materially supports Factor R's premise that the region was habitable and likely occupied around 1699.
  - **Transferability.** Falls Church sits within the greater Chesapeake cultural sphere described in the essay. While the article focuses on Tidewater broadly (rather than specifically Falls Church), it provides contextual evidence that Indigenous settlements were widespread in adjacent river valleys, indicating suitable habitation conditions for any population (Native or European) circa 1699.
  - **Limitations.**
    - Secondary synthesis: Fausz relies on prior demographic studies (e.g., Feest 1978) rather than new primary data.
    - Geographic granularity: Population numbers are province‑level, not specific to the Falls Church micro‑region.
    - Temporal precision: The closest numerical datapoint is for 1607; extrapolation to 1699 assumes continued, though likely diminished, Indigenous presence.
  - **Prior selection logic.** Vocabulary such as "significant" village complexes and explicit five‑figure population estimates imply that habitation was **common to majority** in the period. A conservative Beta(7,3) (mean = 0.70, weight = 10) aligns with this reading while preventing overweighting of a secondary source.
--- 