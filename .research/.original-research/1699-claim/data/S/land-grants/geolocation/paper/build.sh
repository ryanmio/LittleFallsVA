#!/bin/bash
# Make sure you are in the right directory!
# cd /Users/ryanmioduskiimac/littlefallsva/.research/.original-research/1699-claim/data/S/land-grants/geolocation/paper
#./build.sh

# Set the directory variables
PAPER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAIN_MD="$PAPER_DIR/main.md"
REFS_BIB="$PAPER_DIR/refs.bib"
OUTPUT_PDF="$PAPER_DIR/paper_preview.pdf"
ERROR_LOG="$PAPER_DIR/build_errors.log"
FIGURES_DIR="$(dirname "$PAPER_DIR")/analysis/figures"

# Verify figures directory exists
if [ ! -d "$FIGURES_DIR" ]; then
    echo "Warning: Figures directory not found at: $FIGURES_DIR"
    echo "Some figures may not render properly."
else
    echo "Using figures from: $FIGURES_DIR"
fi

# Check if apa.csl exists, download if not
if [ ! -f "$PAPER_DIR/apa.csl" ]; then
    echo "Downloading APA citation style file..."
    curl -s -o "$PAPER_DIR/apa.csl" https://www.zotero.org/styles/apa
fi

# Check for pandoc-crossref filter
if ! command -v pandoc-crossref &> /dev/null; then
    echo "Warning: pandoc-crossref filter not found."
    echo "For proper table and figure cross-references, install it with:"
    echo "  brew install pandoc-crossref"
    CROSSREF=""
else
    CROSSREF="--filter=pandoc-crossref"
    echo "Using pandoc-crossref for cross-references."
fi

# Create a header file for styling
cat > "$PAPER_DIR/styling.tex" << EOF
% Prevent colored links
\\usepackage{hyperref}
% Enable stronger float placement controls and text-wrapping figures
\\usepackage{float}  % Provides the [H] specifier so figures stay where defined
% Load wrapfig only if it exists (prevents LaTeX halt on systems without the package)
\\IfFileExists{wrapfig.sty}{\\usepackage{wrapfig}}{}
% Keep floats within their section to prevent them from sliding past heading changes (if available)
\\IfFileExists{placeins.sty}{\\usepackage[section]{placeins}}{}
\\usepackage{subcaption}
\hypersetup{
    colorlinks=true,
    linkcolor=black,
    filecolor=black,
    urlcolor=black,
    citecolor=black
}
EOF

# Generate PDF with proper cross-references
echo "Generating PDF..."
pandoc -s "$MAIN_MD" -o "$OUTPUT_PDF" \
    --bibliography="$REFS_BIB" \
    --csl="$PAPER_DIR/apa.csl" \
    $CROSSREF \
    --citeproc \
    --pdf-engine=xelatex \
    -V documentclass=article \
    -V geometry:margin=1in \
    -V fontsize=11pt \
    --include-in-header="$PAPER_DIR/math_fix.tex" \
    --include-in-header="$PAPER_DIR/styling.tex" \
    --include-in-header="$PAPER_DIR/code_style.tex" \
    --listings \
    --metadata link-citations=true \
    -M figPrefix="Figure" \
    -M figLabels=arabic \
    -M secPrefix="Section" \
    -M secLabels=arabic \
    -M eqnPrefix="Equation" \
    -M tblPrefix="" \
    -M autoSectionLabels=true \
    --resource-path=.:../analysis/figures:../analysis/figures/cdf_graphs \
    --extract-media=extracted-media 2>"$ERROR_LOG"

# Check if PDF generation was successful
if [ -f "$OUTPUT_PDF" ] && [ -s "$OUTPUT_PDF" ]; then
    echo "PDF generation successful."
    open "$OUTPUT_PDF"
else
    echo "PDF generation failed. See $ERROR_LOG for details."
fi

# Clean up temporary files
rm -f "$PAPER_DIR/styling.tex"

echo "Build process complete." 