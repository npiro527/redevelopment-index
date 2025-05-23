# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 15:29:17 2025

@author: npiro
"""

# This script loads data and identifies parcels to be included in the index

#%%
# Load in packages and set defaults
import json
import geopandas as gpd
import matplotlib.pyplot as plt
import os

plt.rcParams['figure.dpi'] = 300
utm18n = 32618

# Define inputs from json file
info = json.load(open("Scripts/input.json"))
parcel_file = info["input_parcel"]
footprints_file = info["input_footprints"]
bg_file = info["input_block_grp"]

# Define output files
ld_out_file = "Output Files/ld_out_file.gpkg"
fp_out_file = "Output Files/fp_out_file.gpkg"

# Define output folder
os.makedirs("Output Files", exist_ok=True)

#%%
## Import data and join block groups information
# Import and project parcels data
parcels = gpd.read_file(parcel_file)
parcels.to_file("parcels.gpkg", driver="GPKG")
parcels = parcels.to_crs(epsg=utm18n)

# Import and project block groups data
blockgrps = gpd.read_file(bg_file)
blockgrps = blockgrps.to_crs(epsg=utm18n)

# Spatial join block groups to parcels
bgin = blockgrps[["GEOID", "geometry"]]
parcels = parcels.sjoin(bgin, how="left", predicate="within")

#%%
## Narrow parcels down by Commercial and Low Density
# Query by "Commercial" zoning code
commercial = parcels.query("LUCat_Old == 'Commercial'")
print("\nNumber of Properties Zoned Commercial:", len(commercial["FID"]))

# Query by "single-use" land use
lowdensity = commercial.query("LU_parcel == '1 use sm bld'")
print("\nNumber of Properties with Small Density Land Use:", len(lowdensity["FID"]))
    # Smallest queryable QPD column that reflects density

#%%
## Calculate percent of parcel vs land area
# Read and project parcels, building footprints, and lowdensity
footprints = gpd.read_file(footprints_file)
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

#%%
## Evaluate parcels to see if one parcel touches another
# Create for loop to run through lowdensity file
lowdensity["shared_boundary"] = False
for idx, parcel in lowdensity.iterrows():
    others = lowdensity.drop(idx)
    
    if others.geometry.touches(parcel.geometry).any():
        lowdensity.at[idx, "shared_boundary"] = True
print("\nNumber of parcels that share a boundary:", lowdensity["shared_boundary"].sum())

#%%
## Calculate assessed value of land per square meter
# Normalize av per square meter
lowdensity["avperm2"] = lowdensity["land_av"] / lowdensity["ldaream2"]
print("\nAverage Land Assessed Value per Square Meter:", "$", lowdensity["avperm2"].mean().round(2))

#%%
## Determine number of redevelopment candidates per number of residential units by block group

# Calculate number of residential units per block group
resdensity = parcels[["GEOID", "n_ResUnits"]]
resdensity = resdensity.groupby("GEOID")["n_ResUnits"].sum().to_frame()
resdensity = resdensity.rename(columns={'n_ResUnits':'n_resunitsbybg'})

# Calculate number of projects by residential density for each block group
resdensity["prj_per_bg"] = lowdensity.groupby("GEOID").size()
resdensity["prj_per_bg"] = resdensity["prj_per_bg"].fillna(0)
resdensity["prj_per_nres_by_bg"] = resdensity["prj_per_bg"] / resdensity["n_resunitsbybg"]
resdensity["density_per_100"] = resdensity["prj_per_nres_by_bg"] * 100

# Join to lowdensity and calculate redevelopment candidates by blockgroup
lowdensity = lowdensity.merge(resdensity, on='GEOID', how='left')

print("\nAverage Projects per 100 Residential Units by Block Group:", resdensity["density_per_100"].mean())

#%%
# Save files
lowdensity.to_file(ld_out_file, layer= 'lowdensity')
footprints.to_file(fp_out_file, layer = 'footprints')