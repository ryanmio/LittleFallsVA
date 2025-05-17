# Universal Context for All Analysis Prompts

The following points apply to **every** analysis task requested below.  Any AI agent executing a prompt should assume this context without it being restated:

* **Primary dataset** – `validation-RESULTS-CLEANED.csv` produced by the geolocation experiment driver.
* **Key columns**
  * `row_index` – unique integer for each grant in this run.
  * `method_id` – identifier (M-*, T-*, H-1) defined in *test_design.md*.
  * `pipeline` – one of `one_shot`, `tool_chain`, or `static` (human baseline).
  * `prediction` – model-returned coordinates (string).
  * `error_km` – numeric Haversine distance to ground truth (blank if ground truth missing or prediction unparseable).
  * `input_tokens`, `output_tokens`, `total_tokens` – token counts per call.
  * `latency_s` – wall-clock seconds per call.
  * `is_mock` – "1" for dry-run rows (should be 0 in final results).
  * `has_ground_truth` – available only in source eval CSV; all statistics **must** use rows where `has_ground_truth==1`.
  * `is_locatable` – 1 if the grant description contains sufficient location detail; analyses **must** filter to `is_locatable==1` (except specific sensitivity checks).

* **Cost model**
  * Token prices per model are in `pricing.yaml` (USD / 1 M tokens).  Cost = `input_tokens * in_rate + output_tokens * out_rate`.
  * Google Geocoding API calls cost **$0.005** each when `pipeline == tool_chain`.
  * Human baseline (H-1) carries a fixed one-time project fee recorded in the method parameters; do **not** add token cost for H-1.

* **Accuracy bands** – High < 1 km, Medium 1–10 km, Low > 10 km.
* **Statistical tests** – default to non-parametric paired Wilcoxon for distance errors and McNemar for success-rate deltas; apply Bonferroni correction where multiple comparisons occur.
* **File locations** – All artefacts (tables, plots) should be saved into a sibling `analysis/` directory unless otherwise noted.

---

## Prompt A – Per-Method Performance Table
Using the filtered dataset (`has_ground_truth==1` and `is_locatable==1`), build a Markdown table for every *method_id* containing: N rows, mean/median/25-th/75-th percentile error (km), accuracy-band shares, success-rate %, mean latency (s), token totals, estimated token cost, Google call count & cost, and fixed human cost (H-1 only).  Sort rows by mean error ascending.

---

## Prompt B – Pairwise Statistical Tests
For each pair of methods, compute paired error differences and apply Wilcoxon signed-rank (two-sided, Bonferroni-adjusted).  Also perform McNemar on success-rate differences.  Return a Markdown table with N pairs, median diff, test statistic, adjusted p-value; highlight significant cells.

---

## Prompt C – Cost–Accuracy Pareto Frontier Plot
Create a scatter plot of total estimated cost vs mean error (km) per method.  Annotate points with *method_id*, colour the Pareto-optimal frontier, grey out dominated methods, and provide a companion table of frontier members.

---

## Prompt D – Error Distribution Visuals
Produce box-and-violin plots (log-scaled y) of error grouped by (1) pipeline type and (2) individual method.  Show median and IQR, note sample sizes, and log scaling in captions.

---

## Prompt E – Latency vs Spend Trade-off
Plot mean latency (x) against cost per row (y) for each method with 95 % confidence ellipses.  Discuss which methods meet real-time (<5 s, <$0.05/row) thresholds.

---

## Prompt F – Robustness to Tool Access
Compare one_shot vs tool_chain variants of the same base model.  For each pair, run Wilcoxon on error, McNemar on success rate, and compute cost delta.  Summarise significance and magnitude of differences.

---

## Prompt G – Human GIS Benchmark Interpretation
Using `h-1.csv`, classify `accuracy` into High/Medium/Low/Unlocatable, compute their shares, mean/median human error where ground truth exists, and contrast with the best AI method.  Draft 2–3 interpretive sentences.

---

## Prompt H – Failure-Mode Analysis
List rows where **all** AI methods failed (no parseable coordinates).  Provide row_index, truncated raw_entry, and thematic reasons for difficulty.  Produce a short narrative summary.

---

## Prompt I – Sensitivity to Ground-Truth Availability
Repeat core metrics with and without ground-truth filtering; quantify changes in mean error, success rate, and cost per row.  Comment on robustness.

---

## Prompt J – Reproducibility Appendix Artefacts
Assemble for the appendix: prompt file SHAs, commit SHA, CLI flags, environment info, pricing.yaml contents.  Output as a Markdown appendix section titled "Reproducibility Checklist." 