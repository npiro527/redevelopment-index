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
parcels = parcels.set_index('SBL')

#%%
# Summary/workspace
        #layers = fiona.listlayers("Syracuse_Parcel_Map_(Q4_2024).zip")
        #parcelcodes = parcels["LU_parcel"].value_counts()
        #parcelcodes2 = parcels["LUCat_Old"].value_counts()

#%%
# Query by "Commercial" zoning code
commercial = parcels.query("LUCat_Old == 'Commercial'")
print(commercial["FID"].value_counts())

# Query by "single-use" land use
lowdensity = commercial.query("LU_parcel == '1 use sm bld'")
print(lowdensity["FID"].value_counts())
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
footprints = footprints.sjoin(ldin, how='inner', predicate='within')

# Calculate building footprints by area
fp_by_parcel = footprints.groupby("PRINTKEY")["fpaream2"].sum()
lowdensity = lowdensity.set_index("PRINTKEY").join(fp_by_parcel, how="left")

# Add parking characteristics to lowdensity
lowdensity["parkingaream2"] = lowdensity["ldaream2"] - lowdensity["fpaream2"]
lowdensity["parkingpct"] = lowdensity["parkingaream2"] / lowdensity["ldaream2"]
lowdensity["parkingaream2"] = lowdensity["parkingaream2"].fillna(0)
lowdensity["parkingpct"] = lowdensity["parkingpct"].fillna(0)
lowdensity["fpaream2"] = lowdensity["fpaream2"].fillna(0)

#%%
# Loop through parcels to see if one parcel touches another
lowdensity["shared_boundary"] = False
for idx, parcel in lowdensity.iterrows():
    others = lowdensity.drop(idx)
    
    if others.geometry.touches(parcel.geometry).any():
        lowdensity.at[idx, "shared_boundary"] = True
        
#%%
# Plotting
#fig1,ax1 = plt.subplots(dpi=300)
#footprints.plot('geometry', edgecolor='gray', facecolor='none', linewidth=0.5, alpha=0.5, ax=ax1)
#ax1.axis('off')

    # convert footprint data to area, clip from one another

#%%
# Calculate setbacks from road?
    # Load in road data, then calculate setback from centroid

# Identifiers: AV, setback, area
    # By area (Density): commercial["Shape_Are"] / 

# Index walkscore?, assessed value, percent of land as parking, sales tax, proximity
# Definition of strip mall? Theoretical and 

