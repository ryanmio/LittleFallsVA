# H-2 Integration Todo List

## CRITICAL: Data Integration & Analysis Scripts

### Phase 1: Run All Analysis Scripts with New H-2 Data
- [x] **accuracy_usage/accuracy_stats.py** - Core accuracy metrics ✅ COMPLETED
- [x] **accuracy_extended/extended_accuracy_stats.py** - Extended accuracy analysis ✅ COMPLETED
- [x] **cost_analysis/cost_stats.py** - Cost efficiency analysis ✅ COMPLETED
- [x] **time_usage/time_stats.py** - Latency/timing analysis ✅ COMPLETED
- [x] **token_usage/token_stats.py** - Token consumption analysis ✅ COMPLETED
- [x] **tool_usage/tool_usage_stats.py** - Tool usage patterns ✅ COMPLETED
- [x] **human_gis_benchmark/human_gis_benchmark.py** - Human baseline analysis ✅ COMPLETED
- [x] **method_stats/method_stats_promptA.py** - Method comparison statistics ✅ COMPLETED
- [x] **length_stratification/length_stratification.py** - Length vs accuracy analysis ✅ COMPLETED

**STATUS: ✅ ALL PHASE 1 SCRIPTS COMPLETED SUCCESSFULLY**

### Phase 2: Generate Updated Figures
- [ ] **figures/plot_violin_methods.py** - Error distribution violin plot
- [ ] **figures/accuracy_bar.py** - Accuracy bar chart with confidence intervals
- [ ] **figures/pareto_tradeoff.py** - Cost-accuracy Pareto frontier
- [ ] **figures/latency_boxplot.py** - Processing time distribution
- [ ] **figures/error_boxplot.py** - Error distribution boxplot
- [ ] **figures/cdf_graphs/** - Cumulative distribution functions

### Phase 3: Update Paper Tables & Text

#### Tables Requiring H-2 Integration:
- [ ] **Table 4 (tbl:accuracy)** - Core accuracy metrics table
- [ ] **Table 5 (tbl:cost)** - Cost efficiency comparison  
- [ ] **Table 6 (tbl:tooluse)** - Tool usage patterns
- [ ] **Table 7 (tbl:reasoning)** - Reasoning effort analysis
- [ ] **Table B1 (tbl:error_ci)** - Extended accuracy with confidence intervals
- [ ] **Table B2 (tbl:method_performance)** - Detailed performance metrics
- [ ] **Table B3 (tbl:cost_accuracy)** - Cost-accuracy trade-off analysis
- [ ] **Table B4 (tbl:time_usage)** - Processing time analysis
- [ ] **Table B5 (tbl:token_usage)** - Token consumption statistics
- [ ] **Table B6 (tbl:human_benchmark)** - Professional GIS benchmark breakdown

#### Text Sections Requiring Updates:
- [ ] **Section 4.2** - Add H-2 method description
- [ ] **Section 6.1** - Update accuracy results with H-2
- [ ] **Section 6.2** - Update cost-accuracy analysis
- [ ] **Section 6.3** - Update latency analysis  
- [ ] **Section 6.5** - Update tool usage patterns (if H-2 uses tools)
- [ ] **Section 6.6** - Update robustness analysis
- [ ] **Section 7.1** - Update implications discussion
- [ ] **Section 7.2** - Update error analysis
- [ ] **Abstract** - Update key results with H-2 performance

### Phase 4: Quality Assurance
- [ ] **Cross-check all numbers** - Verify consistency between tables and text
- [ ] **Update figure captions** - Ensure all mention H-2 where appropriate
- [ ] **Verify method ordering** - Ensure consistent ranking by performance
- [ ] **Check confidence intervals** - Ensure all CIs reflect updated data
- [ ] **Validate cost calculations** - Confirm H-2 cost methodology
- [ ] **Review conclusions** - Update based on H-2 performance

### Phase 5: Final Integration
- [ ] **Run complete paper build** - Generate final PDF with all updates
- [ ] **Proofread entire paper** - Check for H-2 integration consistency
- [ ] **Update repository** - Ensure all code/data reflects H-2 inclusion
- [ ] **Final validation** - Confirm all metrics are internally consistent

## NOTES:
- H-2 data successfully added to full_results.csv ✅
- All analysis scripts now use ONLY full_results.csv (no validation files) ✅
- H-2 shows mean error of ~79-81 km (between H-1 and automated methods)
- Need to determine if H-2 uses tools or is one-shot methodology
- Consider H-2's position in cost-accuracy Pareto frontier