---
factor: "R"
dataset_id: "arents_1939_tobacco_expansion_1699"
evidence_type: "Historical narrative address (qualitative)"

qualitative_only: true

# Quantitative fields left blank because evidence is descriptive
k:
n:

# Conservative hyperprior reflecting modest, qualitative support for regional occupation near 1699
alpha0: 2
beta0: 8

alpha:
beta:
mean:
ci_lower:
ci_upper:

sources:
  - "Arents, George. 1939. \"The Seed from Which Virginia Grew.\" *William and Mary College Quarterly Historical Magazine* 19 (2): 123–129. Page 129."

notes: |
  The passage on p. 129 states that the soil‑depleting tobacco economy "pushed settlers west, south and southwest ... thus the extension of English boundaries in this part of North America was to a degree dictated by the general occupation of tobacco growing."
  
  •  Time‑frame: Late 17th c. (context of address deals with post‑1612 expansion; by the 1680s the colony was in economic crisis, leading planters to abandon exhausted Tidewater plots).
  •  Geography: References movement beyond Tidewater toward the fall‑line frontier, which includes present‑day Falls Church.
  •  Evidence type: Qualitative description of migration drivers; no explicit counts.
  •  Prior rationale: Language implies a *non‑trivial but not universal* movement of planters beyond Tidewater c. 1670–1700. Assigned Beta(2,8) → mean = 0.20 with low weight (10) so harder evidence can override.
  •  Limitations: Address is secondary, rhetorical, and focuses on macro‑Virginia trends rather than Falls Church specifically. Does not quantify number of settlers or exact dates. Should be cross‑checked against primary land patents near the falls‑line.

---
### Summary

Arents (1939) recounts how continuous tobacco monoculture exhausted Tidewater soils, *forcing settlers westward* by the late‑17th century: "by the mere process of clearing timber the settler was able to move to the west, the south and the southwest" (p. 129). This qualitative statement supports Factor R by indicating that English settlement plausibly reached the fall‑line region (which includes Falls Church) in the decades around 1699. Evidence is descriptive, without counts; we therefore encode it with a conservative Beta(2,8) hyperprior (mean 0.20) and low evidentiary weight. 