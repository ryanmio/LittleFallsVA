# Cavaliers and Pioneers Patent Abstracts

## Data Source

This folder contains OCR'd text files from "Cavaliers and Pioneers" by Nell Marion Nugent, a multi-volume compilation of abstracts of Virginia land patents and grants. The current dataset includes:

- `cavalierspioneer00nuge_djvu.txt` - Full OCR text from Internet Archive
- `cavalierspioneer00nuge_hocr_searchtext.txt` - Cleaner OCR text used for processing

## Important Limitations

### 1. Volume Limitations

The OCR'd text files available only contain **Volume I (1623-1666)** of Nugent's compilation. The full series consists of:

- **Volume 1**: 1623-1666 ✓ (available)
- **Volume 2**: 1666-1695 ✗ (not available in OCR'd form)
- **Volume 3**: 1695-1732 ✗ (not available in OCR'd form)
- **Volumes 4-7**: Later periods to 1776 ✗ (not available)

For research on the Falls Church area circa 1699, **Volumes 2 and 3** would be the most relevant, but they are not currently available in our OCR'd dataset.

### 2. Missing Northern Neck Proprietary Grants

Due to the volume limitations, the dataset lacks many Northern Neck Proprietary grants (Lord Fairfax's proprietary territory), which are crucial for understanding land ownership in Fairfax, Prince William, Stafford, and other Northern Virginia counties in the late 17th and early 18th centuries.

### 3. OCR Quality

The OCR quality varies throughout the text, affecting the reliability of data extraction. While major entries are generally captured correctly, there may be issues with dates, acreages, or grantee names.

## Extracted Data

We have processed the available OCR'd text to extract the following:

- `northern_va_land_grants_1660_1730.csv` - CSV file with land grant data
- `northern_va_land_grants_summary.md` - Overview of findings with charts

## Options for Obtaining Missing Volumes

### 1. Purchase Physical Copies

The missing volumes are available for purchase as hardcover books:
- Volume 2 (1666-1695): ~$48-50 from Amazon, eBay, and specialty book sellers
- Volume 3 (1695-1732): ~$50 from specialty book sellers
- Complete set (Volumes 2, 4, 6): ~$100 on eBay

### 2. Library Access

- Check local university libraries and genealogical societies
- Virginia public libraries may have these volumes available
- Interlibrary loan services may be able to obtain them temporarily

### 3. DIY Digitization

If purchasing physical copies, you could digitize them using:
- Book scanner or high-quality camera: $200-500
- Lighting setup: $50-100
- OCR software: Free options like Tesseract exist
- Estimated processing time: 10-20 hours

### 4. Direct Access to Original Records

Alternatively, consider accessing the original grant records directly:
- Library of Virginia's Land Office Patents collection
- Northern Neck Grant Books (for the proprietary territory)
- County court records for early Northern Virginia counties

## Processing Methodology

Data extraction was performed using regular expressions to identify and parse land grant entries. The extraction code is available in the `abstracts_workflow` directory, which has been updated to handle multiple volumes if/when they become available.

## Next Steps

1. Obtain missing volumes (2 and 3) through purchase or library access
2. Extract data using our existing script, which is ready to process additional volumes
3. Update the summary with more comprehensive data including the critical 1666-1732 period 