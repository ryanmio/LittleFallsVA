# R1 Revision Checklist
## JOSIS Manuscript: "Benchmarking Large Language Models for Geolocating Colonial Virginia Land Grants"

**Status:** 0 of 56 items completed

---

## Editor-in-Chief (4 items)

### Major Themes
- [ ] **E1:** Better embed the work in current literature
  - Changes: 

- [ ] **E2:** Add references to corpora and tools listed in text
  - Changes: 

- [ ] **E3:** Discuss limitations: study limited to ChatGPT models, sample relatively small
  - Changes: 

- [ ] **E4:** Reconsider if sections 14-16 are crucial for main message or make paper too long/hard to read
  - Changes: 

---

## Reviewer A (24 items)

### Major Issues
- [ ] **A1:** Reference Huang et al is missing (p.5)
  - Changes: 

- [ ] **A2:** Include example of grant description early in introduction (or reference to one)
  - Changes: 

- [ ] **A3:** Add literature references for tools/corpora mentioned without citations (GeoCorpora, WikToR, GeoLingit, GeoGlue, GeoText, etc.)
  - Changes: 

- [ ] **A4:** Clarify reasons for small test data set (43 instances) - how was number decided?
  - Changes: 

- [ ] **A5:** Acknowledge limitation that study is limited to ChatGPT models, not other LLMs
  - Changes: 

- [ ] **A6:** Bibliography is comparatively short - add more references where possible
  - Changes: 

- [ ] **A7:** Consider moving Sections 14-16 to web repository to reduce paper length
  - Changes: 

### Section Structure & Formatting
- [ ] **A8:** Use "Section ..." consistently instead of § symbol
  - Changes: 

- [ ] **A9:** Section 4: Switch order of 4.3 and 4.4, or put 4.4 before 4.2
  - Changes: 

- [ ] **A9b:** Add a one-sentence transition when you reorder §4 subsections so the flow reads naturally.
  - Changes: 

- [ ] **A10:** Section 4.5: Explain meaning of temperature parameter in context of LLMs
  - Changes: 

- [ ] **A11:** Remove stray ~ in table/figure references; standardize formatting.
  - Changes: 

- [ ] **A12:** Section 4.6: Inconsistent - no performance outlook (unlike other subsections)
  - Changes: 

- [ ] **A13:** Beginning of section 5 is redundant with previous section - consolidate
  - Changes: 

### Tables & Figures
- [ ] **A14:** Section 6.1: Figure 4 only mentioned briefly - clarify what can be learned from it
  - Changes: 

- [ ] **A15:** Section 6.2: No reference to Table 6 in text - add reference
  - Changes: 

- [ ] **A16:** Choose one cost normalization (per-grant or per-1,000), justify, and align table + prose.
  - Changes: 

- [ ] **A17:** Figure 6 H# column – populate with values and explain, or remove.
  - Changes: 

- [ ] **A18:** Section 6.4: Table reference should be "Table 7", table is lacking number + caption
  - Changes: 

- [ ] **A19:** Section 6.5: Rounding of numbers in text is odd (compare to numbers in table)
  - Changes: 

- [ ] **A20:** Figure 8: Color of triangle in map does not match legend
  - Changes: 

- [ ] **A21:** Figure 8: Not referenced in text - add reference
  - Changes: 

### Appendix Issues
- [ ] **A7b:** Put cut sections in repo and cite the repo with a stable tag so the editor sees nothing was "lost," just moved.
  - Changes: 
- [ ] **A22:** Several references to "appendix" but only 16.5.1 labeled as appendix - resolve inconsistency
  - Changes: 

---

## Reviewer B (4 items)

### Major Requirement
- [ ] **B1:** All table and figure captions need to be more descriptive with context
  - Example: "Figure 1: Coordinate accuracy by method" → "Figure 1: The coordinate accuracy shows ... performing best with a mean error of ... [details]..."
  - Changes: 

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
- [ ] **C1:** Page 5: "Huang et al. [?]" reference error - fix
  - Changes: 

- [ ] **C2:** Normalize citation spacing – use non-breaking spaces in citations (e.g., Li et al.~[5]); remove stray ~ elsewhere.
  - Changes: 

- [ ] **C3:** Page 11: "geocode_place" - check if backslash is copy/paste error in typesetting
  - Changes: 

- [ ] **C4:** Page 12: What is "[H]" - maybe supposed to be a LaTeX command?
  - Changes: 

- [ ] **C5:** Page 21: "WILLIAM WILLIAMS" has unbalanced quote characters
  - Changes: 

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

- [ ] **C10:** Briefly justify temperature where it is first introduced; add forward reference to detailed discussion if needed.
  - Changes: 

- [ ] **C11:** Page 12, re: DBSCAN: Clarify - is that basically MinPts=3?
  - Changes: 

- [ ] **C12:** Clarify what 'script development time' includes and whether subsequent grants would be faster.
  - Changes: 

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
- [ ] **G1:** Descriptive captions pass – each figure/table states what it shows and why it matters; ensure in-text references near first mention.
  - Changes: 

- [ ] **G2:** Cross-reference normalization – replace § with "Section …"; ensure appendix vs numbered sections are consistent.
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
1. **First time:** Run `./build.sh` → automatically creates baselines in `_baseline/` directory
2. **Edit:** Update `main.md` with your revisions
3. **Build:** Run `./build.sh` → regenerates `article.tex` and `content.tex`, creates diff files automatically
4. **Review:** Check `diff_article.tex` and `diff_content.tex` to verify changes are correct
5. **Upload to Overleaf (optional):** Compile diff files there to see highlighted PDF
6. **Iterate:** Repeat steps 2-5 until all checklist items addressed
