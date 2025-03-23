#!/bin/bash

# Test script for the publishing workflow
# This allows testing without pushing to git

set -e  # Exit immediately if a command exits with a non-zero status

echo "🔍 Testing the publishing workflow..."

# Check if directories exist
mkdir -p drafts/english/press
mkdir -p content/english/press

echo "📂 Checking for draft posts..."
DRAFT_FILES=$(find drafts/english/press -name "*.md" -type f -exec grep -l "draft: true" {} \; 2>/dev/null || echo "")

if [ -z "$DRAFT_FILES" ]; then
  echo "❌ No draft posts found"
  echo "👉 You should create a test post in drafts/english/press/ with 'draft: true' first"
  exit 1
fi

echo "✅ Found draft posts:"
for file in $DRAFT_FILES; do
  POST_DATE=$(grep "^date: " "$file" | sed 's/date: //g' | tr -d '"')
  echo "   - $file (date: $POST_DATE)"
done

# Find the post with earliest date
NEXT_POST=""
EARLIEST_DATE="9999-99-99"

for file in $DRAFT_FILES; do
  POST_DATE=$(grep "^date: " "$file" | sed 's/date: //g' | tr -d '"')
  if [[ "$POST_DATE" < "$EARLIEST_DATE" ]]; then
    EARLIEST_DATE="$POST_DATE"
    NEXT_POST="$file"
  fi
done

if [ -z "$NEXT_POST" ]; then
  echo "❌ No scheduled posts found with valid dates"
  exit 1
fi

echo "🔍 Would publish: $NEXT_POST (dated: $EARLIEST_DATE)"
POST_NAME=$(basename "$NEXT_POST")
TODAY=$(date +"%Y-%m-%d")

echo "✅ Test completed successfully!"
echo ""
echo "🚀 If this were a real run, the script would:"
echo "   1. Set draft: false in the file"
echo "   2. Update date to today ($TODAY)"
echo "   3. Move file to content/english/press/$POST_NAME"
echo "   4. Commit and push changes to trigger a Netlify build"
echo ""
echo "👉 To actually run the publish script, use:"
echo "   ./scripts/publish_next_post.sh" 