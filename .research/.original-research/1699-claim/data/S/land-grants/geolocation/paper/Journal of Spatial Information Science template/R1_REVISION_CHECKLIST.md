# R1 Revision Checklist
## JOSIS Manuscript: "Benchmarking Large Language Models for Geolocating Colonial Virginia Land Grants"

---

## Editor-in-Chief (4 items)

### Major Themes
- [x] **E1:** Better embed the work in current literature
  - Changes: Added concise positioning in §1.2 (vs. GeoTxt/Mordecai/CamCoder), benchmark context in §2.2 (GeoCorpora/WikToR task mismatch), and tool‑augmented alignment in §2.3 (relation to GeoAgent/GeoGLUE); minimal prose, no duplication. Commit: 6816de4.

- [x] **E2:** Add references to corpora and tools listed in text
  - Changes: Inserted canonical citations for the above corpora/tools at their first mentions; ensured they compile in the JOSIS build. Commit: aed55252.

- [x] **E3:** Discuss limitations: study limited to ChatGPT models, sample relatively small
  - Changes: Added an explicit model-family scope limitation in §8 (OpenAI GPT/o‑series only) and kept the small evaluation set caveat prominent; numbering adjusted without inflating length. Commit: e637595.

- [ ] **E4:** Reconsider if sections 14-16 are crucial for main message or make paper too long/hard to read
  - Changes: 

---

## Reviewer A (24 items)

### Major Issues
- [x] **A1:** Reference Huang et al is missing (p.5)
  - Changes: Confirmed and retained `@Huang2024_geoagent` citation in §2.3; no remaining placeholder. Commit: aed55252.

- [ ] **A2:** Include example of grant description early in introduction (or reference to one)
  - Changes: 

- [x] **A3:** Add literature references for tools/corpora mentioned without citations (GeoCorpora, WikToR, GeoLingit, GeoGlue, GeoText, etc.)
  - Changes: Added citations for GeoCorpora (IJGIS 2017), WikToR (LRE 2018), GeoGLUE (arXiv 2305.06545), and geocoders (GeoNames/Nominatim/ArcGIS) at first mention (§2.2–§2.3). Commit: aed55252.

- [ ] **A4:** Clarify reasons for small test data set (43 instances) - how was number decided?
  - Changes: 

- [x] **A5:** Acknowledge limitation that study is limited to ChatGPT models, not other LLMs
  - Changes: Added concise OpenAI-only scope rationale in §8 (controls cross‑provider confounders; preserves internal validity); kept generalization note. Commits: 8acc5a7, aff8d40.

- [x] **A6:** Bibliography is comparatively short - add more references where possible
  - Changes: Added citations for GeoCorpora (IJGIS 2017), WikToR (LRE 2018), GeoGLUE (arXiv 2305.06545), and geocoders (GeoNames/Nominatim/ArcGIS) at first mention (§2.2–§2.3). Commit: aed55252.

- [ ] **A7:** Consider moving Sections 14-16 to web repository to reduce paper length
  - Changes: 

### Section Structure & Formatting
- [x] **A8:** Use "Section ..." consistently instead of § symbol
  - Changes: Normalized remaining § references in main text to “Section …” near related-work inserts and tool-usage sections. Commit: 5fc2e87.

- [ ] **A9:** Section 4: Switch order of 4.3 and 4.4, or put 4.4 before 4.2
  - Changes: 

- [ ] **A9b:** Add a one-sentence transition when you reorder §4 subsections so the flow reads naturally.
  - Changes: 

- [x] **A10:** Section 4.5: Explain meaning of temperature parameter in context of LLMs
  - Changes: Added concise definition of temperature at first implementation mention (Setup §5.2 paragraph); referenced §6.6 ablation. Commit: 4e58320.

- [x] **A11:** Remove stray ~ in table/figure references; standardize formatting.
  - Changes: Verified non‑breaking tilde usage limited to LaTeX captions where appropriate; no stray tildes remain in prose references. Commit: 5fc2e87.

- [x] **A12:** Section 4.6: Inconsistent - no performance outlook (unlike other subsections)
  - Changes: Appended one‑sentence performance outlooks to end of 4.5 (M‑series) and 4.6 (T‑series) paragraphs, pointing to Section 6 tables/figures without duplicating numbers. Commit: 29a4070.

- [x] **A13:** Beginning of section 5 is redundant with previous section - consolidate
  - Changes: Removed duplicated efficiency bullets/paragraph from §5.1 and replaced with a single reference to Cost and Latency Accounting; preserves definitions in §4.8 without repetition. Commit: 6fab2ae.

### Tables & Figures
- [x] **A14:** Section 6.1: Figure 4 only mentioned briefly - clarify what can be learned from it
  - Changes: Defined CDF at first mention and added two interpretive sentences explaining near‑field vs tail behavior and threshold‑dependent dominance. Commit: 846ef4b.

- [x] **A15:** Section 6.2: No reference to Table 6 in text - add reference
  - Changes: Added explicit reference to Table \ref{tbl:cost} in 6.2 paragraph discussing the Pareto cost–accuracy plot. Commit: 7dc04f1.

- [x] **A16:** Choose one cost normalization (per-grant or per-1,000), justify, and align table + prose.
  - Changes: Standardized Table 6 to per‑1,000 located grants, simplified columns and caption, and aligned 6.2 text to per‑1,000 normalization. Commit: 7dc04f1.

- [x] **A17:** Figure 6 H# column – populate with values and explain, or remove.
  - Changes: Removed static H‑series baselines from the per‑grant latency figure by filtering pipeline == static in the plotting script; regenerated and synced figure. Commit: 048e467.

- [x] **A18:** Section 6.4: Table reference should be "Table 7", table is lacking number + caption
  - Changes: Added caption and label to qualitative steps table in §6.4 — “Table: Qualitative step‑by‑step comparison… {#tbl:grant04_steps}”. Commit: 7b2ebe3.

- [x] **A19:** Section 6.5: Rounding of numbers in text is odd (compare to numbers in table)
  - Changes: Synchronized §6.5 narrative with Table \ref{tbl:tooluse}: T‑4 uses 2.23 calls/grant with 72.1% first‑call success; T‑1 uses 3.98 calls with 66.7% success; corrected model naming. Commit: 2a30fc7.

- [ ] **A20:** Figure 8: Color of triangle in map does not match legend
  - Changes: 

- [x] **A21:** Figure 8: Not referenced in text - add reference
  - Changes: Added a lead sentence explicitly referencing Figure \ref{fig:grant_maps} before the Grant 1/19 narrative in §6.4, framing the pair as representative success/failure cases. Commit: 26a8bfb.

### Appendix Issues
- [ ] **A7b:** Put cut sections in repo and cite the repo with a stable tag so the editor sees nothing was "lost," just moved.
  - Changes: 
- [ ] **A22:** Several references to "appendix" but only 16.5.1 labeled as appendix - resolve inconsistency
  - Changes: 

---

## Reviewer B (4 items)

### Major Requirement
- [x] **B1:** All table and figure captions need to be more descriptive with context
  - Changes: Revised captions across main text and appendices to state purpose and how to read each artifact (not restating columns or results). Added concise first‑mention takeaways in §6.1 and fixed figure reference mismatch in §6.3. Commits: 9a738a2, b692b3c, d3d0e81, 51ec750, 9394196, dbda28a, 3276d8d.

### Optional/Minor
- [ ] **B2:** [OPTIONAL] Consider adding Google geoparsing pipeline comparison (spatial reasoning AI + geocoding)
  - Changes: 

- [ ] **B3:** [ACKNOWLEDGED] Small evaluation dataset limitation - already noted but reviewer emphasizes
  - Changes: 

- [ ] **B4:** [ACKNOWLEDGED] No polygon-level reconstruction - already noted as future work
  - Changes: 

---

## Reviewer C (17 items)

### References & Formatting
- [x] **C1:** Page 5: "Huang et al. [?]" reference error - fix
  - Changes: Resolved by using `@Huang2024_geoagent` and verifying compile; no stray "[?]" remains. Also normalized “et al.” spacing before bracketed citations with a nonbreaking space to avoid visual double gaps. Commits: aed55252, 1ec066d.

- [x] **C2:** Normalize citation spacing – use non-breaking spaces in citations (e.g., Li et al.~[5]); remove stray ~ elsewhere.
  - Changes: Standardized author–year spacing and converted visible “Table~#” cases to “Table #” in prose; retained LaTeX non‑breaking tildes only where appropriate (captions/labels). Commit: 4bc626d.

- [x] **C3:** Page 11: "geocode_place" - check if backslash is copy/paste error in typesetting
  - Changes: Confirmed underscore is correctly rendered as code or plain text; no stray escape backslashes remain in narrative text. Commit: 5fc2e87, b566ce3.

- [x] **C4:** Page 12: What is "[H]" - maybe supposed to be a LaTeX command?
  - Changes: [H] is intentionally used for figure/table floats per JOSIS build; confirmed not used in prose; no correction needed beyond verification. Commit: 5fc2e87.

- [x] **C5:** Page 21: "WILLIAM WILLIAMS" has unbalanced quote characters
  - Changes: Removed stray quote. Commit: 6b98c0e.

### Phrasing & Language
- [ ] **C6:** Page 7: Revise phrasing of models' "cognitive processes" - be less credulous
  - Changes: 

- [ ] **C7:** Page 21: Very skeptical of phrasing "All cognition is 'in the head' of the network: it interprets archaic toponyms, performs mental triangulation against its latent world map..."
  - Do we know this is true? Revise to be more cautious about claims of what LLM "does"
  - Changes: 

### Clarifications & Details
- [ ] **C8:** Page 9: Having one human is a source of variance - discuss
  - Changes: 

- [ ] **C9:** Page 10: How often did H-2 fall back to Virginia's geographic center? Would pull up average
  - Changes: 

- [x] **C10:** Briefly justify temperature where it is first introduced; add forward reference to detailed discussion if needed.
  - Changes: Clarified t as sampling randomness, noted default (0.2) when supported and that o‑series does not expose temperature; added forward reference to §6.6. Commit: 4e58320.

- [x] **C11:** Page 12, re: DBSCAN: Clarify - is that basically MinPts=3?
  - Changes: Clarified ensemble clustering as DBSCAN with ε = 0.5 km and MinPts = 3 in the Five‑call Ensemble description, Discussion §7.1 and §7.3 language, and Conclusion. Commit: ad3e7430ab5b93c79171b264b1afedb84882d5dc.

- [x] **C12:** Clarify what 'script development time' includes and whether subsequent grants would be faster.
  - Changes: Added brief clarification in §4.8 that script development time covers ingestion/tuning/QA; costs amortize over larger batches and LLMs scale linearly. Commit: 6fab2ae.

- [ ] **C13:** Page 14: Mean column hard to read - adjust column widths (make other columns less wide)
  - Changes: 

### Positive Sections (No Action)
- [ ] **C14:** [POSITIVE] Section 6.2's cost/quality Pareto front discussion is nice
  - Changes: N/A - reviewer praise

- [ ] **C15:** [POSITIVE] Section 6.6 ablation study is nice
  - Changes: N/A - reviewer praise

- [ ] **C16:** [POSITIVE] Section 7.2 "Error Analysis & Failure Modes" is good
  - Changes: N/A - reviewer praise

- [ ] **C17:** [ACKNOWLEDGED] Result that LLMs work well is "unsatisfying" but report is thorough
  - Changes: N/A - general comment

---

## Global Sweeps (7 items)

### Cross-cutting Quality Checks
- [x] **G1:** Descriptive captions pass – each figure/table states what it shows and why it matters; ensure in-text references near first mention.
  - Changes: Added one‑line takeaways at first mention for §6.1 figures; clarified captions for cost/latency figures and all appendix tables/figures; ensured consistent labels and references. Commits: 9a738a2, b692b3c, d3d0e81, 51ec750, 9394196, dbda28a, 3276d8d.

- [ ] **G2:** Ensure appendix vs numbered sections are consistent.
  - Changes: 

- [ ] **G3:** Numbering/labels – every figure/table has a number + caption; fix mismatches (e.g., "Table 7").
  - Changes: 

- [ ] **G4:** Rounding/units – harmonize rounding between prose and tables; apply chosen cost unit consistently.
  - Changes: 

- [ ] **G5:** Typesetting artifacts – resolve [H], geocode\\_place backslash, large spaces, legend color mismatches, empty H# columns.
  - Changes: 

- [ ] **G6:** Figure references – ensure all figures mentioned (incl. Figure 4 and 8) are referenced with a one-line takeaway.
  - Changes: 

- [ ] **G7:** First-mention placement – ensure each figure/table is referenced with a one-line takeaway at first mention and appears after that mention. This operationalizes B1 and G6.
  - Changes: 

---

## Summary Counts
- **Total Items:** 56
- **Editor:** 4
- **Reviewer A:** 24
- **Reviewer B:** 4 (1 major, 3 optional/minor)
- **Reviewer C:** 17 (13 actionable, 4 positive/acknowledged)
- **Global Sweeps:** 7

---

## Revision Strategy Notes
1. **Priority 1:** Editor's main themes (E1-E4) and Reviewer B's caption requirement (B1)
2. **Priority 2:** All reference/citation fixes (A1, A3, C1, C2) and figure/table issues
3. **Priority 3:** Language/phrasing improvements (C6, C7) and structural improvements
4. **Priority 4:** Minor formatting and clarifications

## R1 Submission Requirements (per Judith's email)
Submit THREE items:
1. **Plain revised manuscript** → `article.pdf` (non-blind, with author name)
2. **Highlighted changes version** → `diff_article.pdf` (shows what changed from v0 to v1)
3. **Response letter** → Document addressing each reviewer comment with manuscript changes noted

**Note:** R1 revisions are NOT blind - reviewers already know who you are.

## Workflow
1. **First time:** Run `./build.sh` → automatically creates baselines in `