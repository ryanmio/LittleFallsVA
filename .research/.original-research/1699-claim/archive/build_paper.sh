#!/bin/bash

# Falls Church 1699 Paper Builder
# This script guides through the entire workflow of building the paper

echo "=== Falls Church 1699 Settlement Claim Paper Builder ==="
echo "Building the paper with the latest results..."

# Clean previous build files if they exist
echo "Cleaning previous build files..."
make clean

# Make sure the template exists
if [ ! -f "template.latex" ]; then
    echo "ERROR: template.latex is missing. Cannot proceed."
    exit 1
fi

# Generate main.tex from paper.md using our custom template
echo "Generating LaTeX document from Markdown..."
pandoc paper.md \
    --from=markdown+tex_math_dollars \
    --template=template.latex \
    --citeproc \
    -o main.tex

# Check if the LaTeX file was generated successfully
if [ ! -f "main.tex" ]; then
    echo "ERROR: Failed to generate main.tex"
    exit 1
fi

# Build PDF with latexmk
echo "Building PDF document..."
latexmk -pdf main.tex

# Check if PDF was built successfully
if [ ! -f "main.pdf" ]; then
    echo "ERROR: Failed to generate main.pdf"
    exit 1
fi

echo "=== Build completed successfully ==="
echo "Output files:"
echo "- main.tex: LaTeX document"
echo "- main.pdf: Final PDF document"
echo ""
echo "To preview the PDF, run: open main.pdf"
echo ""

# Make the script executable
chmod +x build_paper.sh 