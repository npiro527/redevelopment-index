# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 08:58:10 2025

@author: npiro
"""

# Summary table and map creation
#%%
# Load in packages and set defaults
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import requests
import seaborn as sns
import fiona

plt.rcParams['figure.dpi'] = 300
utm18n = 32618

#%%
# Load in index dataframe
index = gpd.read_file("index_out_file.gpkg")

#%%
# Graph distribution of index scores
nbins = range(1,12)
index['binned_score'] = pd.cut(index['final_score'], bins=nbins)
counts = index['binned_score'].value_counts().sort_index()
counts.index = counts.index.map(lambda x: x.left)

fig1, ax1 = plt.subplots()
ax1.bar(counts.index.astype(int), counts.values, color="blue")
ax1.set_xticks(range(1,11))
ax1.set_xlabel("Index Scores")
ax1.set_ylabel("Count of Properties")
ax1.set_title("Distribution of Index Scores (1-10)")
fig1.tight_layout()
fig1.savefig("score_distribution.png")