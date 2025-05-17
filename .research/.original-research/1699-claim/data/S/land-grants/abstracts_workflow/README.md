# Northern Virginia Land Grants Abstracts Workflow

## Overview

This toolset extracts structured data from text-based OCR'd land grant abstracts from "Cavaliers and Pioneers" by Nell Marion Nugent. The workflow focuses on identifying and parsing land grants in Northern Virginia counties during the period 1660-1730, to evaluate the historical plausibility of settlement around Falls Church circa 1699.

## Data Source

We're processing data from the multi-volume "Cavaliers and Pioneers" compilation:

- **Volume 1** (1623-1666): Available as OCR'd text from Internet Archive
  - `cavalierspioneer00nuge_hocr_searchtext.txt`
- **Volume 2** (1666-1695): Not currently available in OCR'd form
- **Volume 3** (1695-1732): Not currently available in OCR'd form

**Important:** Currently, only Volume 1 is processed in our workflow. Our script has been updated to handle additional volumes when they become available.

## Workflow Process

1. **Text Extraction**: Parse the OCR'd text to identify individual land grant entries.
2. **Data Extraction**: For each entry, extract:
   - Grantee name
   - Acreage
   - County
   - Grant date
   - Full text snippet
   - Volume source
3. **Filtering**: Focus only on grants in Northern Virginia counties, including:
   - Fairfax, Loudoun, Prince William, Stafford, Westmoreland
   - Northumberland, Lancaster, Richmond, King George
   - Arlington, Alexandria
4. **Date Range Filtering**: Include only grants from 1660-1730
5. **Output Generation**:
   - CSV file with structured data
   - Summary markdown file with chronological statistics

## Usage

Run the extraction script:

```bash
python process_patent_abstracts.py
```

This will:
1. Process available volumes (currently only Volume 1)
2. Extract and parse land grant information
3. Output a CSV file to `../northern_va_land_grants_1660_1730.csv`
4. Generate a summary to `../northern_va_land_grants_summary.md`

### Custom Paths

You can specify custom input and output paths:

```bash
python process_patent_abstracts.py --input /path/to/input.txt --output /path/to/output.csv --summary /path/to/summary.md
```

## Output Files

1. **CSV File**: Contains structured data with the following fields:
   - `grantee`: The name of the person receiving the land grant
   - `acreage`: The size of the grant in acres
   - `county`: The county where the grant is located
   - `date`: The date of the grant in YYYY-MM-DD format
   - `snippet`: A text excerpt from the original entry
   - `volume`: The source volume (e.g., "Volume 1")

2. **Summary Markdown**: Contains statistical analysis including:
   - Number of grants per decade
   - Total grants in Northern Virginia during the period
   - Notes on data quality and limitations

## Notes and Limitations

- **Volume Limitations**: Currently only Volume 1 (1623-1666) is processed. The most relevant data for the 1699 Falls Church research would be in Volumes 2 and 3 (1666-1732), which are not yet available in our dataset.
- **OCR quality** varies throughout the text, which may affect extraction accuracy
- **County boundaries** changed over time; grants may be assigned to modern counties
- **Northern Neck Proprietary grants** (Lord Fairfax) are mostly absent from Volume 1 and would be found in Volumes 2-3
- Some grants lack clear county information and may be missed in the filtering process

## Future Improvements

1. **Obtain and process Volumes 2-3**: These contain the most relevant time period (1666-1732) for our research
2. **Integrate Northern Neck grant data**: Consider direct extraction from Northern Neck Grant Books
3. **Improve county identification**: Enhance the algorithm to better handle historical county names and boundary changes

## Relationship to Research Question

This data will directly inform a Bayesian analysis regarding the historical plausibility of European settlement in the Falls Church area around 1699. By analyzing the chronological and geographic distribution of land grants, we can establish a probability framework for settlement patterns in the region. 