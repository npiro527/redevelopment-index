# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 15:34:43 2025

@author: npiro
"""


# Area of vacant land, shared boundary, AV, projects per number of res units by bg

#%%

# Load in packages and set defaults
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import requests
import seaborn as sns
import fiona

plt.rcParams['figure.dpi'] = 300

# Read in lowdensity file
index = gpd.read_file("ld_out_file.gpkg")

#%%
# Set index categories and weights
# Assign each category a rank of importance from first to fourth, with scores adding up to ten. 
index["area_rank"] = 1
index["shared_boundary_rank"] = 2
index["av_rank"] = 3
index["density_rank"] = 4

#%%
# Vacant area percent by quartile
index["area_score"] = (index["vacantpct"] * index["area_rank"])
print("\nRange of Percent Vacant:", round(index["vacantpct"].min() * 100, 2), "-", round(index["vacantpct"].max() * 100, 2))

#### Higher is better
#%%
# Touching
index["shared_boundary_score"] = index["shared_boundary"] * index["shared_boundary_rank"]
print("\nNumber of parcels that share a boundary:", index["shared_boundary"].sum())

#### Higher is better
#%%
# AV by quartile
index["av_quartile"] = pd.qcut(index["avperm2"], q=4, labels=[1, .75, .5, .25]).astype(float)
index["av_score"] = index["av_quartile"] * index["av_rank"]
print("\nRanges for assessed value quartiles:", index["avperm2"].quantile([1, .75, .5, .25]))

#### Lower is better, need to flip
#%%
# Projects per res units by bg by quartile
index["density_quartile"] = pd.qcut(index["density_per_100"], q=4, labels=[.25, .5, .75, 1]).astype(float)
index["density_score"] = index["density_rank"] * index["density_quartile"]
print("\nRanges for density quartiles:", index["density_per_100"].quantile([0.25, 0.5, 0.75, 1]))

#### Higher is better
#%%
# Final score calculation (out of 10 possible)
index["final_score"] = index[["area_score", "shared_boundary_score", "av_score", "density_score"]].sum(axis=1).round(2)
index = index.sort_values(by="final_score", ascending=False)
