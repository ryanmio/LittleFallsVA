---
factor: "R"
dataset_id: "patents_2mi_buffer_1650-1739"
evidence_type: "Northern Neck patents"
k:            # successes (integer)
n:            # trials (integer)
alpha0: 1     # hyperprior α (default 1)
beta0: 1      # hyperprior β (default 1)
alpha:        # alpha0 + k
beta:         # beta0 + n - k
mean:         # alpha / (alpha + beta)
ci_lower:     # 2.5th percentile
ci_upper:     # 97.5th percentile
sources:
  - "GeoHack coordinates for Big Chimneys, https://geohack.toolforge.org/geohack.php?pagename=Big_Chimneys&params=38_52_56.56_N_77_10_29.34_W_"
  - "Camp, Shirley W. \"Colonial Land Grants and Their Owners or Tenants.\" Falls Church Historical Commission, May 1994."
notes: |
  Buffer radius 2 mi (3.22 km) centered at 38.882378, -77.174817 (38°52'56.56"N, 77°10'29.34"W).
  This location corresponds to the traditional site of Big Chimneys, now Big Chimneys Park in Falls Church.
  Coordinate validation was performed using GeoHack and Google Maps.
---
### Summary

Based on historical research from the Falls Church Historical Commission's document "Colonial Land Grants and Their Owners or Tenants" (1994), the earliest documented land grants within the present boundaries of Falls Church date from the 1720s, not 1699. The document provides strong evidence regarding the regional settlement patterns in the area, which directly informs our analysis of Factor R.

#### Key findings on early patents within our 2-mile buffer:

1. **Prior to 1724**: "Prior to 1724 there were no registered grants within the boundaries of the City of Falls Church." This directly contradicts the 1699 settlement claim, as formal land ownership would typically follow habitation.

2. **First recorded grant**: "The first recorded grant within the City of Falls Church was to Captain Simon Pearson (c. 1688-1733) on August 1, 1724 (NN Grant, #108)." This establishes 1724, not 1699, as the earliest documented European claim to the land.

3. **Other early grants**:
   - John Harle/Hurle received a grant on March 8, 1728 (NN Grant, #166)
   - William Gunnell received grants in 1729 (NN Grants #184, #185)
   - Thomas Harrison, Junior acquired 270 acres near Falls Church in 1731 (NN Grant #270)
   - Michael Reagan received a grant in the Falls Church area (NN Grant #187)
   - George Harrison received a grant in 1742 (NN Grant #338)

4. **Settlement patterns**: Early settlement occurred along rivers where travel was easier. The document notes: "As the good land along the rivers had been taken, persons then began to move inland where there was arable land." This pattern suggests the Falls Church area, being inland, would have been settled later than riverfront properties.

5. **Population context**: "In 1700 there were about 50,000 persons in Virginia. By 1720 the population was estimated to have doubled." This population growth in the 1710s-1720s aligns with the timing of the first formal land grants in the Falls Church area.

6. **Squatters and early occupation**: While the document acknowledges "there was nothing to prevent a squatter from tilling the soil wherever he chose," evidence of such activity in Falls Church before the 1720s is absent. The document mentions Sampson Darrell's "frontier plantation at Pimmit's (Run) in 1692" but notes he "did not record a grant until 1715," showing a significant gap between occupation and formal registration.

7. **Indian presence**: The document notes an "Indian poison field" mentioned in the 1724 Pearson deed, referring to areas where Native Americans had burned over hunting grounds. This suggests Native American activity in the area prior to European settlement.

This evidence suggests a timeline of European settlement in the Falls Church area beginning in the 1720s, with formal land patents recorded from 1724 onward. There is no documentary evidence of European settlement specifically at the Big Chimneys location in 1699.

This dataset will examine land patents within a 2-mile buffer of the traditional Big Chimneys location to determine the probability of regional habitability during the target period (1669-1729).

Key questions to be addressed:
1. What is the earliest documented patent within the buffer zone?
2. What percentage of land was patented by decade?
3. How does the patent timeline compare to neighboring areas? 