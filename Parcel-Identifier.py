# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 15:29:17 2025

@author: npiro
"""

# This script loads data and identifies parcels to be included in the index
## Universality Notes (with double ##): json or csv as an input file, dictionary w/ name of parcel file


# Load in packages and set defaults
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import requests
import seaborn as sns
import fiona

plt.rcParams['figure.dpi'] = 300

#%%
# Import data
## Use json and csv for editing before adding, converting both to geopackages
parcels = gpd.read_file("Syracuse_Parcel_Map_(Q4_2024).zip")
parcels.to_file("parcels.gpkg", driver="GPKG")
#parcels = parcels.set_index('PRINTKEY')

#%%
# Summary/workspace
        #layers = fiona.listlayers("Syracuse_Parcel_Map_(Q4_2024).zip")
        #parcelcodes = parcels["LU_parcel"].value_counts()
        #parcelcodes2 = parcels["LUCat_Old"].value_counts()

#%%
# Query by "Commercial" zoning code
commercial = parcels.query("LUCat_Old == 'Commercial'")
print("\nNumber of Properties Zoned Commercial:", len(commercial["FID"]))

# Query by "single-use" land use
lowdensity = commercial.query("LU_parcel == '1 use sm bld'")
print("\nNumber of Properties with Small Density Land Use:", len(lowdensity["FID"]))
    # Smallest queryable QPD column that reflects density

#%%
# Calculate percent of parcel vs land area

# Define projection code for utm18n
utm18n = 32618

# Read and project building footprints and lowdensity
footprints = gpd.read_file("cugir-009065-geojson.json")
footprints = footprints.to_crs(epsg=utm18n)
lowdensity = lowdensity.to_crs(epsg=utm18n)

# Calculate area of footprints and lowdensity in meters squared (m2)
footprints['fpaream2'] = footprints.geometry.area
lowdensity['ldaream2'] = lowdensity.geometry.area

# Join low density identifiers to footprints
ldin = lowdensity[["PRINTKEY", "geometry"]]
footprintsld = footprints.sjoin(ldin, how='inner', predicate='within')

# Calculate building footprints by area
fp_by_parcel = footprintsld.groupby("PRINTKEY")["fpaream2"].sum()
lowdensity = lowdensity.set_index("PRINTKEY").join(fp_by_parcel, how="left")

# Add vacant land characteristics to lowdensity
lowdensity["vacantaream2"] = lowdensity["ldaream2"] - lowdensity["fpaream2"]
lowdensity["vacantpct"] = lowdensity["vacantaream2"] / lowdensity["ldaream2"]

# Clean output and account for zeroes (vacants?)
lowdensity["fpaream2"] = lowdensity["fpaream2"].fillna(0)
    # parcels with no building footprints should have a footprint area of zero
lowdensity["vacantaream2"] = lowdensity["vacantaream2"].fillna(lowdensity["ldaream2"]) 
    # parcels with no vacant area are assumed to be fully built, meaning their developed area should match the parcel area
lowdensity["vacantpct"] = lowdensity["vacantpct"].fillna(1)
    # parcels with vacant areas that match the parcel area are assumed to be fully built, meaning percent of vacant land should be 100%

# Print summary statistics
print("\nAverage Vacant Area per Parcel:", lowdensity["vacantpct"].mean() * 100, "%")
filtered_lowdensity = lowdensity[lowdensity["vacantpct"] <1.0]
print("\nAverage Vacant Area per Parcel (Excluding 100% Vacants):", filtered_lowdensity["vacantpct"].mean() * 100, "%")

#### how to intrepret zeroes: vacants?, footprint data incomplete per streetview
#%%
# Loop through parcels to see if one parcel touches another
lowdensity["shared_boundary"] = False
for idx, parcel in lowdensity.iterrows():
    others = lowdensity.drop(idx)
    
    if others.geometry.touches(parcel.geometry).any():
        lowdensity.at[idx, "shared_boundary"] = True
   
#%%
# Calculate assessed value of land per square meter
lowdensity["avperm2"] = lowdensity["land_av"] / lowdensity["ldaream2"]
print("\nAverage Land Assessed Value per Square Meter", lowdensity["avperm2"].mean())
#%%
# One proximity indicator

#%%
# Save files
#%%
# Create a plot
fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
lowdensity.plot(ax=ax, edgecolor="blue", facecolor="blue", linewidth=0.5, alpha=0.7)

# Remove axes for a clean look
ax.axis("off")
ax.set_title("Parcel Footprints")

# Show the map
plt.show()

#%%
# Calculate setbacks from road?
    # Load in road data, then calculate setback from centroid
# Calculate proximity

# Index walkscore?, assessed value, percent of land as parking, sales tax, proximity
# Definition of strip mall? Theoretical and 

