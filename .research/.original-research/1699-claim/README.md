# Falls Church 1699 Settlement Claim Analysis

This repository contains the analysis code, paper, and data for the "Quantifying the Plausibility of Falls Church's 1699 Settlement Date: A Bayesian Chain‑Rule Analysis" paper.

## Current Workflow & Essential Files

### Core Files
- `paper.md` - The paper content in Markdown format
- `bayesian_analysis.py` - Main Bayesian model implementation with logical constraints
- `template.latex` - LaTeX template for consistent PDF generation
- `build_overleaf.sh` - Script to build LaTeX files and package for Overleaf
- `refs.bib` - Bibliography references
- `figures/` - Directory containing generated figures

### Generated Files
- `falls_church_overleaf.zip` - Ready-to-upload package for Overleaf
- `overleaf_export/` - Working directory where LaTeX files are processed before zipping
- `falls_church_results.csv` - Analysis results in CSV format
- `model_comparison.csv` - Model comparison results

## Reproduction Steps

### 1. Run the Bayesian Analysis

The main analysis script is `bayesian_analysis.py`, which:
- Implements the Bayesian chain-rule model with logical constraints
- Generates the posterior distribution and Sobol indices
- Creates figures in the `figures/` directory
- Exports results to CSV

```bash
# Run the Bayesian analysis
python bayesian_analysis.py
```

### 2. Build Paper for Overleaf

The `build_overleaf.sh` script builds the LaTeX files and packages them for Overleaf:
- Converts `paper.md` to LaTeX using `template.latex`
- Fixes any figure syntax issues for Overleaf compatibility
- Copies figures and bibliography files
- Creates a zip file ready for upload to Overleaf

```bash
# Build and package for Overleaf
bash build_overleaf.sh
```

This process:
1. Creates the `overleaf_export/` directory with all processed files
2. Generates `falls_church_overleaf.zip` for easy upload to Overleaf

### 3. Upload to Overleaf

1. Go to [Overleaf.com](https://www.overleaf.com/)
2. Create a new project
3. Upload `falls_church_overleaf.zip` using the "Upload Project" option
4. Compile the paper on Overleaf

## Prerequisites

- Python 3.9+
- Required Python packages:
  ```bash
  pip install numpy matplotlib pandas seaborn
  ```
- Pandoc (for Markdown to LaTeX conversion)
  ```bash
  # For MacOS:
  brew install pandoc
  ```

## Repository Maintenance Notes

This repository underwent cleanup on April 19, 2025.

Some older scripts remain in the archive directory for historical purposes but are not used in the current workflow.

## License

All code and data are available under CC-BY-4.0.

## Contact

For questions about this research, contact:
[ryan.mioduski@fallschurchhistoricalsociety.org](mailto:ryan.mioduski@fallschurchhistoricalsociety.org) 