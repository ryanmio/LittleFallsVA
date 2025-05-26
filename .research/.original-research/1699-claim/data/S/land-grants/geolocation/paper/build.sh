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

# ---------------- JOSIS / Overleaf build ----------------
#   1. Convert Markdown to a LaTeX body (content.tex)
#   2. Sync figures and bibliography into the template folder
#   3. Optionally compile a JOSIS-styled PDF for local preview
# --------------------------------------------------------

# Location of the JOSIS template folder relative to this script
TEMPLATE_DIR="$PAPER_DIR/Journal of Spatial Information Science template"

# Ensure template folder exists
if [ -d "$TEMPLATE_DIR" ]; then
    echo "Updating JOSIS template at: $TEMPLATE_DIR"
else
    echo "⚠️  JOSIS template folder not found at $TEMPLATE_DIR – skipping JOSIS build."
    exit 0
fi

# Path to output body-only LaTeX
CONTENT_TEX="$TEMPLATE_DIR/content.tex"

# Backup the current content.tex if it exists
if [ -f "$CONTENT_TEX" ]; then
    cp "$CONTENT_TEX" "$CONTENT_TEX.backup"
    echo "Backed up existing content.tex to content.tex.backup"
fi

# 1. Generate body-only LaTeX (no preamble)
pandoc "$MAIN_MD" \
  --from markdown \
  --to latex \
  --natbib \
  --listings \
  $CROSSREF \
  --resource-path="$PAPER_DIR:$FIGURES_DIR" \
  -o "$CONTENT_TEX"

# 2. Post-process the content.tex file for JOSIS format...
echo "Post-processing content.tex for JOSIS format..."

# FIRST: Remove the abstract section entirely since it's handled by article.tex
# Find the Introduction section and remove everything before it
INTRO_LINE=$(grep -n "Introduction" "$CONTENT_TEX" | head -1 | cut -d':' -f1)
if [ ! -z "$INTRO_LINE" ]; then
  # Remove everything from the beginning to the Introduction line (not including Introduction)
  sed -i '' "1,$((INTRO_LINE-1))d" "$CONTENT_TEX"
  echo "Removed abstract section - content.tex now starts with Introduction"
else
  echo "Warning: Could not find Introduction section"
fi

# Fix section numbering by adding numbers to section headers
sed -i '' 's/\\section{/\\section{/g' "$CONTENT_TEX"
sed -i '' 's/\\section{1 /\\section{/g' "$CONTENT_TEX"
sed -i '' 's/\\section{2 /\\section{/g' "$CONTENT_TEX"
sed -i '' 's/\\section{3 /\\section{/g' "$CONTENT_TEX"
sed -i '' 's/\\section{4 /\\section{/g' "$CONTENT_TEX"
sed -i '' 's/\\section{5 /\\section{/g' "$CONTENT_TEX"
sed -i '' 's/\\section{6 /\\section{/g' "$CONTENT_TEX"
sed -i '' 's/\\section{7 /\\section{/g' "$CONTENT_TEX"
sed -i '' 's/\\section{8 /\\section{/g' "$CONTENT_TEX"
sed -i '' 's/\\section{9 /\\section{/g' "$CONTENT_TEX"
sed -i '' 's/\\section{10 /\\section{/g' "$CONTENT_TEX"
sed -i '' 's/\\section{11 /\\section{/g' "$CONTENT_TEX"

# Fix subsection numbering
sed -i '' 's/\\subsection{1\.1 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{1\.2 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{1\.3 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{2\.1 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{2\.2 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{2\.3 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{3\.1 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{3\.2 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{3\.3 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{4\.1 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{4\.2 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{4\.3 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{4\.4 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{5\.1 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{5\.2 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{6\.1 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{6\.2 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{6\.3 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{6\.4 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{6\.5 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{6\.6 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{7\.1 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{7\.2 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{7\.3 /\\subsection{/g' "$CONTENT_TEX"

# Properly handle the appendix
# First remove any existing appendix commands
sed -i '' '/\\appendix/d' "$CONTENT_TEX"
sed -i '' '/\\section{Appendices}/d' "$CONTENT_TEX"

# Find the line number of the first supplementary section
SUPP_LINE=$(grep -n "section{Supplementary Methods" "$CONTENT_TEX" | head -1 | cut -d':' -f1)

if [ ! -z "$SUPP_LINE" ]; then
  # Insert a line before the Supplementary Methods section
  sed -i '' "${SUPP_LINE}i\\
\\\\appendix" "$CONTENT_TEX"
  # Fix the literal \n that might be inserted
  sed -i '' 's/\\\\appendix\\n/\\\\appendix/' "$CONTENT_TEX"
  sed -i '' 's/\\\\appendix/\\appendix/' "$CONTENT_TEX"
  echo "Inserted appendix command at line $SUPP_LINE"
else
  # Fallback: try with Acknowledgements section
  ACK_LINE=$(grep -n "section{Acknowledgements}" "$CONTENT_TEX" | head -1 | cut -d':' -f1)
  
  if [ ! -z "$ACK_LINE" ]; then
    # Add 15 lines to get past the acknowledgements section
    INSERT_LINE=$((ACK_LINE + 15))
    sed -i '' "${INSERT_LINE}i\\
\\\\appendix" "$CONTENT_TEX"
    # Fix the literal \n that might be inserted
    sed -i '' 's/\\\\appendix\\n/\\\\appendix/' "$CONTENT_TEX"
    sed -i '' 's/\\\\appendix/\\appendix/' "$CONTENT_TEX"
    echo "Inserted appendix command at line $INSERT_LINE (after Acknowledgements)"
  else
    echo "Warning: Could not find appropriate place to insert appendix command"
  fi
fi

# Fix appendix subsections
sed -i '' 's/\\subsection{Appendix A Supplementary Methods/\\section{Supplementary Methods/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{Appendix B Extended/\\section{Extended/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{Appendix C Supplementary/\\section{Supplementary/g' "$CONTENT_TEX"
sed -i '' 's/\\subsection{Appendix D Tool/\\section{Tool/g' "$CONTENT_TEX"

# Fix subsubsections in appendices
sed -i '' 's/\\subsubsection{A\.1 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsubsection{A\.2 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsubsection{A\.3 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsubsection{A\.4 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsubsection{A\.5 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsubsection{B\.1 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsubsection{B\.2 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsubsection{B\.3 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsubsection{B\.4 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsubsection{B\.5 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsubsection{B\.6 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsubsection{C\.1 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsubsection{C\.2 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsubsection{C\.3 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsubsection{C\.4 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsubsection{D\.1 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsubsection{D\.2 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsubsection{D\.3 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsubsection{D\.4 /\\subsection{/g' "$CONTENT_TEX"
sed -i '' 's/\\subsubsection{D\.5 /\\subsection{/g' "$CONTENT_TEX"

# Fix includegraphics paths and options for better JOSIS compatibility
# IMPORTANT: Preserve the original image formatting and only change the paths

# First, fix the grant example images with proper formatting (before general path replacement)
sed -i '' 's/\\includegraphics\[width=\\linewidth,height=0.35\\textheight,keepaspectratio\]{..\/analysis\/figures\/map_outputs/\\includegraphics[width=\\linewidth,height=0.35\\textheight,keepaspectratio]{figures\/map_outputs/g' "$CONTENT_TEX"

# Then fix other image types
sed -i '' 's/\\includegraphics\[width=\\textwidth,height=0.8\\textheight,keepaspectratio\]{..\/analysis\/figures/\\includegraphics[width=\\textwidth,height=0.8\\textheight,keepaspectratio]{figures/g' "$CONTENT_TEX"
sed -i '' 's/\\includegraphics\[width=\\linewidth,height=0.35\\textheight,keepaspectratio\]{..\/analysis\/figures/\\includegraphics[width=\\linewidth,height=0.35\\textheight,keepaspectratio]{figures/g' "$CONTENT_TEX"
sed -i '' 's/\\includegraphics\[width=0.75\\linewidth\]{..\/analysis\/figures/\\includegraphics[width=0.75\\linewidth]{figures/g' "$CONTENT_TEX"
sed -i '' 's/\\begin{figure}\[htbp\]/\\begin{figure}[H]/g' "$CONTENT_TEX"

# Make sure pandocbounded includes are properly handled
sed -i '' 's/\\pandocbounded{\\includegraphics\[keepaspectratio\]{..\/analysis\/figures/\\pandocbounded{\\includegraphics[keepaspectratio]{figures/g' "$CONTENT_TEX"

# Replace all remaining references to "../analysis/figures" with "figures"
sed -i '' 's/..\/analysis\/figures/figures/g' "$CONTENT_TEX"

# Convert pandocbounded format to specific sizing format (to match manually edited version)
sed -i '' 's/\\pandocbounded{\\includegraphics\[keepaspectratio\]{figures\/\([^}]*\)}}/\\includegraphics[width=\\textwidth,height=0.8\\textheight,keepaspectratio]{figures\/\1}/g' "$CONTENT_TEX"

# Apply pandocbounded conversion again to catch any remaining patterns
sed -i '' 's/\\pandocbounded{\\includegraphics\[keepaspectratio\]{figures\/\([^}]*\)}}/\\includegraphics[width=\\textwidth,height=0.8\\textheight,keepaspectratio]{figures\/\1}/g' "$CONTENT_TEX"

# Fix figure path for grant examples 
sed -i '' 's/..\/analysis\/mapping_workflow\/map_outputs/figures\/map_outputs/g' "$CONTENT_TEX"
sed -i '' 's/..\/analysis\/mapping_workflow\/contact_sheet.png/figures\/contact_sheet.png/g' "$CONTENT_TEX"

# Add missing height and aspect ratio parameters to grant map images
sed -i '' 's/\\includegraphics\[width=\\linewidth\]{figures\/map_outputs/\\includegraphics[width=\\linewidth,height=0.35\\textheight,keepaspectratio]{figures\/map_outputs/g' "$CONTENT_TEX"

# Fix the endminipage issue 
sed -i '' 's/\\endend{minipage}/\\end{minipage}/g' "$CONTENT_TEX"

# FINAL: Convert any remaining pandocbounded patterns (do this last)
sed -i '' 's/\\pandocbounded{\\includegraphics\[keepaspectratio\]{figures\/\([^}]*\)}}/\\includegraphics[width=\\textwidth,height=0.8\\textheight,keepaspectratio]{figures\/\1}/g' "$CONTENT_TEX"

# 3. Copy bibliography
cp "$REFS_BIB" "$TEMPLATE_DIR/refs.bib"

# 4. Sync figure assets used in the paper into template/figures
if [ -d "$FIGURES_DIR" ]; then
  # Create figures directory in template if it doesn't exist
  mkdir -p "$TEMPLATE_DIR/figures"
  
  # Copy figures to template directory
  rsync -av --delete "$FIGURES_DIR/" "$TEMPLATE_DIR/figures/" | grep -v '/$'
  
  # Create mapping_workflow directory and copy map outputs if they exist
  MAPPING_DIR="$(dirname "$PAPER_DIR")/analysis/mapping_workflow"
  if [ -d "$MAPPING_DIR" ]; then
    mkdir -p "$TEMPLATE_DIR/figures/mapping_workflow"
    rsync -av --delete "$MAPPING_DIR/" "$TEMPLATE_DIR/figures/mapping_workflow/" | grep -v '/$'
  fi
  
  # Create cdf_graphs directory if it doesn't exist
  mkdir -p "$TEMPLATE_DIR/figures/cdf_graphs"
  
  # Copy CDF graphs if they exist
  CDF_DIR="$FIGURES_DIR/cdf_graphs"
  if [ -d "$CDF_DIR" ]; then
    rsync -av --delete "$CDF_DIR/" "$TEMPLATE_DIR/figures/cdf_graphs/" | grep -v '/$'
  fi
fi

# 5. (Optional) compile JOSIS PDF locally for preview
if command -v latexmk &> /dev/null; then
  (
    cd "$TEMPLATE_DIR" || exit 1
    echo "Compiling JOSIS-formatted PDF…"
    latexmk -pdf -silent article.tex
    latexmk -c # clean aux files
  )
  if [ -f "$TEMPLATE_DIR/article.pdf" ]; then
    echo "JOSIS PDF built at $TEMPLATE_DIR/article.pdf"
  else
    echo "⚠️  LaTeX build failed—check logs in template folder."
  fi
else
  echo "Latexmk not available; Skipping local JOSIS PDF compilation."
fi

# 6. Create double-blind versions for submission
echo "Creating double-blind versions for submission..."

# Create blind article.tex by copying and editing the original
cp "$TEMPLATE_DIR/article.tex" "$TEMPLATE_DIR/article_blind.tex"

# Remove identifying information from article_blind.tex
sed -i '' 's/Ryan Mioduski/[Author name removed for blind review]/g' "$TEMPLATE_DIR/article_blind.tex"
sed -i '' 's/Independent Researcher/[Affiliation removed for blind review]/g' "$TEMPLATE_DIR/article_blind.tex"
sed -i '' 's/received={May 24, 2025}/received={[Date removed for blind review]}/g' "$TEMPLATE_DIR/article_blind.tex"
# Redirect the main body to the blind content file
sed -i '' 's/\\input{content.tex}/\\input{content_blind.tex}/g' "$TEMPLATE_DIR/article_blind.tex"

# Create blind content.tex by removing identifying information
cp "$CONTENT_TEX" "$TEMPLATE_DIR/content_blind.tex"

# Remove GitHub references (replace with placeholder)
sed -i '' 's|https://github\.com/ryanmio/colonial-virginia-llm-geolocation|[Repository URL removed for blind review]|g' "$TEMPLATE_DIR/content_blind.tex"
sed -i '' 's|https://github\.com/ryanmioduskiimac/littlefallsva|[Repository URL removed for blind review]|g' "$TEMPLATE_DIR/content_blind.tex"

# Remove acknowledgments section entirely
sed -i '' '/\\section{Acknowledgments}/,/^$/d' "$TEMPLATE_DIR/content_blind.tex"
sed -i '' '/\\subsection{Acknowledgments}/,/^$/d' "$TEMPLATE_DIR/content_blind.tex"

# Replace any author name references
sed -i '' 's/Ryan Mioduski/[Author name removed for blind review]/g' "$TEMPLATE_DIR/content_blind.tex"

# Compile blind version if latexmk is available
if command -v latexmk &> /dev/null; then
  (
    cd "$TEMPLATE_DIR" || exit 1
    echo "Compiling double-blind PDF..."
    latexmk -pdf -silent article_blind.tex
    latexmk -c # clean aux files
  )
  if [ -f "$TEMPLATE_DIR/article_blind.pdf" ]; then
    echo "Double-blind PDF built at $TEMPLATE_DIR/article_blind.pdf"
  else
    echo "⚠️  Double-blind LaTeX build failed—check logs in template folder."
  fi
fi

echo "Double-blind versions created:"
echo "  - $TEMPLATE_DIR/article_blind.tex"
echo "  - $TEMPLATE_DIR/content_blind.tex"
echo "  - $TEMPLATE_DIR/article_blind.pdf (if LaTeX compilation succeeded)"

echo "JOSIS update complete." 