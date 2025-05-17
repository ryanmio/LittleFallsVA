#!/bin/bash

# Script to add front matter to markdown files
# Usage: ./add-frontmatter.sh [file] [title] [author] [date] [source_url]

if [ "$#" -lt 5 ]; then
  echo "Usage: $0 [file] [title] [author] [date] [source_url]"
  echo "Example: $0 file.md \"Article Title\" \"Author Name\" \"2024-03-26\" \"https://example.com/article\""
  exit 1
fi

FILE=$1
TITLE=$2
AUTHOR=$3
DATE=$4
SOURCE_URL=$5

# Generate topics based on file content
TOPICS=$(grep -i -o -E '(falls church|black history|segregation|civil rights|tinner hill|integration|schools|mary ellen henderson|historical|education)' "$FILE" | sort | uniq | tr '\n' ',' | sed 's/,/, /g' | sed 's/, $//')

if [ -z "$TOPICS" ]; then
  TOPICS="Falls Church history"
fi

# Create temporary file
TMP_FILE=$(mktemp)

# Add front matter and original content
cat > "$TMP_FILE" << EOF
---
title: "$TITLE"
author: "$AUTHOR"
date: "$DATE"
source: "$SOURCE_URL"
topics: "$TOPICS"
---

EOF

# Append the original content
cat "$FILE" >> "$TMP_FILE"

# Replace the original file
mv "$TMP_FILE" "$FILE"

echo "Front matter added to $FILE"
echo "Title: $TITLE"
echo "Author: $AUTHOR"
echo "Date: $DATE"
echo "Source: $SOURCE_URL"
echo "Topics: $TOPICS" 