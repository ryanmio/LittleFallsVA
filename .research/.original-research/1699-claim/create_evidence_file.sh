#!/bin/bash
# Script to create a new evidence file from the template

# Check if parameters are provided
if [ $# -lt 3 ]; then
    echo "Usage: $0 <factor> <dataset_id> <evidence_type>"
    echo "  factor: One of R, S, D, V, A"
    echo "  dataset_id: Descriptive name with underscores"
    echo "  evidence_type: Brief description in quotes"
    echo ""
    echo "Example: $0 R land_patents_northern_neck \"Northern Neck land patents 1650-1739\""
    exit 1
fi

FACTOR=$1
DATASET_ID=$2
EVIDENCE_TYPE=$3

# Ensure factor is valid
if [[ ! "$FACTOR" =~ ^[RSDVA]$ ]]; then
    echo "Error: Factor must be one of R, S, D, V, A"
    exit 1
fi

# Create the output file path
OUTPUT_FILE="data/$FACTOR/${DATASET_ID}.md"

# Check if file already exists
if [ -f "$OUTPUT_FILE" ]; then
    echo "Error: File $OUTPUT_FILE already exists"
    exit 1
fi

# Create a copy of the template
cp data/TEMPLATE.md "$OUTPUT_FILE"

# Replace template values with provided parameters
sed -i '' "s/factor: \"X\"/factor: \"$FACTOR\"/" "$OUTPUT_FILE"
sed -i '' "s/dataset_id: \"descriptive_name_timeperiod\"/dataset_id: \"$DATASET_ID\"/" "$OUTPUT_FILE"
sed -i '' "s/evidence_type: \"Brief description of evidence type\"/evidence_type: \"$EVIDENCE_TYPE\"/" "$OUTPUT_FILE"

echo "Created new evidence file: $OUTPUT_FILE"
echo "Edit this file to add your evidence details." 