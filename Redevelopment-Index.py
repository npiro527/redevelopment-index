# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 15:34:43 2025

@author: npiro
"""


# Area of vacant land, touching, AV, projects per number of res units by bg

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

#%%
# Area by quintile

#%%
# Touching

#%%
# AV by quintile

#%%
# Projects per res units by bg by qunitile