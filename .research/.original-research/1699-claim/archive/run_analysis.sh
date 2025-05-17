#!/bin/bash

# Falls Church 1699 Settlement Analysis Runner
# This script sets up the environment and runs the analysis

echo "Setting up environment..."
# Check if we have the required Python packages
if ! command -v pip &> /dev/null; then
    echo "pip not found. Please install Python and pip first."
    exit 1
fi

# Install requirements
echo "Installing required Python packages..."
pip install -r requirements.txt

# Run the analysis
echo "Running Bayesian analysis..."
python falls_church_model.py

# Check if figures were generated
if [ -f "figures/posterior_density.pdf" ] && [ -f "figures/sobol_indices.pdf" ]; then
    echo "Analysis complete! Figures generated successfully."
    echo "Posterior density plot: figures/posterior_density.pdf"
    echo "Sobol indices plot: figures/sobol_indices.pdf"
    echo "Results saved to: falls_church_results.csv"
else
    echo "Error: Figures were not generated correctly."
    exit 1
fi 