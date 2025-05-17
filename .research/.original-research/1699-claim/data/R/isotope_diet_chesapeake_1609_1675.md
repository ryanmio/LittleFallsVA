---
factor: "R"
dataset_id: "isotope_diet_chesapeake_1609_1675"
evidence_type: "Stable isotope analysis of colonial Chesapeake human burials (1609–1675)"

# Evidence characterization
qualitative_only: false

# Data fields – quantitative evidence extracted from Table 1 (p. 133)
# Threshold criteria for 'local habitation ≥ 10 y' after ChatGPT suggestion:
#   δ13C ≥ −17 ‰ AND δ15N ≥ 9 ‰ → success
# Table has 27 rows; 3 flagged unreliable were removed (18CV271-12, APV-HR7, NPS-14A)
# Remaining usable observations: n = 24
# Successes meeting threshold: k = 13
k: 13
n: 24
alpha0: 0.5
beta0: 0.5

# Calculated fields – to be filled by analysis notebook
alpha:
beta:
mean:
ci_lower:
ci_upper:

# Documentation fields
sources:
  - "Ubelaker, Douglas H., and Douglas W. Owsley. 2003. 'Isotopic Evidence for Diet in the Seventeenth-Century Colonial Chesapeake.' American Antiquity 68 (1): 129-139, Table 1 p. 133."
notes: |
  ## QUANTITATIVE EVIDENCE EXTRACTION
  - **Counting unit:** individual skeletons with collagen & nitrogen isotope values in Table 1.
  - **Inclusion criteria:** rows with reliable collagen preservation (C/N 2.9–3.6) as specified by authors. Rows with C/N outside range and those explicitly flagged by authors (18CV271-12, APV-HR7, NPS-14A) were excluded, leaving *n = 24*.
  - **Success criterion (local occupation ≥ 10 years):** δ¹³C_collagen ≥ −17 ‰ (indicates sustained C₄/maize consumption) **AND** δ¹⁵N ≥ 9 ‰ (minimum protein sufficiency). Rationale: literature (Katzenberg 2000; Miller 1984) and authors' own discussion pp. 135-136 link these thresholds to individuals born or long-resident in the Chesapeake.
  - **Raw counts:** applying the rule yields *k = 13* successes.
  - **Assumptions & limitations:**
    * Burial samples cluster geographically ~120 km south of Falls Church; evidence extrapolates regional occupation rather than the exact Falls Church site.
    * Sample biased toward plantation contexts and Jamestown elite; may under-represent transient laborers.
    * Threshold is a conservative heuristic; future re-analysis may refine.
  ## PRIOR LOGIC
  - Tiny prior weight Beta(0.5,0.5) applied (following Recommendation A) to acknowledge spatial extrapolation (sites ~120 km south) while letting closer evidence dominate future updates.
  - Resulting posterior will be Beta(13.5,11.5) ⇒ mean ≈ 0.54; 95 % CI to be computed.
  ## CROSS-REFERENCE
  - Complements existing Factor R priors derived from settlement tax lists (dataset_id: tax_records_1700_va); both point to substantial regional occupation pre-1700.
  - No contradictions detected.
  ## LIMITATIONS FOR FALLS CHURCH CLAIM
  - Falls Church lies ~175 km upriver; maize suitability and European presence may differ slightly from Tidewater contexts.
  - Dietary isotopes prove occupation but not necessarily year-round habitation or structure building.
--- 