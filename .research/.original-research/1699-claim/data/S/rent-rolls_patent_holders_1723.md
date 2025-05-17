---
factor: S
dataset_id: rent-rolls_patent_holders_1723
evidence_type: "Cross-match of \u22641723 land patents (\u226410 km radius of Falls\
  \ Church) with the 1723 Stafford County rent roll"
qualitative_only: false
k: 1
n: 5
alpha0: 1
beta0: 1
alpha: 2
beta: 5
mean: 0.2857
ci_lower: 0.0
ci_upper: 0.5988
sources:
- Stafford County Rent Roll for the Year 1723. Manuscript, Huntington Library, San
  Marino (microfilm BR 297 Item 1). Transcribed May 2011 by Greg Mason.
- Digitised Northern Neck land-patent markdown files in `patent_bounds/` directory
  (individual citation lines therein).
notes: "## DATA DESCRIPTION\nThis dataset quantifies the proportion of European land-patent\
  \ holders within a 10 km radius of the Big Chimneys site who were *actively paying\
  \ quit-rents* by mid-1723. Presence on the rent roll constitutes direct documentary\
  \ evidence of permanent structures built in the region and thus bears on **Factor\
  \ S** (a structure intended to be permanent was built during 1669-1729).\n\n###\
  \ Risk-Set Approach\nWe use a \"risk-set\" approach, considering only patents that\
  \ would have reached their improvement covenant deadline by July 1723:\n\u2022 **Inclusion\
  \ criterion:** Patent issued \u2264 1722 (allowing for the standard 12-month Northern\
  \ Neck improvement period).\n\u2022 Absence from the rent-roll represents a genuine\
  \ failure only if the owner was legally obligated to pay.\n\u2022 Patents from 1723\u2013\
  1729 are excluded because their owners were not yet liable; treating their absence\
  \ as a failure would introduce right-censoring bias.\n\n### Counting Units\n\u2022\
  \ **Trial (n):** A unique land patent whose centroid lies \u226410 km of Big Chimneys\
  \ *and* has a grant date early enough to have required improvements by 1723.  \n\
  \u2022 **Success (k):** The patent-holder's surname and first initial (when available)\
  \ match entries on the 1723 Stafford rent-roll.\n\n### Data Completeness Note\n\u2022\
  \ **Current corpus limitation:** The current digitized patent corpus is incomplete.\
  \ Several known pre-1723 patents (e.g., John West, Henry Fitzhugh leases, 1712 Goin)\
  \ have been identified in historical records but not yet transcribed into markdown\
  \ format.\n\u2022 The current k and n values reflect only the digitized subset,\
  \ and will be updated as additional patents are processed.\n\u2022 Missing patents\
  \ are treated as an ongoing data-collection task rather than as failures in the\
  \ denominator.\n\n### Inclusion / Exclusion Criteria\n\u2022 Patents beyond 10 km\
  \ are excluded to focus on Falls Church-adjacent settlement.  \n\u2022 Patents dated\
  \ after 1722 are excluded because their owners would not yet be required to have\
  \ completed improvements and thus not liable for quit-rents in 1723.  \n\u2022 Where\
  \ multiple patents belong to the same individual, that person is counted **once**\
  \ to preserve Bernoulli independence.\n\n### Workflow Summary\n1. **Parse rent-roll\
  \ markdown** to extract surnames and first initials.  \n2. **Scan patent markdowns**\
  \ in `patent_bounds/` to gather grantee names.  \n3. **Spatial filter**: For now,\
  \ apply a manual inclusion list of patents confidently \u226410 km; replace with\
  \ GIS when shapes exist.  \n4. **Temporal filter**: retain `grant_year \u2264 1722`\
  \ to ensure improvement covenant maturity.  \n5. **Cross-match names** requiring\
  \ both surname and first initial to match when available.  \n6. Record *k* and *n*;\
  \ posterior parameters will be `\u03B1 = 1 + k`, `\u03B2 = 1 + n \u2212 k`.\n\n\
  ### Assumptions & Limitations\n\u2022 The rent-roll's absence of a name may reflect\
  \ non-payment or archival loss; we nevertheless treat it as a failure because the\
  \ *obligation* existed.  \n\u2022 Manual inclusion list is provisional; GIS filtering\
  \ will improve accuracy.  \n\u2022 Orthographic variants (e.g., \"FitzHugh\" vs\
  \ \"Fitzhugh\") are resolved automatically where possible; ambiguous cases flagged\
  \ for review.  \n\u2022 Missing earlier rent-rolls are *not* encoded as additional\
  \ failures but discussed qualitatively elsewhere."
---
### Summary

The 1723 Stafford County rent roll lists **tax-paying landowners** across the county. By linking names to pre-1724 patents within a 10 km radius of Big Chimneys, we obtain a data-driven measure of permanent European settlement near Falls Church by the early 1720s. 

Our analysis uses a **"risk-set" approach** that considers only patents whose improvement covenant would have matured by 1723. This requires patents to be issued by 1722 or earlier, allowing for the typical 12-month improvement period in Northern Neck grants. We identified **1 match** among **5 total** eligible patent-holder entries, yielding a posterior Beta(2.0, 5.0) distribution with a mean of **0.286** and a 95% confidence interval of **[0.000, 0.599]**.

The single confirmed match was Fitzhugh (appearing in two entries in the rent roll, including one with 17,630 acres). Four other patent holders from the pre-1723 period (Gabriel Adams, Sampson Darrell, Thomas Pearson, and Simon Pearson) did not appear in the rent roll despite holding patents in the area. Later patents (e.g., Charles Broadwater, 1749) are correctly excluded since their owners would not yet have been required to pay quit-rents in 1723.

This evidence supports Factor S by showing that patent-holders were sometimes maintaining permanent structures in the area by 1723, though at a relatively low rate. The precise first-initial matching and risk-set approach provide a statistically sound estimate of settlement patterns, though the current sample size is small due to the incomplete digitization of pre-1723 patents.

#### Cross-match results (using surname + first initial matching)

| Patent-holder name | Surname | First Initial | Grant Year | Rent-roll match? | Notes |
|---|---|---|---|---|---|
| Fitzhugh | fitzhugh | - | c.1720 | ✅ | 2 separate rent-roll entries |
| Gabriel Adams Sr. | adams | g | 1716 | ❌ | No matching initial in rent roll |
| Sampson Darrell | darrell | s | 1715 | ❌ | No entry found |
| Thomas Pearson | pearson | t | unknown | ❌ | No entry found |
| Simon Pearson | pearson | s | 1716-24 | ❌ | No entry found |

### Known Missing Patents

Several pre-1723 patents have been identified in historical sources but are not yet digitized in our corpus:

1. **John West's Alexandria Property** (c.1716-1720) - Referenced in Simon Pearson/Gabriel Adams grant
2. **Henry Fitzhugh Leases** (c.1710-1720) - Referenced in multiple secondary sources
3. **Thomas Going Patent** (c.1712) - Referenced in land records but not fully transcribed

These missing patents represent ongoing data collection efforts rather than failures; future digitization will expand the risk-set and may alter the k/n values.

### Interpretation & Context

1. **Earliest parallel datasets** – The 1723 Stafford quit-rent roll and the pre-1724 Northern Neck patents are the *first* overlapping administrative records for the Falls Church vicinity. Their mutual corroboration implies that tax and land-office processes were functioning and preserved for this period.

2. **Argument from silence** – No quit-rent entries nor NN patents link to Falls Church before 1712. Given (i) the existence of quit-rent lists for other Stafford landowners from c. 1700 onward and (ii) continuous operation of the NN land-office since 1690, we **would expect** a 1699 cabin's proprietor (or heirs) to appear in one or both datasets. Their absence therefore lowers the plausibility of a permanent European structure in 1699.

3. **Caveats** – Record loss is non-zero. Nevertheless, the comparative survival of both rolls and patents for nearby tracts (e.g., Potomac and Accotink patents) suggests that a systematic archival gap localized only to Falls Church is unlikely. 