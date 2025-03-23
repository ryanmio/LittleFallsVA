#!/bin/bash

# Script to publish the next scheduled blog post
# To be run weekly via GitHub Actions or similar CI/CD platform

set -e  # Exit immediately if a command exits with a non-zero status

# 1. Find the oldest draft post by date
# First get all markdown files that are drafts
DRAFT_FILES=$(find drafts/english/press -name "*.md" -type f -exec grep -l "draft: true" {} \;)

if [ -z "$DRAFT_FILES" ]; then
  echo "No draft posts found"
  exit 0
fi

# Extract dates and filenames, then sort by date
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
  echo "No scheduled posts found with valid dates"
  exit 0
fi

echo "Publishing post: $NEXT_POST with date $EARLIEST_DATE"

# 2. Update the post status to published
# Use different sed syntax for Linux (GitHub Actions) vs macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS
  sed -i '' 's/draft: true/draft: false/g' "$NEXT_POST"
  
  # 3. Update the date to today
  TODAY=$(date +"%Y-%m-%d")
  sed -i '' "s/^date: .*/date: $TODAY/g" "$NEXT_POST"
else
  # Linux (GitHub Actions)
  sed -i 's/draft: true/draft: false/g' "$NEXT_POST"
  
  # 3. Update the date to today
  TODAY=$(date +"%Y-%m-%d")
  sed -i "s/^date: .*/date: $TODAY/g" "$NEXT_POST"
fi

# 4. Move the file to the content directory
POST_NAME=$(basename "$NEXT_POST")
DESTINATION="content/english/press/$POST_NAME"

cp "$NEXT_POST" "$DESTINATION"
rm "$NEXT_POST"

echo "Published post: $POST_NAME with current date: $TODAY"

# 5. Commit the changes
git add "$DESTINATION"
git commit -m "Published scheduled post: $POST_NAME"

# The push will trigger Netlify to rebuild and deploy
git push

echo "Changes pushed, Netlify build should start automatically" 