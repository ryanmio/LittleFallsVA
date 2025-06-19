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

### Phase 1: Run Analysis Scripts
- [ ] **accuracy_usage/accuracy_stats.py** – Core accuracy metrics
- [ ] **accuracy_usage/extended_accuracy_stats.py** – Extended accuracy analysis
- [ ] **cost_stats/cost_stats.py** – Cost analysis (Ensemble vs baselines)
- [ ] **time_stats/time_stats.py** – Latency analysis (include per-call breakdown for Ensemble)
- [ ] **token_stats/token_stats.py** – Token usage analysis (Ensemble only)
- [ ] **tool_usage_stats/tool_usage_stats.py** – Tool call analysis (Mortecai + Ensemble)
- [ ] **human_gis_benchmark/human_gis_benchmark.py** – Human baseline comparison (optional)
- [ ] **method_stats_promptA/method_stats_promptA.py** – Method comparison with new methods
- [ ] **length_stratification/length_stratification.py** – Length vs accuracy analysis

### Phase 2: Generate Updated Figures
- [ ] **figures/plot_violin_methods.py** – Error distribution violin plot (add four methods)
- [ ] **figures/plot_accuracy_bar.py** – Accuracy bar chart with CIs
- [ ] **figures/plot_pareto.py** – Cost-accuracy Pareto frontier (highlight new methods)
- [ ] **figures/plot_pareto_latency.py** – Latency-accuracy Pareto frontier
- [ ] **figures/plot_latency_box.py** – Processing time distribution (Ensemble vs others)
- [ ] **figures/plot_error_boxplot.py** – Error distribution boxplot
- [ ] **figures/plot_cdf_models.py** – CDF curves with new methods
- [ ] **figures/plot_tool_calls.py** – Tool usage stacked bar chart (Mortecai, Ensemble)
- [ ] **figures/plot_cost_accuracy.py** – Cost vs accuracy scatter plot

### Phase 3: Update Paper Tables and Text
- [ ] **Add method descriptions** – Section 4.x for each new method
- [ ] **Update accuracy table** – Include new performance metrics
- [ ] **Update cost table** – Ensemble cost per grant and total
- [ ] **Update latency table** – Include Ensemble latency breakdown
- [ ] **Update abstract** – Mention improved Ensemble results
- [ ] **Update introduction** – Reference new baselines and their roles
- [ ] **Update results summary** – Highlight comparative performance
- [ ] **Update discussion** – Implications of Ensemble & Mortecai performance
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