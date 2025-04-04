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

# Summary/workspace
parcelcodes = parcels["LU_parcel"].value_counts()
parcelcodes2 = parcels["LUCat_Old"].value_counts()

# Calculate percent of parcel vs land area
footprints = gpd.read_file("cugir-009065-geojson.json")

# Identifiers: AV, setback, area, zoning code
    # By zoning code: parcels["LUCat_old == 'Commercial']
    # By area (Density): parcels["Shape_Are"] / 
# Identifiers: 
# Index walkscore?, assessed value, percent of land as parking, sales tax, proximity
# Definition of strip mall? Theoretical and 

