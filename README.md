# Urban Strip Mall Redevelopment Index
# Executive Summary:
This script is a prioritization tool that identifies and analyzes low-density commercial parcels (“strip malls”) for redevelopment by scoring them from 0-10. Prioritization takes place through a customizable index that includes land assessed value, building density of the surrounding environment, consolidation opportunities for neighboring sites, and land vacancy rate of the parcel. Users rank these four priorities to tailor the outcome of the scores to reflect their objectives. Organizations are left with a ranked list of properties for further research into redevelopment opportunities.

# Background
With nearly a half-century of urban “renewal” policies promising to revitalize America’s cities, the programs’ impacts have had a questionable effect. In many instances, entire blocks- even neighborhoods- were razed to make room for newer, flashier buildings. The high density, mixed-use structures lining commercial corridors in urban centers were often labelled as “blight”, removed and replaced by lower density structures or just left as overgrown lots. Removing the core threads of a neighborhood weakens the urban fabric of a city, with urban renewal acting as an unraveling force as opposed to a strengthening one. These land use policies imposed a vision of the ideal urban planning doctrine of the time: low density, segregated land uses that prioritize automotive infrastructure over pedestrian accessibility. 

Post-urban renewal policies have brought a renewed sense of importance for urban commercial corridors. Cities with strong bones- sound structures that once supported adaptive, walkable communities- are becoming attractive to residents, local governments, and investors. For residents, the block that was once bulldozed and replaced with a car-dependent strip mall is viewed as an eyesore in need of new buildings. For investors, an old, run-down building may have adverse side effects on neighboring property values, reducing their willingness to invest. For local governments, low-density parcels may mean low tax revenue. In any case, low-density parcels present an opportunity for redevelopment and growth.

This project was built within the context of Syracuse, NY, a rustbelt city of around 150,000 four hours north of New York City. Once an industrial powerhouse, Syracuse’s population has fallen by nearly 50%, with wealth and residents retreating to the neighboring suburbs. Property values remain low, commercial corridors- both strip-malls and legacy mixed-use- remain dilapidated, and vacant properties remain overgrown. Syracuse’s path to redevelopment reflects a broader trend of rustbelt cities along the Great Lakes: like many of them, it faces new opportunities for adaptive growth in the coming decades. New investment from educational institutions, the removal of divisive interstates, and the prospect of a micro-chip manufacturing plant are once in a lifetime opportunities to kickstart growth. With new opportunities come new challenges, such as gentrification and displacement, but also leave a cash-strapped city with the need for a tool to help prioritize resources investment. This project seeks to assist cities like Syarcuse in determining how to best prioritize investments to ultimately take advantage of these opportunities.

# Factors for Analysis
The index relies on four factors to judge a property’s prioritization for redevelopment: land assessed value, building density of the surrounding environment, consolidation opportunities for neighboring sites, and land vacancy rate of the parcel. Land assessed value indicates the value (in USD) of the land, which is normalized as the value per area unit (meters squared). This economic indicator is useful for potential cost estimation for acquisition and redevelopment. Density of the surrounding environment calculates density as a proximity to residential units by tallying the number of redevelopment candidates in each block group, dividing by the number of residential units in a block group, and assigning the ratio to each parcel. Density provides users with a gauge of how the built environment may impact the number of residents served. Consolidation of neighboring sites judges if multiple redevelopment opportunities exist alongside each other, which reflects an opportunity to assist with site selection. Finally, vacancy rate of the parcels calculates the percent of the parcel that is unused land, which illustrates the size and utilization rate of the parcel given its current building footprints.

# Input.json: 
Complete the keys in this file first. The input.JSON file contains input variable definitions that can be altered to reflect the structure of the organization’s input files, as well as changing the index rankings to reflect organizational priorities. The first grouping of keys are slots to insert the unique file names of an organization’s parcel file (.zip), building footprints data (.json), and block group file (.zip). The second grouping of keys adapt the columns of the organization’s parcel file to the terminology used by the parcel identifier script. The final grouping of keys allows the organization to tailor the factors of the index to the organizational priorities. Users should rank each of the four facets on a scale of 4 (most important) to 1 (least important) and ensure that the final score adds up to ten.

# Script 1: Parcel-Identifier.py
Run this script first. Parcel-Identifier.py filters a parcel dataset to identify low density commercial properties and computes key factors that are incorporated into the index. The script outputs a cleaned parcel and building footprints geopackage that are imported into the index script and used to create maps in the visuals script. 

# Script 2: Redevelopment-Index.py
Run this script second. Redevelopment-Index.py incorporates the weighted scores of the user’s priorities and applies them to the factors calculated in Parcel-Identifier.py. The script normalizes the scores for each of the factors on a scale of 0-1 based on quartile distribution of the data, if they are not already normalized. This value is then multiplied by the priority scores to be given a final score out of 10 and ultimately exported as a CSV and geopackage file. 

# Script 3: Visuals.py
Run this script third. Visuals.py creates a table showing the top 25 scores, a graph showing the distribution of scores, and two maps showing the geographical location of the eligible candidates.

# Output Example: Syracuse, NY
The script was initially developed with data illustrating the city of Syracuse, NY. Parcel data was sourced through the City of Syracuse’s Open Data Portal, building footprint data from Cornell University, and block group data from the US Census Bureau. All maps are projected with UTM18N. 

# Table 1: 
This table shows the top 25 properties ranked by final index score. Based on the chosen factor rankings, high scoring properties should be interpreted as better candidates for redevelopment than lower scoring properties.

# Graph 1:
![graph] https://github.com/npiro527/redevelopment-index/blob/main/score_distribution.jpg
This graph shows the distribution of all scores in the dataset. The bins reflect full value scores, which are rounded to the whole value of the score (ex. 3.47 is displayed as a 3). The graph provides important contextualization when interpreting the results or performing statistical analysis.

# Map 1:
![map1] https://github.com/npiro527/redevelopment-index/blob/ef9ff53e63da4f49ea0ff97254388faf521fc39d/eligible_parcels.jpg
This map shows the location of the redevelopment candidates compared to the total parcel map. Locational information may help visualize the geographical distribution of candidate properties.

# Map 2:
![map2] https://github.com/npiro527/redevelopment-index/blob/ef9ff53e63da4f49ea0ff97254388faf521fc39d/parcels_index_map.jpg
This map shows the location and score of the redevelopment candidates on a scale of green (10) to red (4). The information is based on the bins identified when creating Graph 1. The map provides further information on the grouping and geographical distribution of the candidate properties.

# Limitations and Future Improvements:
One immediate limitation of the Parcel-Identifier script is the filtering of all parcels by land use and zoning code. For Syracuse, I first sorted by “commercial” and “1 use small”, which returned many strip malls, but also returned vacant parcels and industrial sites. Calculating building footprints also assumes the accuracy of footprint data. The spatial join resulted in many parcels having no building structure, even when field observations showed a structure on the property. Additionally, focusing on land assessed value as opposed to total assessed value helps users understand the underlying value of their property, but does not account for reassessment history. Future versions of the script may wish to refine the initial filter, source more accurate building footprint data, and factor in other value trackers, such as market value or changes in assessed value.

# Data Sources:
City of Syracuse Parcel Data: https://data.syr.gov/datasets/addb85afc6a14daca340c4ae0077e998_0/explore

Onondaga County Building Footprints: https://cugir.library.cornell.edu/catalog/cugir-009065

New York State Block Groups: https://www2.census.gov/geo/tiger/TIGER2020/BG/
