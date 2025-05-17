#!/bin/bash
set -e

# Navigate to the directory containing the paper
cd "$(dirname "$0")"

# Create output directories if they don't exist
mkdir -p overleaf_export
mkdir -p overleaf_export/figures

# Copy figures to output directory
cp -r figures/*.pdf overleaf_export/figures/ 2>/dev/null || true
cp -r figures/*.png overleaf_export/figures/ 2>/dev/null || true

# Convert markdown to tex using pandoc with the template.latex file
echo "Converting Markdown to LaTeX using template.latex..."
pandoc paper.md -o overleaf_export/main.tex \
  --standalone \
  --template=template.latex \
  --natbib \
  --number-sections

# Fix any remaining figure issues by replacing problematic LaTeX figure syntax
echo "Fixing figure syntax for Overleaf compatibility..."
sed -i '' 's/\[width=0.8\\linewidth,height=\\textheight,keepaspectratio\]/[width=0.8\\textwidth]/g' overleaf_export/main.tex

# Copy bibliography and template files
cp refs.bib overleaf_export/ 2>/dev/null || true
cp template.latex overleaf_export/ 2>/dev/null || true

# Create a zip file for easy upload to Overleaf
echo "Creating zip file for Overleaf..."
cd overleaf_export
zip -r ../falls_church_overleaf.zip main.tex template.latex refs.bib figures/* 2>/dev/null || zip -r ../falls_church_overleaf.zip main.tex template.latex

cd ..
echo "Success! Files prepared for Overleaf in overleaf_export/ directory"
echo "Zip file created at: falls_church_overleaf.zip"
echo "You can upload this zip file directly to Overleaf." 