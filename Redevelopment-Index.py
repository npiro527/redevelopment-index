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
index["area_quartile"] = pd.qcut(index["vacantpct"], q=4, labels=[.25, .5, .75, 1]) 
    # The more vacant, the higher the score

#%%
# Touching

#%%
# AV by quartile

#%%
# Projects per res units by bg by quartile