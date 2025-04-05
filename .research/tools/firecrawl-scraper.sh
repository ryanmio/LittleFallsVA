#!/bin/bash

# Script to automatically scrape multiple URLs with Firecrawl and extract markdown content
# Updated to include specific URLs for Falls Church history research

# Check if API key is set
API_KEY="fc-ed88ac7645374dfd86cbef95f93f5001"
if [ -z "$API_KEY" ]; then
  echo "Error: Firecrawl API key not set"
  exit 1
fi

# Base directory for research files
BASE_DIR=".research"

# Function to create a filename from URL
get_filename() {
  local url=$1
  local filename=$(echo "$url" | sed -E 's/https?:\/\/(www\.)?//g' | sed -E 's/\//-/g' | sed 's/\./-/g')
  echo "$filename"
}

# Function to get directory based on domain
get_directory() {
  local url=$1
  if [[ "$url" == *"fallschurchpulse.org"* ]]; then
    echo "$BASE_DIR/Falls Church Pulse"
  elif [[ "$url" == *"fcnp.com"* ]]; then
    echo "$BASE_DIR/Falls Church News Press"
  else
    echo "$BASE_DIR/Other Sources"
  fi
}

# Function to scrape a URL
scrape_url() {
  local url=$1
  local output_dir=$(get_directory "$url")
  local filename=$(get_filename "$url")
  
  # Create output directory if it doesn't exist
  mkdir -p "$output_dir"
  
  echo "Scraping $url..."
  
  # Run the curl command to get the JSON data
  curl -s -X POST https://api.firecrawl.dev/v1/scrape \
    -H 'Content-Type: application/json' \
    -H "Authorization: Bearer $API_KEY" \
    -d "{\"url\": \"$url\", \"formats\": [\"markdown\"]}" > "$output_dir/${filename}.json"
  
  # Check if curl was successful
  if [ $? -ne 0 ]; then
    echo "Error: Failed to scrape URL: $url"
    return 1
  fi
  
  # Extract markdown content from JSON
  cat "$output_dir/${filename}.json" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'data' in data and 'markdown' in data['data']:
        print(data['data']['markdown'])
    else:
        print('Error: No markdown content found in JSON response')
        exit(1)
except Exception as e:
    print(f'Error parsing JSON: {e}')
    exit(1)
" > "$output_dir/${filename}.md"
  
  # Check if extraction was successful
  if [ $? -ne 0 ]; then
    echo "Error: Failed to extract markdown content from $url"
    return 1
  fi
  
  echo "Success! Created files for $url:"
  echo "JSON: $output_dir/${filename}.json"
  echo "Markdown: $output_dir/${filename}.md"
  echo ""
}

# URLs to scrape
URLS=(
  "https://fallschurchpulse.org/new-public-artwork-2024/"
  "https://fallschurchpulse.org/tinner-hill-historic-and-cultural-district/"
  "https://www.fcnp.com/2005/10/06/me-costner-leads-first-class-of-black-students-following-approval-by-falls-church-school-board"
  "https://www.fcnp.com/2005/09/25/meeting-john-a-johnson-unsung-hero-in-falls-churchs-1950s-struggle-to-integrate-its-schools"
  "https://www.fcnp.com/2017/10/11/program-dedication-found-new-gm-high-school-65-years-ago"
)

# Process each URL
echo "Starting batch processing of URLs..."
echo "-------------------------------------"
for url in "${URLS[@]}"; do
  scrape_url "$url"
done

echo "Batch processing complete!"
echo "Don't forget to add front matter to each markdown file."
echo "-------------------------------------" 