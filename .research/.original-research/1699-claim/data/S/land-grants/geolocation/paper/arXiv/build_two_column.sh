#!/usr/bin/env bash
# Simple arXiv build: single column, figures inline
set -euo pipefail

ROOT=$(cd "$(dirname "$0")" && pwd)
SRC="$ROOT/main_arxiv.md"
OUT_TEX="$ROOT/main_two_column.tex"

CSL_SRC="$(dirname "$ROOT")/apa.csl"
if [ -f "$CSL_SRC" ] && [ ! -f "$ROOT/apa.csl" ]; then
  cp "$CSL_SRC" "$ROOT/apa.csl"
fi

# Generate LaTeX - SINGLE COLUMN for reliable figure placement
pandoc "$SRC" \
  --from markdown --to latex --citeproc \
  --filter pandoc-crossref \
  --bibliography="$ROOT/refs.bib" \
  -V documentclass=article \
  -V geometry:margin=1in -V fontsize=11pt \
  --include-in-header="$ROOT/code_style_two_column.tex" \
  --listings \
  -o "$OUT_TEX"

# Copy figures
FIG_SRC="$(dirname "$ROOT")/analysis/figures"
MAP_SRC="$(dirname "$ROOT")/analysis/mapping_workflow/map_outputs"
mkdir -p "$ROOT/figures" "$ROOT/map_outputs"
if [ -d "$FIG_SRC" ]; then
  rsync -a --delete "$FIG_SRC/" "$ROOT/figures/" >/dev/null
fi
if [ -d "$MAP_SRC" ]; then
  rsync -a --delete "$MAP_SRC/" "$ROOT/map_outputs/" >/dev/null
fi

# Fix paths
sed -i '' 's|\.\./analysis/figures/|figures/|g' "$OUT_TEX"
sed -i '' 's|\.\./analysis/mapping_workflow/map_outputs/|map_outputs/|g' "$OUT_TEX"
sed -i '' 's|\.\./analysis/mapping_workflow/contact_sheet.png|map_outputs/contact_sheet.png|g' "$OUT_TEX"

CONTACT_SHEET="$(dirname "$ROOT")/analysis/mapping_workflow/contact_sheet.png"
if [ -f "$CONTACT_SHEET" ]; then
  cp "$CONTACT_SHEET" "$ROOT/map_outputs/contact_sheet.png"
fi

# Compile PDF
cd "$ROOT"
FILE_BASENAME=$(basename "$OUT_TEX" .tex)

pdflatex -interaction=nonstopmode "$FILE_BASENAME.tex"
bibtex   "$FILE_BASENAME" || true
pdflatex -interaction=nonstopmode "$FILE_BASENAME.tex"
pdflatex -interaction=nonstopmode "$FILE_BASENAME.tex" 