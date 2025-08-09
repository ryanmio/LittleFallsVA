CSL_SRC="$(dirname "$ROOT")/apa.csl"
if [ -f "$CSL_SRC" ] && [ ! -f "$ROOT/apa.csl" ]; then
  cp "$CSL_SRC" "$ROOT/apa.csl"
fi

# Generate LaTeX
pandoc "$SRC" 