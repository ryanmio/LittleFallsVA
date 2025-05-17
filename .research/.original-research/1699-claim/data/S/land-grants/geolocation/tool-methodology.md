## AI-Powered Location Extraction

### Text Analysis with Large Language Models

The system uses OpenAI's GPT-4 model to analyze historical land grant descriptions, which often contain archaic language, complex geographical references, and non-standardized location descriptions.

#### Prompt Engineering

The AI is provided with a specialized prompt designed to:

1. Focus on extracting the location of the land grant itself (not the origins of people mentioned)
2. Identify natural features (creeks, rivers, etc.) that define the land's location
3. Determine the historical county
4. Format the extracted information in a structured way for geocoding

The prompt instructs the model to return a JSON object with the following fields:
- `extractedLocation`: The specific place where the land grant is located
- `county`: The county where the land is located (for fallback)
- `geocodingQuery`: A properly formatted query for the geocoding API
- `naturalFeature`: The specific natural feature without county information

Example prompt excerpt:
\`\`\`
You are an expert in historical geography and land records from colonial Virginia.
Analyze the following historical land grant entry and extract ONLY the location of the LAND GRANT itself (not where people are from):

[Raw land grant text]

For the geocodingQuery field, follow these EXACT formatting rules:
1. Start with the most specific natural feature (creek, river, swamp, etc.)
2. Follow with the county name
3. End with "Virginia"
4. Format as: "[Natural Feature], [County] County, Virginia"
\`\`\`

### Response Processing

The AI's response is parsed to extract the structured location data. The system handles various response formats, including direct JSON or JSON embedded in markdown code blocks.

## Multi-Strategy Geocoding

The system employs a cascading series of geocoding strategies to maximize the chances of finding accurate coordinates.

### Strategy 1: Natural Feature-Specific Geocoding

This strategy focuses on locating specific natural features mentioned in the land grant.

1. Creates multiple query variations to increase chances of finding the natural feature:
   - `[Natural Feature] point, [County] County, Virginia`
   - `[Natural Feature], [County] County, Virginia`
   - `[Natural Feature] water feature, [County] County, Virginia`

2. Uses Google Maps Geocoding API with natural feature bias
3. Filters results to prioritize natural features and water bodies
4. Verifies the result is within Virginia

### Strategy 2: Enhanced Geocoding with Virginia Restriction

If Strategy 1 fails, the system attempts a more general approach:

1. Uses the AI-generated geocoding query with added historical context
2. Restricts results to Virginia using the `components=administrative_area:VA|country:US` parameter
3. Filters results to prioritize natural features and non-administrative areas
4. Verifies the result is within Virginia

### Strategy 3: Standard Geocoding with Virginia Restriction

If Strategy 2 fails, the system falls back to standard geocoding:

1. Uses the AI-generated geocoding query
2. Restricts results to Virginia
3. Takes the first result that is verified to be in Virginia

### Strategy 4: County-Level Fallback

As a last resort, if all other strategies fail:

1. Uses only the county name with "Virginia"
2. Provides at least county-level coordinates when more specific locations cannot be determined

## Virginia Verification

All geocoding results undergo verification to ensure they are within Virginia:

1. Checks address components for "VA" or "Virginia" as administrative_area_level_1
2. Also checks the formatted address as a backup
3. Flags any results that appear to be outside Virginia

## Confidence Scoring and Validation

### Confidence Metrics

The system assigns confidence scores based on:
1. The type of geocoding strategy that succeeded
2. The location type returned by the geocoding API
3. Whether the result is a natural feature or administrative area

### Distance Error Calculation

When original coordinates are available in the input data, the system calculates a distance error:

1. Uses the Haversine formula to calculate the distance between original and calculated coordinates
2. Categorizes results by error distance:
   - High accuracy: < 1km
   - Medium accuracy: 1-10km
   - Low accuracy: > 10km

## Technical Implementation

### API Integration

The system integrates with two key external APIs:

1. **OpenAI API**: For text analysis and location extraction
   - Model: GPT-4.1-2025-04-14
   - Temperature: Default (optimized for factual responses)
   - Max tokens: Sufficient for comprehensive analysis

2. **Google Maps Geocoding API**: For converting location descriptions to coordinates
   - Uses region biasing to Virginia
   - Uses component filtering to restrict to Virginia, USA
   - Implements timeout handling to prevent hanging requests