# Patent Metes and Bounds Collection

This directory contains patent metes and bounds data for land grants within a 2-mile buffer of Big Chimneys (38.882378, -77.174817).

## Purpose
- Collect precise boundary descriptions for all patents within the study area
- Document only information directly relevant to geolocation 
- Prepare data for GIS processing and mapping

## Organization Strategy
Each file in this collection follows these organizational principles:
- One file per distinct grant number or identifiable land parcel
- Files are named using the simple pattern: `[grantee]_grant.md` (e.g., `thomas_pearson_grant.md`)
- For multiple grants by the same person, a descriptor is added: `[grantee]_[descriptor]_grant.md` (e.g., `john_trammell_1727_grant.md`)
- Joint grants are filed under the primary grantee with co-grantees listed in the filename
- All files maintain the standard template format for consistency

## Documented Patents
Based on the Colonial Landgrants document, we've created files for the following grants:

### Confirmed Grant Numbers
1. Simon Pearson (1724) - `simon_pearson_108_grant.md` - First recorded grant within Falls Church boundaries
2. John Harle/Hurle (1728) - `john_harle_grant.md` - Small portion in Falls Church 
3. William Gunnell (1729) - `william_gunnell_184_grant.md` - Partially in Falls Church
4. William Gunnell (1729) - `william_gunnell_185_grant.md` - Partially in Falls Church
5. Michael Reagan (c.1730s) - `michael_reagan_grant.md` - Falls Church tract
6. Simon Pearson & Thomas Going (652 acres) - `simon_pearson_thomas_going_grant.md` - Within two miles of Falls Church
7. Thomas Harrison Jr. (1731, 270 acres) - `thomas_harrison_grant.md` - Small portion in Falls Church
8. Simon Pearson & Gabriel Adams Sr. (708 acres) - `simon_pearson_gabriel_adams_grant.md`
9. George Harrison (1742) - `george_harrison_grant.md` - Falls Church location
10. Thomas Pearson (660 acres on road to Alexandria) - `thomas_pearson_grant.md` - Father of Simon Pearson
11. Charles Broadwater - `charles_broadwater_grant.md` - Near Four Mile Run
12. Simon Pearson & William Fitzhugh (1409 acres) - `simon_pearson_fitzhugh_grant.md`

### Additional Properties (Grant Numbers Unknown or Different Format)
1. Sampson Darrell Grant (1715) - `sampson_darrell_grant.md` - At Pimmit's Run
2. John Trammell Grant (185 acres, 1727) - `john_trammell_1727_grant.md` - NN B:55
3. John Trammell "Cherry Hill" Grant (248 acres, 1729) - `john_trammell_1729_grant.md`
4. Gerrard Trammell Grant - `gerrard_trammell_grant.md` - In vicinity of Falls Church
5. Fitzhugh Ravensworth Grant (nearly 22,000 acres) - `fitzhugh_ravensworth_grant.md`
6. Daniel and Spence Neale Property - `daniel_spence_neale_grant.md` - Former Reagan property

## Data Sources
- Northern Neck Land Office Patents - Library of Virginia
- Fairfax County Land Records and Surveys
- Historic maps with property boundaries
- "Colonial Land Grants and Their Owners or Tenants" by Shirley W. Camp

## Next Steps
1. Locate original survey descriptions from Library of Virginia for all identified grants
2. Look for metes and bounds descriptions in deed books
3. Check if Fairfax GIS has digitized historical land patents
4. Consult "Record of Surveys, 1742-1856. Fairfax Circuit Court Archives, Fairfax, Virginia" (mentioned on p. 269)
5. Prepare data for polygon creation in GIS 