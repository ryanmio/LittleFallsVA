# Response to Editor and Reviewers

**Manuscript:** Benchmarking Large Language Models for Geolocating Colonial Virginia Land Grants  

---

Dear Editor and Reviewers,

Thank you for the thoughtful and constructive reviews. We deeply appreciate the journal's volunteer model and the effort to secure three detailed reports.

Below we summarize the revisions and then respond point-by-point. All changes are visible in the tracked‐changes PDF generated with latexdiff (submitted alongside the clean revised manuscript).

---

## Summary of Substantive Revisions

We revised the manuscript to 1) better embed it in current literature, 2) explicitly scope limitations (OpenAI-only models, small N), and 3) streamline length by moving extended appendices to a public supplementary repository with stable tag. We also addressed all typesetting, figure/table, and reference issues and synchronized numbers across text and tables. A highlighted diff and plain PDF are provided per instructions.

---

## Editor-in-Chief

### E1. Embed work in current literature.
- **Change:** Added concise positioning in Section 1.2 (vs. GeoTxt/Mordecai/CamCoder), benchmark context in Section 2.2 (GeoCorpora/WikToR task mismatch), and tool-augmented alignment in Section 2.3 (relation to GeoAgent/GeoGLUE).

### E2. Add references to all corpora/tools cited.
- **Change:** Inserted canonical citations at first mention throughout Sections 2.2–2.3.

### E3. Discuss limitations – ChatGPT-only, small sample.
- **Change:** Added explicit scope limitation in Section 8 and kept small-N caveat prominent.

### E4. Consider trimming Sections 14–16.
- **Change:** Kept Appendix A in-paper; moved Extended Results (B) and Supplementary Figures (C) to a tagged public repository, with detailed in-paper stubs and links. We retained Appendix A in the manuscript because it is essential to understanding and reproducing the core methodology referenced in the main text. To address the editor’s request to trim Sections 14–16 while preserving transparency and reproducibility, we moved Extended Results (Appendix B) and Supplementary Figures (Appendix C)—which elaborate on robustness checks and additional visualizations not required for the main argument—to a tagged public repository.

---

## Reviewer A
We thank Reviewer A for thorough feedback on literature and tool citations, early orientation, dataset scope (n=43) and ChatGPT-only limitations, section ordering/terminology, and figure/table references, units, and rounding; each item is addressed below.

### A1. Missing "Huang et al." reference.
- **Change:** Resolved with @Huang2024_geoagent.

### A2. Include an example grant early.
- **Change:** Inserted a concise C&P example at the end of Section 1.1.

### A3/A6. Add citations for corpora/tools; bibliography short.
- **Change:** Added citations for GeoCorpora, WikToR, GeoGLUE, and geocoders at first mention.

### A4. Clarify small test set (n=43).
- **Change:** Added explanation in Sections 3.2–3.3 (random draw, archival vetting, deterministic seed).

### A5. Acknowledge ChatGPT-only scope.
- **Change:** Done in Limitations with rationale for internal validity and future expansion plans.

### A7. Consider moving long Sections 14–16.
- **Change:** Moved to supplement; kept succinct summaries in paper.

### A8. Use "Section …" not §.
- **Change:** Global replacement and cross-ref normalization.

### A9. Reorder Section 4 subsections for natural flow.
- **Change:** Reordered and added a one-sentence transition.

### A10. Explain temperature in §4.5.
- **Change:** Added brief definition and forward pointer to ablation.

### A11. Stray "~" in references.
- **Change:** Removed stray tildes in prose; kept non-breaking spaces where appropriate in cites.

### A12. §4.6 lacked outlook.
- **Change:** Added a concise outlook sentence aligned with §6.

### A13. Start of §5 redundant.
- **Change:** Consolidated to a single pointer; removed duplication.

### A14. Clarify what can be learned from Figure 4.
- **Change:** Defined the CDF at first mention and added two interpretive sentences explaining near‑field vs tail behavior and threshold‑dependent dominance.

### A15. Add explicit reference to Table 6.
- **Change:** Added an explicit reference to Table \ref{tbl:cost} in Section 6.2.

### A16. Choose one cost normalization.
- **Change:** Standardized to per‑1,000 located grants and aligned prose and table.

### A17. Figure 6 "H#" column.
- **Change:** Removed static H‑series baselines from the per‑grant latency figure.

### A18. 6.4 table numbering/caption.
- **Change:** Added a proper number and caption to the qualitative step‑by‑step table.

### A19. 6.5 rounding inconsistencies.
- **Change:** Synchronized narrative and table values; corrected model naming.

### A20. Figure 8 legend/marker color mismatch.
- **Change:** Standardized series colors and regenerated figures.

### A21. Figure 8 not referenced.
- **Change:** Added a lead sentence that explicitly references the figure.

### A7b. Put cut sections in repo with stable tag.
- **Change:** Implemented with tag R1‑supplement‑2025‑10‑23; in‑paper stubs cross‑link to the repository.

### A22. Appendix references inconsistent.
- **Change:** Replaced numbered supplementary sections with appendix sections and updated references in the text.

---

## Reviewer B
We thank Reviewer B for emphasizing descriptive, contextual captions and for suggestions regarding the Google pipeline comparison, the small dataset limitation, and polygon reconstruction; each item is addressed below.

### B1. Make captions descriptive with context.
- **Change:** Revised all figure/table captions to include purpose and how to read; added concise first-mention takeaways.

### B2. Optional Google end-to-end pipeline.
- **Change:** Added a Future Work note proposing a follow-on benchmark with rationale (proprietary/instability/engineering cost).

### B3. Small dataset limitation.
- **Change:** Strengthened rationale in Sections 3.2–3.3 (random draw, archival vetting, deterministic seed).

### B4. No polygon reconstruction.
- **Change:** No manuscript change; acknowledged as Future Work.

---

## Reviewer C
We thank Reviewer C for precise notes on references and typesetting, cautious phrasing about LLM "cognition," and methodological clarifications; each item is addressed below.

### C1. "Huang et al. [?]" error.
- **Change:** Fixed citation and compile.

### C2. Spacing in "Li et al.~[5]" – use non-breaking space; remove stray ~ elsewhere.
- **Change:** Normalized author–year spacing and limited visible "~" usage to where appropriate.

### C3. geocode_place backslash artifact.
- **Change:** Corrected code rendering and removed stray escapes.

### C4. "[H]" float specifier.
- **Change:** Removed stray [H] in manuscript body.

### C5. Unbalanced quote ("WILLIAM WILLIAMS").
-**Change:** Removed stray quote.

### C6–C7. Tone about LLM "cognition".
- **Change:** Rewrote to method-grounded terms; removed anthropomorphic language around "mental triangulation".

### C8. Single human – variance.
- **Change:** Clarified as illustrative lower bound in Section 4.1 and discussed generality in Section 8.7.

### C9. H-2 fallback frequency to Virginia centroid.
- **Change:** Inserted sentence stating 4/43 statewide-centroid defaults (~9.3%) in Section 4.3.

### C10. Why this temperature – mention earlier.
- **Change:** Added brief justification where first introduced and a pointer to Section 6.6.

### C11. DBSCAN – confirm MinPts.
- **Change:** Clarified ensemble clustering as ε = 0.5 km and MinPts = 3.

### C12. "Script development time" clarity.
- **Change:** Clarified inclusion (ingestion/tuning/QA) and amortization.

### C13. Mean column readability.
- **Change:** Adjusted table column widths to improve readability.

### C14. Positive – Section 6.2 cost/quality Pareto front.
- **No Change:** Appreciated; no changes required.

### C15. Positive – Section 6.6 ablation study.
- **No Change:** Appreciated; no changes required.

### C16. Positive – Section 7.2 error analysis and failure modes.
- **No Change:** Appreciated; no changes required.

### C17. Acknowledged – Result that LLMs work well is "unsatisfying" but report is thorough.
- **No Change:** We empathize with the reviewer's note. We hope this benchmark serves as a reproducible record which may inform future work on interpretable, specialized methods that can compete on this challenging task.

---

## Correction to Ensemble Statistics

During R1 preparation, we discovered the R0 manuscript contained stale ensemble statistics (E-1: 18.7 km, E-2: 20.4 km) from before we corrected locatability flags. The actual experimental data shows E-1: 19.2 km and E-2: 20.6 km. We inadvertently referenced the old statistics when drafting R0. All E-1/E-2 values in R1 now correctly match our actual experimental data. The corrections are minor (+0.5 km for E-1), do not affect our conclusions, and were verified by re-running all analysis scripts. We disclose this transparently as it changes headline numbers independent of reviewer feedback.

---

We submit two anonymized files as requested:

- Revised manuscript (clean) anonymized PDF.
- Revised manuscript (changes highlighted) anonymized latexdiff PDF.
- A point-by-point mapping is this letter.

Thank you for considering our revised submission.

Sincerely,  
The authors
