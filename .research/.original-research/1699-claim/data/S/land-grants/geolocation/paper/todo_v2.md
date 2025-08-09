# Multi-Method Integration Todo List (Ensemble, County Centroid, Mortecai, Name-Redacted Ablation)

## Integration Status: 🚀 PHASE 1 – IN PROGRESS
- [x] **Phase 0 completed** – Data prepared and merged into `full_results.csv`; sanity checks passed

### Phase 0: Data Preparation
- [x] **Generate predictions** – Run the evaluation pipeline for:
  - Ensemble (o3_ensemble5 DBSCAN)
  - County Centroid baseline
  - Mortecai (historical gazetteer)
  - Name-Redacted Ablation test
- [x] **Merge into `full_results.csv`** – Append all four methods' predictions and metadata
- [x] **Sanity checks** – Validate coordinate formats, method names, and unique identifiers

### Phase 0-b: Update Name-Redacted Ensemble (low-effort rerun)
- [x] **Generate NEW predictions** – Re-run `o3_ensemble5_redact` with `reasoning_effort: low`
- [x] **Merge into `full_results_v2.csv`** – Replace old redacted rows, keep other methods
- [x] **Sanity checks** – Confirm method_id matches, coordinates valid, row counts intact

### Phase 1: Run Analysis Scripts
- [x] **accuracy_usage/accuracy_stats.py** – Core accuracy metrics updated
- [x] **accuracy_extended/extended_accuracy_stats.py** – Extended accuracy analysis
- [x] **cost_analysis/cost_stats.py** – Cost analysis (Ensemble vs baselines)
- [x] **time_usage/time_stats.py** – Latency analysis (include per-call breakdown for Ensemble)
- [x] **token_usage/token_stats.py** – Token usage analysis (Ensemble only)
- [x] **tool_usage/tool_usage_stats.py** – Tool call analysis (Mortecai + Ensemble)
- [x] **method_stats/method_stats_promptA.py** – Method comparison with new methods
- [x] **length_stratification/length_stratification.py** – Length vs accuracy analysis
- [x] **wilcoxon_tests/wilcoxon_tests.py** – Wilcoxon signed-rank tests (pairwise)
- [x] **bootstrap_CI/bootstrap_ci.py** – Bootstrap confidence intervals
- [x] **outlier_analysis.py** – Outlier case study tables/figures

### Phase 2: Generate Updated Figures
- [x] **figures/plot_violin_methods.py** – Error distribution violin plot (add four methods)
- [x] **figures/plot_accuracy_bar.py** – Accuracy bar chart with CIs
- [x] **figures/plot_pareto.py** – Cost-accuracy Pareto frontier (highlight new methods)
- [x] **figures/plot_pareto_latency.py** – Latency-accuracy Pareto frontier
- [x] **figures/plot_latency_box.py** – Processing time distribution (Ensemble vs others)
- [x] **figures/plot_error_boxplot.py** – Error distribution boxplot
- [x] **figures/plot_cdf_models.py** – CDF curves with new methods
- [x] **figures/plot_tool_calls.py** – Tool usage stacked bar chart (Mortecai, Ensemble)
- [x] **figures/plot_cost_accuracy.py** – Cost vs accuracy scatter plot

### Phase 3: Update Paper Tables and Text
- [x] **Add method descriptions** – Section 4.x for each new method
- [x] **Update accuracy table** – Include new performance metrics
- [x] **Update cost table** – Ensemble cost per grant and total
- [x] **Update latency table** – Include Ensemble latency breakdown
- [x] **Update abstract** – Mention improved Ensemble results
- [-] **Update introduction** – Reference new baselines and their roles
- [x] **Update results summary** – Highlight comparative performance
- [x] **Update discussion** – Implications of Ensemble & Mortecai performance
- [ ] **Update conclusion** – Broaden takeaway with new methods
- [ ] **Review figure captions** – Ensure new methods properly labeled
- [ ] **Update method count** – Increment to reflect total methods in study

### Phase 4: Quality Assurance
- [ ] **Cross-check all numbers** – Consistency between tables, figures, text
- [ ] **Verify confidence intervals** – Recompute if needed
- [ ] **Validate cost calculations** – Ensemble token accounting
- [ ] **Check method ordering** – Ensure rankings updated consistently
- [ ] **Proofread new sections** – Clarity and consistency

### Phase 5: Final Integration
- [ ] **Run complete paper build** – Generate final PDF with all updates
- [ ] **Full read-through** – Proofread entire manuscript for coherence
- [ ] **Repository update** – Commit code/data reflecting new methods
- [ ] **Final validation** – Confirm metrics and references are correct

## NOTES:
- Ensemble (o3_ensemble5 DBSCAN) currently outperforms TTC variant – keep TTC results archived but not highlighted
- County Centroid serves as deterministic low-effort baseline
- Mortecai leverages historical gazetteer; may require additional disclosures
- Name-Redacted Ablation tests sensitivity to toponym removal
- All analysis scripts should now source exclusively from `full_results.csv` 