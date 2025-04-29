# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 08:58:10 2025

@author: npiro
"""

# This script creates summary graphs, tables, and maps to visualize outputs

#%%
# Load in packages and data and set defaults
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os

plt.rcParams['figure.dpi'] = 300
utm18n = 32618

# Define output folder
os.makedirs("Output Visuals", exist_ok=True)

# Load and project dataframes
index = gpd.read_file("Output Files/index_out_file.gpkg")
lowdensity = gpd.read_file("Output Files/ld_out_file.gpkg")
parcels = gpd.read_file("parcels.gpkg")

parcels = parcels.to_crs(epsg=utm18n)
lowdensity = lowdensity.to_crs(epsg=utm18n)
index = index.to_crs(epsg=utm18n)

#%%
## Illustrate table with top 25 parcel candidates by final score
# Build figure
filtered_index = index[["FullAddres", "final_score"]]
top_candidates = filtered_index.sort_values(by="final_score", ascending=False).head(25)
top_candidates.set_index("FullAddres", inplace=True)

fig, ax = plt.subplots(figsize=(1, 6))  
ax.axis('off')
table = ax.table(cellText=top_candidates.values, colLabels=["Final Score"], rowLabels=top_candidates.index, loc='center')
ax.set_title("Table 1: Top 25 Candidates")

plt.savefig("Output Visuals/top_25_parcels_table.jpg", bbox_inches='tight')
plt.show()

#%%
## Graph distribution of index scores
# Build figure
nbins = range(1,12)
index['binned_score'] = pd.cut(index['final_score'], bins=nbins)
counts = index['binned_score'].value_counts().sort_index()
counts.index = counts.index.map(lambda x: x.left)

fig1, ax1 = plt.subplots()
ax1.bar(counts.index.astype(int), counts.values, color="blue")
ax1.set_xticks(range(1,11))
ax1.set_xlabel("Index Scores")
ax1.set_ylabel("Count of Properties")
ax1.set_title("Table 2: Distribution of Index Scores (1-10)")

fig1.tight_layout()
fig1.savefig("Output Visuals/score_distribution.jpg")

#%%
## Map identified parcels onto general parcel map
# Build figure
fig, ax = plt.subplots(figsize=(10, 10))
lowdensity.plot(ax=ax, edgecolor="black", facecolor="blue", linewidth=0.5, alpha=0.9)
parcels.plot(ax=ax, edgecolor="black", facecolor="white", linewidth=0.2, alpha=0.7)

ax.axis("off")
ax.set_title("Map 1: Eligible Parcels (Blue)")
fig.savefig("Output Visuals/eligible_parcels.jpg")

plt.show()

#%%
## Map identified parcels by final score
# Build figure
index['binned_score'] = index['binned_score'].astype(str)
bin_colors = {
    "(9,10]": "green",
    "(8, 9]": "#66cc66",  # Light green
    "(7, 8]": "#99ff99",  # Lighter green
    "(6, 7]": "#cccc00",  # Yellow-green
    "(5, 6]": "#ffcc00",  # Yellow
    "(4, 5]": "#ff9933",  # Orange
    "(3, 4]": "red",
}

fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
for bin_value, color in bin_colors.items():
    index[index['binned_score'] == str(bin_value)].plot(
        ax=ax, edgecolor="black", facecolor=color, linewidth=0.5, alpha=1, label=bin_value
    )
parcels.plot(ax=ax, edgecolor="black", facecolor="white", linewidth=0.2, alpha=0.7)

ax.axis("off")
ax.set_title("Map 2: Parcels by Index Score: Green (10) to Red (4)")
fig.savefig("Output Visuals/parcels_index_map.png")

plt.show()