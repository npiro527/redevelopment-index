# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 15:34:43 2025

@author: npiro
"""


# This script computes scores by weighing data compiled in Parcel_identifier.py

#%%
# Load in packages and set defaults
import json
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

plt.rcParams['figure.dpi'] = 300

info = json.load(open("input.json"))

# Read in lowdensity file
index = gpd.read_file("ld_out_file.gpkg")
index_out_file = "Output Files/index_out_file.gpkg"

#%%
## Rank importance from most (4) to least (1), with scores adding up to ten. 
# Percent of a parcel's area that is vacant
index["area_rank"] = info["area_rank"]

# Eligible parcel shares a boundary with another eligible parcel
index["shared_boundary_rank"] = info["shared_boundary_rank"]

# Ratio of assessed value($) per square foot in area
index["av_rank"] = info["av_rank"]

# Ratio of projects to surrounding residential units within block groups
index["density_rank"] = info["density_rank"]

# Run check to ensure ranking system is equal to ten
if info["density_rank"] + info["av_rank"] + info["shared_boundary_rank"] + info["area_rank"] == 10:
    print("Index score of 10 assigned, ready to run!")
else:
    print("Index total does not equal 10. Return to input.json and reassign values so that they equal 10.")

#%%
## Apply scoring weights for each factor
# Vacant area percent by quartile
index["area_score"] = (index["vacantpct"] * index["area_rank"])
print("\nRange of Percent Vacant:", round(index["vacantpct"].min() * 100, 2), "-", round(index["vacantpct"].max() * 100, 2))

# Shared boundary
index["shared_boundary_score"] = index["shared_boundary"] * index["shared_boundary_rank"]
print("\nNumber of parcels that share a boundary:", index["shared_boundary"].sum())

# AV (by quartile()
index["av_quartile"] = pd.qcut(index["avperm2"], q=4, labels=[1, .75, .5, .25]).astype(float)
index["av_score"] = index["av_quartile"] * index["av_rank"]
print("\nRanges for assessed value quartiles:", index["avperm2"].quantile([1, .75, .5, .25]))

# Projects per res units by block group (by quartile)
index["density_quartile"] = pd.qcut(index["density_per_100"], q=4, labels=[.25, .5, .75, 1]).astype(float)
index["density_score"] = index["density_rank"] * index["density_quartile"]
print("\nRanges for density quartiles:", index["density_per_100"].quantile([.25, 0.5, 0.75, 1]))

# Note: higher is better for each category

#%%
# Final score calculation (out of 10 possible)
index["final_score"] = index[["area_score", "shared_boundary_score", "av_score", "density_score"]].sum(axis=1).round(2)
index = index.sort_values(by="final_score", ascending=False)

#%%
# Save index to csv and geopackage
index.to_file(index_out_file, layer='index')
index.to_csv("Output Files/redevelopment_index.csv")
