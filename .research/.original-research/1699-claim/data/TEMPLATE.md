---
# EVIDENCE FILE TEMPLATE - GUIDANCE FOR RESEARCHERS
# =================================================

# ANALYZING SCHOLARLY ARTICLES FOR EVIDENCE EXTRACTION
# ===================================================
# Follow this workflow to systematically analyze scholarly sources:
#
# 1. IDENTIFY RELEVANT FACTORS
#    - Scan the article's abstract, introduction, and conclusion first
#    - Look for sections discussing: historic structures, building materials, chronology, settlement patterns
#    - Map findings to our factors:
#      → Factor R: Evidence about earliest settlement date in the region
#      → Factor S: Evidence about settlement vs. structure distinction
#      → Factor D: Evidence about brick vs. wood chimneys 
#      → Factor V: Evidence about date inscriptions/cartouches
#      → Factor A: Evidence about artifact chronology from the site
#
# 2. DETERMINE EVIDENCE TYPE AND EXTRACTION METHOD
#    a) For QUANTITATIVE evidence (explicit counts or percentages):
#       - Create a data extraction methodology:
#         → Define counting units clearly (e.g., structures, sites, features)
#         → Establish inclusion/exclusion criteria
#         → Document time period and geographic range
#         → Record raw counts: k (successes) and n (total observations)
#         → Note any sampling biases or limitations
#
#    b) For QUALITATIVE evidence (descriptive/narrative):
#       - Identify key phrases describing frequency/prevalence
#       - Extract direct quotes with page numbers
#       - Consider context: time period, region, socioeconomic factors
#       - Assess evidence strength (primary vs secondary, specificity)
#       - Translate qualitative assessments to appropriate hyperpriors
#
# 3. CROSS-REFERENCE WITH EXISTING EVIDENCE
#    - Check how new evidence relates to already documented sources
#    - Note agreements and discrepancies
#    - Consider how the new evidence strengthens, challenges, or refines existing priors
#
# 4. DOCUMENT LIMITATIONS TRANSPARENTLY
#    - Geographic relevance to Falls Church area
#    - Temporal scope and its match to the target period (c.1699)
#    - Methodological constraints from original research
#    - Generalizability concerns
#    - Potential biases in source material

# GUIDELINES FOR SETTING CONSERVATIVE HYPERPRIORS
# ================================================
# When setting hyperpriors for qualitative evidence, consider:
#
# 1. MEAN VALUE: α/(α+β) represents your best estimate of the probability
#    - Translate qualitative terms carefully: "rare" ≈ 5-15%, "common" ≈ 50-70%
#    - Be cautious not to overstate rarity or commonness without strong evidence
#
# 2. WEIGHT/CERTAINTY: (α+β) represents the "strength" or "weight" of your prior
#    - For qualitative evidence, keep weight low (typically 10-20)
#    - Stronger evidence should have higher weights; weaker evidence lower weights
#    - Example: Beta(1,9) has weight=10; Beta(3,17) has weight=20
#
# 3. INFLUENCE ON POSTERIOR: Lower weights get "washed out" more easily by quantitative data
#    - For secondary/tertiary sources or those with limited applicability, use lower weights
#    - For primary sources or highly relevant synthesis, somewhat higher weights may be justified
#
# 4. UNCERTAINTY RANGE: Check the 95% CI to ensure it captures reasonable possibilities
#    - Example: Beta(1,9) → mean=0.10, 95% CI ≈ [0.002, 0.45]
#    - Very wide intervals reflect high uncertainty, narrow intervals reflect confidence
#
# 5. CONSERVATISM PRINCIPLE: When in doubt, choose priors that:
#    - Have lower weights (to avoid overstating certainty)
#    - Have means that don't exaggerate rarity or commonness
#    - Allow for meaningful updates when harder data becomes available
#
# For uncertain qualitative evidence, priors like Beta(1,9) or Beta(2,18) allow for:
#    - Modest influence on the final analysis
#    - Reasonable mean estimates (10%)
#    - Wide confidence intervals reflecting uncertainty
#    - Getting appropriately outweighed by stronger quantitative evidence

# IMPORTANT: Never guess page numbers or citations; always verify with primary sources and ask human researchers when unsure.


# Required fields - Must be filled out
factor: "X"          # One of: R, S, D, V, A - corresponding to the factor in the chain rule
dataset_id: "descriptive_name_timeperiod"  # Unique identifier for this evidence, use lowercase with underscores
evidence_type: "Brief description of evidence type"  # e.g., "Archaeological survey", "Peer-reviewed synthesis"

# Evidence characterization
qualitative_only: false  # Set to 'true' if source contains no explicit counts

# Data fields - APPROACH DEPENDS ON EVIDENCE TYPE:
# For QUANTITATIVE evidence:
k:                   # Number of "successes" (integer) - e.g., structures with brick chimneys
n:                   # Total number of "trials" (integer) - e.g., total structures surveyed
alpha0: 1            # Hyperprior α (default 1) - Use 1 for uniform prior unless there's a specific reason
beta0: 1             # Hyperprior β (default 1) - Use 1 for uniform prior unless there's a specific reason

# For QUALITATIVE-ONLY evidence:
# k:                 # Leave blank - no explicit counts in source
# n:                 # Leave blank - no explicit counts in source
# alpha0: 2          # Set based on narrative (e.g., Beta(2,8) for "uncommon/~20%")
# beta0: 8           # Set based on narrative (e.g., Beta(2,8) for "uncommon/~20%")

# Calculated fields - Leave blank initially, will be filled by analysis notebook
alpha:               # Will be calculated as alpha0 + k
beta:                # Will be calculated as beta0 + n - k
mean:                # Will be calculated as alpha / (alpha + beta)
ci_lower:            # Will be calculated as 2.5th percentile of Beta(alpha, beta)
ci_upper:            # Will be calculated as 97.5th percentile of Beta(alpha, beta)

# Documentation fields
sources:             # List of sources, following Chicago style where possible
  - "Author Year, Title, Publication details, Pages"
  - "Archive Name, Collection Name, Item Identifier"

notes: |
  # QUANTITATIVE EVIDENCE: Include methodological details
  # - Sampling methodology
  # - Inclusion/exclusion criteria
  # - Date ranges considered
  # - Geographical scope
  # - Potential biases and how addressed
  
  # QUALITATIVE EVIDENCE: Document prior selection logic
  # - Key phrases used by author(s) suggesting frequency
  # - How language was translated to probability (e.g., "rare" → <15%)
  # - Justification for alpha0/beta0 values
  # - Regional transferability considerations
  # - Limitations and future data needs
  
  # EXAMPLE QUALITATIVE TRANSLATION GUIDANCE:
  # "Rare/few/uncommon": Beta with mean 0.10-0.20 (e.g., Beta(1,9) or Beta(2,8))
  # "Some/occasional": Beta with mean 0.25-0.35 (e.g., Beta(3,7) or Beta(3.5,6.5))
  # "Common/many": Beta with mean 0.50-0.70 (e.g., Beta(5,5) or Beta(7,3))
  # "Majority/most": Beta with mean 0.75-0.90 (e.g., Beta(7.5,2.5) or Beta(9,1))
  
  # For verification of Beta parameters, use:
  # Mean = alpha0/(alpha0+beta0)
  # 95% CI ≈ [2.5th percentile, 97.5th percentile] of Beta(alpha0,beta0)
---
### Summary

[Write a detailed narrative describing the evidence here. For QUANTITATIVE evidence, include:
1. What was examined/collected (e.g., "We tallied 43 pre-1700 structures...")
2. How it was analyzed (e.g., "...classified each as having brick or non-brick chimneys")
3. Key findings (e.g., "...found 12 structures (28%) had brick chimneys")
4. Uncertainties or limitations
5. Interpretation in context of the claim]

[For QUALITATIVE evidence, include:
1. Key thesis/argument of the source
2. Relevant evidence presented (e.g., case studies, archaeological findings)
3. Author's language regarding frequency (e.g., "rare," "common")
4. Temporal and regional scope of the findings
5. Social/economic factors affecting the phenomenon
6. Relationship to other evidence sources
7. Implication for the factor probability]

[Tables, lists, or other structured data can be included here if helpful.]

[If including tables, use markdown format:]

| Year | Document | Evidence |
|------|----------|----------|
| 1680 | Example  | Details  |
| 1701 | Example  | Details  | 