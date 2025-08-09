# Ensemble Consensus Rule Selection

## Background
On June 16, 2025, we evaluated two consensus rules for the o3-2025-04-16 five-call ensemble method:

1. **DB-0.5 (DBSCAN)**: 500-meter DBSCAN clustering with min_samples=3, fall back to simple mean
2. **TTC (Tightest-Triple Centroid)**: Select 3 points with minimum total pairwise distance, return their centroid

## Results Summary
**Test Set:** validation-dev-A.csv (13 rows with ground truth)
**Runtime:** 69 minutes, 130 API calls, ~130K tokens

### Performance Comparison:
- **DBSCAN:** 13.48 km average error, wins 7/13 cases
- **TTC:** 14.35 km average error, wins 6/13 cases

**Winner:** DBSCAN consensus rule performs 0.87 km better on average than TTC.

## Decision
Based on the superior average performance, **DBSCAN consensus** was selected as the winning method for the full evaluation. The o3_ensemble5 method in methods.yaml now uses `consensus_rule: dbscan` as the default and only ensemble variant.

## Next Steps
- Run full evaluation on validation - TEST-FULL-H1-final.csv (45 grants) with DBSCAN ensemble
- Merge results into full_results.csv for final analysis 