#!/bin/bash
# process_batch.sh - Process multiple PDFs in parallel
# Usage: ./process_batch.sh <max_parallel>

# Set up environment
cd "$(dirname "$0")"
source ../venv/bin/activate

# Directory paths
PDF_DIR="../pdf scans"
OUTPUT_DIR="../OCR-output"

# Max parallel processes (default: 2)
MAX_PARALLEL=${1:-2}

# All PDFs to process, in order
PDF_FILES=(
  "book10.pdf"
  "book10pt2.pdf"
  "book11_20250426190043.pdf"  # Better rescan of book11.pdf
  "book12part1.pdf"
  "book13_20250426190714.pdf"  # Better rescan of book13.pdf
  "book14.pdf"
  "index1.pdf"
  "index2.pdf"
)

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Function to process a single PDF
process_pdf() {
  local pdf_file="$1"
  echo "Starting OCR for $pdf_file ($(date))"
  python process_single_pdf.py --input-pdf "$PDF_DIR/$pdf_file" --output-dir "$OUTPUT_DIR"
  local status=$?
  echo "Finished OCR for $pdf_file with status $status ($(date))"
  return $status
}

# Keep track of running processes
declare -a pids

# Process PDFs with parallelism
for pdf_file in "${PDF_FILES[@]}"; do
  # Check if output already exists
  if [ -f "$OUTPUT_DIR/${pdf_file%.pdf}_ocr.txt" ]; then
    echo "Skipping $pdf_file - already processed"
    continue
  fi
  
  # Wait if we've reached max parallel processes
  while [ ${#pids[@]} -ge $MAX_PARALLEL ]; do
    for i in "${!pids[@]}"; do
      if ! kill -0 ${pids[$i]} 2>/dev/null; then
        wait ${pids[$i]}
        status=$?
        unset pids[$i]
        break
      fi
    done
    sleep 1
  done
  
  # Start processing this PDF in background
  process_pdf "$pdf_file" &
  pids+=($!)
  echo "Started $pdf_file (PID: $!), active jobs: ${#pids[@]}"
done

# Wait for remaining processes to finish
for pid in "${pids[@]}"; do
  wait $pid
done

echo "All PDFs processed!" 