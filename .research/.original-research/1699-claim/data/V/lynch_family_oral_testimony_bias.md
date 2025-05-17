---
factor: "V"          # Date inscriptions/cartouches frequency – existence of the claimed "1699" brick
dataset_id: "lynch_family_oral_testimony_bias"
evidence_type: "Genealogical provenance analysis of oral testimony"

# Evidence characterization
qualitative_only: true  # No explicit counts; evaluative provenance study

# For QUALITATIVE-ONLY evidence: conservative low-weight prior
alpha0: 1   # Weak belief the brick existed
beta0: 14   # Very uncertain evidence → weight = 15, mean ≈ 0.067

# Calculated fields – to be auto-filled by analysis notebook
alpha:
beta:
mean:
ci_lower:
ci_upper:

# Documentation fields
sources:
  - "Falls Church News-Press, 'Longtime F.C. Resident & Former DAR President Marie Yochim Dies at Age 92', 26 Apr 2012, confirms oral tradition & Steadman relationship."
  - "Steadman, Melvin L. Jr. 1964. *Falls Church, By Fence and Fireside*, Falls Church Public Library, Introduction pp. iii-x (first print source of the '1699' brick story)."
  - "Stewart, Charles A. 1904. *A Virginia Village*, Washington DC: W.F. Roberts, p. 21 (earlier history that does **not** mention any 1699 brick despite interviewing Lynch family members)."
  - "Compiled genealogy: *Genealogical Connection from the Lynch Family to Melvin L. Steadman Jr.* (research memo, 2025) – establishes unbroken family line transmitting the story."

notes: |
  # QUALITATIVE EVIDENCE: Prior selection logic
  **Key provenance finding:** The only attested report of a chimney brick inscribed "1699" derives from the Lynch family (owners 1868–c.1908), transmitted orally through the Mankin and Hirst lines to Marie Hirst Yochim, and first fixed in print by her nephew, historian Melvin L. Steadman Jr. in 1964.

  **Implications for reliability:** Because the testimony is confined to a single kin group with a clear incentive to highlight an early founding date, it lacks independent corroboration and may be subject to memory distortion or embellishment. No third-party 19th- or early-20th-century observer records seeing the purported brick, and an earlier chronicler (Stewart 1904) expressly dating the house to the Revolutionary era did not mention it.

  **Translation to prior parameters:** Following template guidance, a lone, biased oral report warrants a *low* mean probability and *low weight*. Beta(1,14) gives a mean ≈ 0.067 and a wide 95 % CI (~0.001–0.30), allowing future archaeological data to dominate while still acknowledging a non-zero chance the brick existed.

  **Regional transferability:** This evidence does not speak to prevalence of date inscriptions broadly, only to the credibility of this *particular* reported inscription. Therefore it applies exclusively to Factor V in the Falls Church model and carries no weight for other regions.

  **Limitations and future data needs:**
  - Relies on secondary obituary and genealogical compilations rather than primary diaries or demolition records.
  - Absence of independent witnesses is suggestive but not conclusive; discovery of demolition photographs or salvage records could revise this assessment.
  - Additional oral histories from non-family contemporaries could either corroborate or further weaken the claim.
---
### Summary

Genealogical research demonstrates that the "1699" datestone story traces **exclusively** to the Lynch family that owned *Big Chimneys* (1868–c.1908) and their descendants. Marie Hirst Yochim—granddaughter of owner Ann (Lynch) Mankin—proudly repeated the claim and was the aunt of local historian **Melvin L. Steadman Jr.**, who first published it in 1964. No independent 19th-century source mentions such an inscription, and Charles A. Stewart's 1904 history, based on interviews with John Lynch, dates the house only to "Revolutionary times."

Because the report emanates from a single kin network with a vested interest in an early founding date, its evidentiary value is weak. Encoding this as Beta(1,14) reflects both the low likelihood that the brick ever existed (mean ≈ 6.7 %) and the high uncertainty due to lack of corroboration. This conservative prior ensures that subsequent physical or archival discoveries would substantially update the probability of Factor V, while the current testimonial alone contributes little weight to the overall chain-rule estimate. 