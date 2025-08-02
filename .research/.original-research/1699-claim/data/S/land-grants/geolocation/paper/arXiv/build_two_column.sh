#!/usr/bin/env bash
# Build two-column PDF directly from main.md
# Usage: ./build_two_column.sh

set -euo pipefail
PAPER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$PAPER_DIR")"
MAIN_MD="$ROOT_DIR/main.md"
TEX_OUT="$PAPER_DIR/main_two_column.tex"
PDF_OUT="$PAPER_DIR/main_two_column.pdf"
CROSSREF=""

if command -v pandoc-crossref >/dev/null 2>&1; then
  CROSSREF="--filter pandoc-crossref"
  echo "Using pandoc-crossref for figure & table labels."
else
  echo "⚠️  pandoc-crossref not found – table refs will break."
fi

# Before generating LaTeX
# Ensure numeric superscript CSL style (Nature)
NUM_CSL="$ROOT_DIR/numeric_superscript.csl"
if [ ! -f "$NUM_CSL" ]; then
  echo "Downloading Nature CSL for superscript numeric citations…"
  curl -s -o "$NUM_CSL" https://www.zotero.org/styles/nature
fi

echo "Generating two-column LaTeX…"
pandoc "$MAIN_MD" \
  --from markdown \
  --to latex \
  $CROSSREF \
  --citeproc \
  --bibliography="$ROOT_DIR/refs.bib" \
  --csl="$NUM_CSL" \
  -V documentclass=article \
  -V classoption=twocolumn \
  -V geometry:margin=1in \
  -V fontsize=10pt \
  --include-in-header="$PAPER_DIR/code_style_two_column.tex" \
  --listings \
  --metadata link-citations=true \
  -o "$TEX_OUT"

# Post-process to enforce safer table layout in two-column mode
# Remove problematic onecolumn/twocolumn commands and let tables stay in natural layout

# Remove any existing onecolumn/twocolumn commands that might be causing issues
sed -i '' '/\\onecolumn/d' "$TEX_OUT"
sed -i '' '/\\twocolumn/d' "$TEX_OUT"

# Fix any malformed table structures that might have been created
# Remove any duplicate caption/label combinations
sed -i '' '/\\end{tabular}\\caption{Coordinate-accuracy metrics.}\\label{tbl:accuracy}\\end{table*}/d' "$TEX_OUT"

# Convert key figures to figure* for full width presentation
# These are the main results figures that benefit from full width
sed -i '' 's/\\begin{figure}/\\begin{figure*}/g' "$TEX_OUT"
sed -i '' 's/\\end{figure}/\\end{figure*}/g' "$TEX_OUT"

# (Removed) Do not force a clear page before Discussion; let floats settle naturally

# Ensure Appendices starts on fresh one-column page
sed -i '' '/\\section{Appendices}/{i\
\\onecolumn
}' "$TEX_OUT"

# The first appendix heading begins with "\\subsection{Appendix A", ensure single column from there to end
# (Removed – we now transition before the section header instead)

# Define path to geolocation project root
GEO_DIR="$(dirname "$(dirname "$PAPER_DIR")")"
CONTACT_SHEET="$GEO_DIR/analysis/mapping_workflow/contact_sheet.png"

# 1. Replace broken image paths so LaTeX looks inside arXiv/figures and arXiv/map_outputs
sed -i '' 's|\./analysis/figures/|figures/|g' "$TEX_OUT"
sed -i '' 's|\.\./analysis/figures/|figures/|g' "$TEX_OUT"
sed -i '' 's|\.\./analysis/mapping_workflow/map_outputs/|map_outputs/|g' "$TEX_OUT"
sed -i '' 's|../analysis/mapping_workflow/contact_sheet.png|map_outputs/contact_sheet.png|g' "$TEX_OUT"
# copy after rsync
if [ -f "$CONTACT_SHEET" ]; then
  cp "$CONTACT_SHEET" "$PAPER_DIR/map_outputs/contact_sheet.png"
fi

# After rsync ensures file exists
after_rsync_contact="$PAPER_DIR/map_outputs/contact_sheet.png"
if [ -f "$CONTACT_SHEET" ]; then
  cp "$CONTACT_SHEET" "$after_rsync_contact"
fi

# 2. Sync figure assets into arXiv/figures and map_outputs
FIGURES_SRC="$GEO_DIR/analysis/figures"
MAP_SRC="$GEO_DIR/analysis/mapping_workflow/map_outputs"
mkdir -p "$PAPER_DIR/figures" "$PAPER_DIR/map_outputs"
if [ -d "$FIGURES_SRC" ]; then
  rsync -av --delete "$FIGURES_SRC/" "$PAPER_DIR/figures/" | grep -v '/$'
fi
if [ -d "$MAP_SRC" ]; then
  rsync -av --delete "$MAP_SRC/" "$PAPER_DIR/map_outputs/" | grep -v '/$'
fi

sed -i '' 's|\.figures/|figures/|g' "$TEX_OUT"

# Fix subfigure width lines that render literal "0.48" in output
# Prepend a position option so LaTeX treats the numeric width correctly.
sed -i '' 's|\\begin{subfigure}{0\\.48\\textwidth}|\\begin{subfigure}[t]{0.48\\textwidth}|g' "$TEX_OUT"

# Ensure subfigure environment exists by adding subcaption package (BSD sed)
sed -i '' '/\\usepackage{graphicx}/a\
\\usepackage{subcaption}\
' "$TEX_OUT"

# --- Fix missing 4.5–4.8 subsection numbers ---
sed -i '' \
  -e 's/\\subsection{One-shot Prompting/\\subsection{4.5 One-shot Prompting/' \
  -e 's/\\subsection{Tool-augmented Chain-of-Thought/\\subsection{4.6 Tool-augmented Chain-of-Thought/' \
  -e 's/\\subsection{Five-call Ensemble/\\subsection{4.7 Five-call Ensemble/' \
  -e 's/\\subsection{Cost and Latency/\\subsection{4.8 Cost and Latency/' \
  "$TEX_OUT"

# Add sed commands to change [H] spec to [tbp] in table, table*, figure*, and figure environments to allow floats
sed -i '' '/\\begin{table}\[H\]/s/\\[H\\]/[tbp]/' "$TEX_OUT"
sed -i '' '/\\begin{table\*}\[H\]/s/\\[H\\]/[tbp]/' "$TEX_OUT"
sed -i '' '/\\begin{figure\*}\[H\]/s/\\[H\\]/[tbp]/' "$TEX_OUT"
sed -i '' '/\\begin{figure}\[H\]/s/\\[H\\]/[tbp]/' "$TEX_OUT"

# Force token pricing table to stay near the cost equation
sed -i '' 's/\\begin{table}\[H\]/\\begin{table}[ht!]/' "$TEX_OUT"

# Make length vs error figure smaller so it doesn't take a whole page
sed -i '' '/\\label{fig:length-vs-error}/,/\\end{figure\*}/ {
  /\\includegraphics/s/\\[keepaspectratio\\]/[width=0.7\\textwidth]/g
}' "$TEX_OUT"

echo "Compiling PDF…"
cd "$PAPER_DIR"
pdflatex -interaction=nonstopmode main_two_column.tex >/dev/null
bibtex   main_two_column      >/dev/null || true
pdflatex -interaction=nonstopmode main_two_column.tex >/dev/null
pdflatex -interaction=nonstopmode main_two_column.tex >/dev/null

echo "✓ Built $PDF_OUT"
open "$PDF_OUT" 