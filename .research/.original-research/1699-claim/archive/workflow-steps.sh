#!/bin/bash
# This script outlines the workflow steps without executing them
# To actually run these commands, you'll need to install dependencies first

echo "### Step 1: Install prerequisites (on macOS)"
echo "brew install pandoc latexmk basictex"
echo "# You might need to run: sudo tlmgr install collection-fontsrecommended"
echo "pip install arxiv-latex-cleaner"
echo ""

echo "### Step 2: Convert Markdown to LaTeX using custom template"
echo "cd /Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim"
echo "pandoc paper.md \\
      --from=markdown+tex_math_dollars \\
      --template=template.latex \\
      --citeproc \\
      -o main.tex"
echo ""

echo "### Step 3: Compile PDF using latexmk"
echo "latexmk -pdf main.tex"
echo ""

echo "### Step 4: Check PDF quality"
echo "pdffonts main.pdf   # Verify all fonts are embedded"
echo ""

echo "### Step 5: Move to Overleaf (optional)"
echo "# Create new project on Overleaf"
echo "# Upload main.tex, template.latex, refs.bib, and figures/ directory"
echo ""

echo "### Step 6: Clean for submission"
echo "arxiv_latex_cleaner --images_compress --verbose ."
echo "zip -r falls-church-1699.zip main.tex template.latex figures/ refs.bib"
echo ""

echo "### Alternative: Use the provided Makefile or build script"
echo "make tex    # Generate LaTeX only"
echo "make pdf    # Generate PDF via LaTeX"
echo "make clean  # Remove temporary files"
echo "make preview # Open the PDF (macOS only)"
echo "make arxiv-clean # Prepare for arXiv submission"
echo ""
echo "# Or use the all-in-one build script:"
echo "./build_paper.sh  # Generates LaTeX and PDF with proper error checking" 