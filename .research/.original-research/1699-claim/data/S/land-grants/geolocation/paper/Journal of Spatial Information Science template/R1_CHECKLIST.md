# JOSIS R1 Revision Checklist

## Workflow Instructions

1. **Make edits**: Edit LaTeX sources on `r1-revisions` branch
2. **Build**: Run `./build.sh` to generate both:
   - `article_blind.pdf` (clean revised version)
   - `diff_article_blind.pdf` (tracked changes from v1.0.0)
3. **Commit**: Small, topical commits with tags like `refs(A):`, `refs(B):`, `refs(C):`, `editor:`, `global:`
4. **Update checklist**: After committing, mark `[x]` and add Location + commit hash
5. **Iterate**: Continue until all items are `[x]`

---

## Status at a Glance

- **Total items**: 47
- **Open**: 47
- **In Progress**: 0
- **Done**: 0

---

## Editor Comments

- [ ] **ED-1**: Better embed the work in current literature and add references to listed corpora and tools (GeoCorpora, WikToR, GeoLingit, GeoGlue, GeoText, etc.)
  - Location: 
  - Linked commit(s): 

- [ ] **ED-2**: Discuss limitations regarding study being limited to ChatGPT models (not including other LLMs) and relatively small sample size
  - Location: 
  - Linked commit(s): 

- [ ] **ED-3**: Reconsider if Sections 14-16 (Appendices A-E) are crucial for main message or should be moved to web repository to make paper less overwhelming
  - Location: 
  - Linked commit(s): 

---

## Reviewer A

### Major Issues

- [ ] **A-1**: Clarify reasons for using small test data set (43 instances) and whether larger number could have been used for automatic approaches
  - Location: 
  - Linked commit(s): 

- [ ] **A-2**: Acknowledge limitation that study is restricted to ChatGPT models and does not include other LLMs
  - Location: 
  - Linked commit(s): 

- [ ] **A-3**: Add literature references for tools and corpora mentioned without citations (GeoCorpora, WikToR, GeoLingit, GeoGlue, GeoText)
  - Location: 
  - Linked commit(s): 

- [ ] **A-4**: Consider moving Sections 14-16 (extensive appendices) to web repository to reduce paper length
  - Location: 
  - Linked commit(s): 

### Detailed Points

- [ ] **A-5**: Fix missing Huang et al. reference (p.5)
  - Location: 
  - Linked commit(s): 

- [ ] **A-6**: Include example of grant description early in introduction or reference to one appearing later
  - Location: 
  - Linked commit(s): 

- [ ] **A-7**: Replace § symbols with "Section ..." consistently throughout text
  - Location: 
  - Linked commit(s): 

- [ ] **A-8**: Reorder Section 4 subsections (switch 4.3 and 4.4, or put 4.4 before 4.2) for better logical flow
  - Location: 
  - Linked commit(s): 

- [ ] **A-9**: Explain meaning of temperature parameter in context of LLMs (Section 4.5)
  - Location: 
  - Linked commit(s): 

- [ ] **A-10**: Remove ~ symbols appearing with table references (e.g., Section 4.8)
  - Location: 
  - Linked commit(s): 

- [ ] **A-11**: Add performance outlook to Section 4.6 (inconsistent with other subsections)
  - Location: 
  - Linked commit(s): 

- [ ] **A-12**: Reduce redundancy between beginning of Section 5 and previous section
  - Location: 
  - Linked commit(s): 

- [ ] **A-13**: Expand discussion of Figure 4 in Section 6.1 to clarify what can be learned from it
  - Location: 
  - Linked commit(s): 

- [ ] **A-14**: Add text reference to Table 6 in Section 6.2 and reconsider listing both costs per individual grant and per 1000 requests
  - Location: 
  - Linked commit(s): 

- [ ] **A-15**: Address missing values for H# methods in Figure 6 or remove them from table
  - Location: 
  - Linked commit(s): 

- [ ] **A-16**: Fix table reference in Section 6.4 (should be "Table 7") and add missing number + caption
  - Location: 
  - Linked commit(s): 

- [ ] **A-17**: Fix inconsistent rounding of numbers in text of Section 6.5 compared to table values
  - Location: 
  - Linked commit(s): 

- [ ] **A-18**: Fix Figure 8 color mismatch (triangle color doesn't match legend) and add text reference
  - Location: 
  - Linked commit(s): 

- [ ] **A-19**: Resolve inconsistent "appendix" references in text (only 16.5.1 still labeled as appendix)
  - Location: 
  - Linked commit(s): 

---

## Reviewer B

- [ ] **B-1**: Make all table and figure captions more descriptive with context about what they show and why it matters
  - Location: 
  - Linked commit(s): 

---

## Reviewer C

### Major Issues

- [ ] **C-1**: Revise phrasing about models' "cognitive processes" (page 7) to be less credulous about what LLMs actually do
  - Location: 
  - Linked commit(s): 

- [ ] **C-2**: Revise problematic phrasing on page 21: "All cognition is 'in the head' of the network: it interprets archaic toponyms, performs mental triangulation..." - clarify what is actually known vs. speculative
  - Location: 
  - Linked commit(s): 

### Detailed Points

- [ ] **C-3**: Fix Huang et al. [?] reference error (page 5)
  - Location: 
  - Linked commit(s): 

- [ ] **C-4**: Fix large space after "Li et al. [5]" on page 6, section 2.4 line 4 - use ~
  - Location: 
  - Linked commit(s): 

- [ ] **C-5**: Address concern about single human baseline being source of variance (page 9)
  - Location: 
  - Linked commit(s): 

- [ ] **C-6**: Report how often H-2 fell back to Virginia's geographic center (page 10)
  - Location: 
  - Linked commit(s): 

- [ ] **C-7**: Mention reason for temperature choice early (page 11) even though discussed later
  - Location: 
  - Linked commit(s): 

- [ ] **C-8**: Fix "geocode\_place" backslash - appears to be copy/paste error in typesetting (page 11)
  - Location: 
  - Linked commit(s): 

- [ ] **C-9**: Clarify DBSCAN parameters on page 12 - confirm if MinPts=3
  - Location: 
  - Linked commit(s): 

- [ ] **C-10**: Fix "[H]" on middle of page 12 - appears to be broken LaTeX command
  - Location: 
  - Linked commit(s): 

- [ ] **C-11**: Clarify what "script development time" entails and whether further grants would be quicker to georeference (page 13)
  - Location: 
  - Linked commit(s): 

- [ ] **C-12**: Improve readability of mean column in table on page 14 by adjusting column widths
  - Location: 
  - Linked commit(s): 

- [ ] **C-13**: Fix unbalanced quote characters in "WILLIAM WILLIAMS) text (page 21)
  - Location: 
  - Linked commit(s): 

---

## Global Sweeps

These are cross-cutting issues that require systematic checking across the entire document:

- [ ] **G-1**: Replace all § symbols with "Section" consistently
  - Location: 
  - Linked commit(s): 

- [ ] **G-2**: Review all figure references to ensure they are mentioned in text with adequate discussion
  - Location: 
  - Linked commit(s): 

- [ ] **G-3**: Review all table references to ensure they are mentioned in text
  - Location: 
  - Linked commit(s): 

- [ ] **G-4**: Check all table and figure numbers/captions are present and correctly formatted
  - Location: 
  - Linked commit(s): 

- [ ] **G-5**: Standardize cross-reference formatting (use consistent spacing with ~)
  - Location: 
  - Linked commit(s): 

- [ ] **G-6**: Verify rounding consistency between text and tables throughout document
  - Location: 
  - Linked commit(s): 

- [ ] **G-7**: Perform spell check pass on entire manuscript
  - Location: 
  - Linked commit(s): 

- [ ] **G-8**: Review and enhance all captions to be more descriptive per Reviewer B
  - Location: 
  - Linked commit(s): 

- [ ] **G-9**: Ensure all mentioned tools/corpora have proper citations
  - Location: 
  - Linked commit(s): 

---

## Notes

**Priority groups:**
- **Critical fixes**: A-5, C-3 (missing reference), C-8, C-10, C-13 (typesetting errors)
- **High priority**: B-1 (all captions), C-1, C-2 (tone about LLM cognition), ED-1, A-3 (missing citations)
- **Medium priority**: Most A-series detailed points about tables/figures/sections
- **Strategic decision**: ED-3, A-4 (appendices - decide before making other changes)

**Commit message tags:**
- `refs(A):` - Reviewer A item
- `refs(B):` - Reviewer B item  
- `refs(C):` - Reviewer C item
- `editor:` - Editor request
- `global:` - Cross-cutting sweep

