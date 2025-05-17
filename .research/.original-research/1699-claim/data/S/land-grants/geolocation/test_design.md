# Experimental Design: AI-Assisted Geolocation of Colonial-Era Virginia Land Grants

## 1  Objectives & Research Questions

Colonial land-grant books contain thousands of terse place descriptions that have **never** been geocoded.  Mapping them would open new lines of inquiry on early-eighteenth-century settlement diffusion, river-borne trade, and the origins of many modern towns.  Manually locating every grant is prohibitively slow, so we test whether recent OpenAI language-and-reasoning models can *infer* reasonable latitude/longitude coordinates directly from the text.

Research questions

1. How accurate are different model families and prompt/tool pipelines when asked to geolocate a grant description?  (distance error distribution)
2. How do monetary cost and latency trade off against that accuracy?
3. Does adding a geocoding tool (LLM → Google Maps API) improve performance over pure one-shot prompting?
4. How do the best AI methods compare to a **professional human GIS baseline** in both error and cost?
5. Which methods (human or AI) lie on the cost-accuracy Pareto frontier?

Because no public or private dataset contains coordinates for these grants (including the Northern Neck volumes we will also sample), strong performance would indicate genuine spatial reasoning rather than memorisation.

## 2  Corpus & Validation-File Protocol
| File | Description |
|------|-------------|
| `books9-14.csv` | All extracted grants (≈6 500 rows) – **source of samples only**. |
| `split_books9-14.csv` | Same as above with an added column `set ∈ {dev,test}` (stratified random 20 %-80 % split, seeded). |
| `validation-dev-A.csv` | ~300 randomly chosen *dev* rows for prompt/tool tuning. |
| `validation-dev-B.csv` | (Optional) independent dev replicate. |
| `validation-test.csv` | ~1 000 *test* rows, **held-out** for final reporting. |

### Manual Geolocation
Because only ~10 % of entries can be confidently located by hand:
1. Investigators manually geolocate as many rows in each validation file as possible (open-source maps, historical atlases, etc.).
2. Rows still lacking verified coordinates are retained **but flagged** with `has_ground_truth = 0`.
3. During evaluation, metrics are computed **only** on rows where `has_ground_truth = 1`; others are ignored but still logged for transparency.

This strategy maximises sample size while avoiding biased deletion of hard cases.

## 3  Method Catalogue
| Method ID | Model | Prompt / Pipeline | Tool Access | Output File | Status |
|----------|-------|-------------------|-------------|-------------|--------|
| **M-1** | `o4-mini-2025-04-16` | One-shot DMS | ‑ | `validation_results_M1.csv` | Not run |
| **M-2** | `o3-2025-04-16` | One-shot DMS | ‑ | `validation_results_M2.csv` | Not run |
| **M-3** | `o3-mini-2025-01-31` | One-shot DMS | ‑ | `validation_results_M3.csv` | Not run |
| **M-4** | `gpt-4.1-2025-04-14` | One-shot DMS | ‑ | `validation_results_M4.csv` | Not run |
| **M-5** | `chatgpt-4o-latest` | One-shot DMS | ‑ | `validation_results_M5.csv` | Not run |
| **M-6** | `gpt-3.5-turbo` | One-shot DMS | ‑ | `validation_results_M6.csv` | Not run |
| **T-1** | `o4-mini-2025-04-16` | Tool-chain (AI extracts location → Google API queries with retry, low reasoning) | ✅ | `validation_results_T1.csv` | Not run |
| **T-2** | `o3-2025-04-16` | Tool-chain (low reasoning) | ✅ | `validation_results_T2.csv` | Not run |
| **T-3** | `o3-mini-2025-01-31` | Tool-chain (low reasoning) | ✅ | `validation_results_T3.csv` | Not run |
| **T-4** | `gpt-4.1-2025-04-14` | Tool-chain | ✅ | `validation_results_T4.csv` | Not run |
| **T-5** | `chatgpt-4o-latest` | Tool-chain | ✅ | `validation_results_T5.csv` | Not run |
| **H-1** | *Human GIS freelancer* | Manual geocoding | ‑ | `validation_results_H1.csv` | Not run |

**One-shot DMS**: single prompt asks the LLM to output DMS coordinates directly.  **Tool-chain**: prompt instructs LLM to create structured location + iterative Google Geocoding calls (max 3) before returning chosen coordinates.

**Human manual baseline (H-1)**: coordinates supplied by an independent GIS professional.  We log their total cost (fixed project fee) and the time billed as "latency".  No model calls are involved; results are imported as a static CSV.

## 4  Metrics
1. Haversine **Distance Error** (km).
2. **Accuracy Bands**: <1 km (High); 1-10 km (Medium); >10 km (Low).
3. **Cost** (USD): token cost + $0.005 per Google request.
4. **Latency** (wall-clock s).
5. **Success Rate**: percentage of rows with parseable coordinates.

## 5  Experimental Procedure
1. **Dataset preparation** (`make datasets`):
   - Reproducibly split `books9-14.csv` into dev/test (seed=42) → `split_books9-14.csv`.
   - Sample specified counts to create validation files; add `has_ground_truth` default 0.
2. **Manual Annotation**: researchers populate lat/long & flip `has_ground_truth` to 1 where verified.
3. **Development Phase**: run any subset of methods on *dev* validation sets for prompt/tool tuning.
4. **Lock Prompts & Code**.
5. **Final Runs**: execute each trial on `validation-test.csv` using `--final` flag (script will refuse if prompts changed after lock SHA).
6. **Logging**: each call appended as JSON to `runs/{trial}/{date}.jsonl` with request/response, tokens, cost, latency, fingerprint.

## 6  Statistical Analysis Plan
Paired analyses use only rows with ground-truth across both methods being compared.

| Hypothesis | Test | α-adj | Notes |
|------------|------|-------|-------|
| Mean error reduction vs M-1 | Wilcoxon signed-rank | 0.006 | Bonferroni (9 comparisons) |
| Median cost difference | Wilcoxon | ‑ |  |
| Accuracy-cost slope | OLS regression | 0.05 | tokens as covariate |

## 7  Reproducibility
*Dependencies*: `openai==1.16.x`, `python-dotenv`, `googlemaps==4.10.0`, Python 3.11.

Provide:
• `Dockerfile`, `requirements.txt`, `Makefile` (targets: datasets, dev-run, final-run, analyse).
• `.env.example` (no secrets).
• SHA of each prompt file stored; script aborts if SHA mismatch on final run.

## 8  Ethical & Practical Considerations
• Colonial context; include interpretive note in manuscript.
• Respect Google Maps TOS; no bulk caching.
• Abort run if projected spend exceeds $50.

## 9  Deliverables
1. Result CSVs per method (see table §3).
2. `analysis.ipynb` generating figures & stats.
3. ArXiv manuscript (Methods, Results, Discussion, Appendices with full prompts & code).