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

plt.rcParams['figure.dpi'] = 300
utm18n = 32618

#%%
# Load and project dataframes
index = gpd.read_file("index_out_file.gpkg")
lowdensity = gpd.read_file("ld_out_file.gpkg")
parcels = gpd.read_file("parcels.gpkg")

parcels = parcels.to_crs(epsg=utm18n)
lowdensity = lowdensity.to_crs(epsg=utm18n)
index = index.to_crs(epsg=utm18n)

#%%
# Illustrate table with top 25 parcel candidates by final score
filtered_index = index[["FullAddres", "final_score"]]
top_candidates = filtered_index.sort_values(by="final_score", ascending=False).head(25)
top_candidates.set_index("FullAddres", inplace=True)

fig, ax = plt.subplots(figsize=(1, 6))  
ax.axis('off')
table = ax.table(cellText=top_candidates.values, colLabels=["Final Score"], rowLabels=top_candidates.index, loc='center')
ax.set_title("Table 1: Top 25 Candidates")

plt.savefig("top_25_parcels_table.jpg", bbox_inches='tight')
plt.show()

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
ax1.set_title("Table 2: Distribution of Index Scores (1-10)")
fig1.tight_layout()
fig1.savefig("score_distribution.jpg")

#%%
# Map identified parcels onto general parcel map
fig, ax = plt.subplots(figsize=(10, 10))
lowdensity.plot(ax=ax, edgecolor="black", facecolor="blue", linewidth=0.5, alpha=0.9)
parcels.plot(ax=ax, edgecolor="black", facecolor="white", linewidth=0.2, alpha=0.7)

ax.axis("off")
ax.set_title("Map 1: Eligible Parcels (Blue)")
fig.savefig("eligible_parcels.jpg")

plt.show()

#%%
# Map identified parcels by final score
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
fig.savefig("parcels_index_map.png")

plt.show()