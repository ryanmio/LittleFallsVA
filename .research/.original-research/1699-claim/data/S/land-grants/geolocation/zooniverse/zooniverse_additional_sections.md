# Additional Zooniverse Project Sections

## Workflow Description
In this workflow, you'll help locate colonial Virginia land grants from the early 18th century. Each task presents you with a historical text description of a land parcel and an interactive map. Your goal is to place a marker at the most likely location of the grant based on geographical clues in the text. You'll also rate your confidence in your placement. Each grant will be reviewed by multiple volunteers to ensure accuracy.

## Researcher Quote
"These land grant records represent the earliest documented European settlement patterns in Virginia, but they've never been systematically mapped. With the help of citizen scientists, we can finally visualize this critical period of American history while also testing whether AI systems can interpret historical geography as effectively as human researchers."

## Discipline Tag
History

## Research Page Content

# Mapping Virginia's Colonial Frontier: Citizens and AI

## The Challenge of Historical Geography

Colonial land grant records contain some of our most detailed information about early American settlement, but they've remained largely untapped by spatial historians. Why? Because turning a text description like "400 acres on the South side of Nottoway River, adjacent to John Smith's line" into precise coordinates is extremely difficult.

Between 1700-1735, thousands of land patents were issued throughout Virginia as settlement expanded westward from the Tidewater region. Each record in the patent books contains a brief description of the parcel's location, typically mentioning:

- Nearby rivers, creeks, or swamps
- Adjacent landowners
- Natural landmarks (mountains, ridges, distinctive trees)
- Parish or county boundaries
- Distances and directions (though rarely in a complete way)

These descriptions were sufficient for surveyors and neighbors at the time, but mapping them today requires significant detective work.

## Why This Matters

By creating the first comprehensive spatial dataset of early Virginia land grants, we unlock new possibilities for historical research:

1. **Settlement Patterns**: Track how European colonization moved inland along waterways, revealing the environmental and economic logic behind expansion.

2. **Historical Networks**: Identify clusters of related families, economic connections, and community formation.

3. **Indigenous Displacement**: Document the progressive encroachment on Native American territories and preservation of indigenous place names.

4. **Modern Geography**: Many current towns, county boundaries, and even property lines originated during this period.

5. **Environmental History**: Land grant descriptions often mention now-lost ecological features like meadows, swamps, and old-growth forests.

[INSERT SAMPLE IMAGE: Early Virginia map with sample land grant locations]

## Testing Artificial Intelligence on Historical Texts

This project has a second, cutting-edge dimension: we're testing whether modern artificial intelligence can effectively interpret historical geography.

Large language models (like GPT-4 and Claude) have demonstrated remarkable abilities to understand modern geography. But can they accurately locate places from centuries-old descriptions written in colonial English, referencing landmarks that may no longer exist?

Your classifications provide the essential "ground truth" that allows us to measure AI performance. For each land grant, we'll:

1. Have human volunteers (you!) determine the most likely location
2. Ask various AI systems to interpret the same text
3. Measure the distance between human and AI placements
4. Analyze which types of descriptions humans find easier or harder than AI

This comparison will help us understand the current limitations of AI for historical research and potentially identify ways to improve these systems for humanities scholarship.

## Your Contribution

Each pin you place on the map advances both traditional historical geography and cutting-edge AI research. Multiple volunteers will classify each grant, allowing us to measure human consensus and uncertainty.

The final dataset—combining human expertise across hundreds of classifications—will be openly published with full credit to Zooniverse volunteers. Your work will enable future researchers to study this pivotal period of American history with unprecedented spatial detail.

## Project Team and Partners

This research is conducted by the Little Falls Historical Society in collaboration with digital humanities scholars at the University of Virginia. The project builds on previous work digitizing the Virginia land patent books and creating GIS layers of colonial parishes and counties.

[INSERT IMAGE: Team photo or institutional logos]

## Further Reading

If you're interested in learning more about colonial Virginia geography or the use of AI in historical research:

- Morgan, Edmund S. (1975). *American Slavery, American Freedom: The Ordeal of Colonial Virginia*
- Hofstra, Warren R. (2004). *The Planting of New Virginia: Settlement and Landscape in the Shenandoah Valley*
- Gregory, Ian N. & Geddes, Alistair (2014). *Toward Spatial Humanities: Historical GIS and Spatial History*
- Blevins, Cameron (2021). *Paper Trails: The US Post and the Making of the American West*

Thank you for contributing to this groundbreaking research at the intersection of historical geography and artificial intelligence!

## Subject Set Instructions

Yes, you'll need to upload your list of 50 land grant descriptions as a "Subject Set." Here's how to prepare your data:

1. **Create a CSV file** with the following columns:
   - `raw_entry`: The complete text of the land grant description
   - `volume`: Book volume (for reference)
   - `book`: Book number (for reference)
   - `set`: Should all be "test" for consistency
   - Optional: Include any other reference columns you want to keep with the data

2. **On the Zooniverse platform**:
   - Go to the "Subject Sets" tab in your project builder
   - Click "New Subject Set" and give it a name (e.g., "Colonial Virginia Land Grants Test Set")
   - Upload your CSV file
   - Map the columns to the appropriate fields in the Zooniverse interface
   - Make sure to set "raw_entry" as the main text to display to volunteers

3. **Link your Subject Set to your Workflow**:
   - In the Workflow tab, select your workflow
   - Under "Subject Sets," assign your newly created set
   - This connects your data to the task interface you've designed

Zooniverse will automatically:
- Distribute tasks to multiple volunteers
- Track completed classifications
- Allow you to export the results with coordinates and confidence ratings

When designing your CSV, consider including a unique ID for each land grant to make it easier to match volunteer classifications with your original data during analysis. 