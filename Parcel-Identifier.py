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

plt.rcParams['figure.dpi'] = 300

# Import data
## Use json or csv for editing before adding
parcels = gpd.read_file("Syracuse_Parcel_Map_(Q4_2024).zip")

# Summary/workspace (assist)
parcelcodes = parcels["LU_parcel"].value_counts()
parcelcodes2 = parcels["LUCat_Old"].value_counts()

# Query by "Commercial" zoning code
commercial = parcels.query("LUCat_Old == 'Commercial'")
print(commercial["FID"].value_counts())

# Query by "single-use" land use
lowdensity = commercial.query("LU_parcel == '1 use sm bld'")
print(lowdensity["FID"].value_counts())
    # Smallest queryable QPD column that reflects density

# Calculate percent of parcel vs land area
footprints = gpd.read_file("cugir-009065-geojson.json")
    # Project commercial and footprints as shape, clip from one another

# Calculate setbacks from road?
    # Load in road data, then calculate setback from centroid

# Identifiers: AV, setback, area
    # By area (Density): commercial["Shape_Are"] / 

# Index walkscore?, assessed value, percent of land as parking, sales tax, proximity
# Definition of strip mall? Theoretical and 

