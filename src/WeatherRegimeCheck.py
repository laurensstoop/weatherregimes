#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 10:52:51 2022

@author: Laurens Stoop
"""

# load the dependencies
# import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import cartopy.feature as cftr
import cartopy.crs as ccrs
# import os

# set the data location
project_folder='/Users/3986209/Library/CloudStorage/OneDrive-UniversiteitUtrecht/Projects/weatherregimes/'
external_drive='/Volumes/ExtremePro2/'

# Raw data folder
weather_regimes='data/processed/WR_k6_combo.csv'

#%%
# =============================================================================
# Getting the Weather Regime files & fixing them in correct format befor the merger
# =============================================================================

# open the .csv of the data
df = pd.read_csv(project_folder+weather_regimes, delimiter=';')

# set the correct name for the time index for mergin later
df = df.rename(columns={'datetime': 'time'})

# Parse the time column to the datetime format
df = df.set_index(pd.to_datetime(df.time,dayfirst=True))

# drop the no longer needed time column (only need the index)
df = df.drop(axis=-1, columns='time')

# convert to Xarray and select the period of interest (1982-2010)
ds_wr = df.to_xarray()
ds_wr = ds_wr.sel(time=slice('1982-01-01', '2010-12-31'))

# Open the project data & remove the hour component of the daily mean values
ds = xr.open_mfdataset(external_drive+'ERA5/WR-daily/ERA5-EU_mpsl_*.nc')
ds['time'] = ds.time.dt.floor("D")

# Merge the two datasets
ds['WR'] = ds_wr.WR

#%%
# =============================================================================
# Select each WR to plot
# =============================================================================

# group the dataset by the Weather Regimes into a new dataset
ds2 = ds.groupby(ds.WR).mean('time')

# Determine the mean pressure for each grid-cell
ds2['meanMPSL'] = ds.mpsl.mean('time')

# Determine pressure anomaly that indicates the weather regimes
ds2['mpsl_dev'] = ds2.mpsl - ds2.meanMPSL

# Make some plots for each weather regimes (start with 0-5)
ds2.sel(WR=0).mpsl_dev.plot()


#%%
# =============================================================================
# Fancy version of plots
# =============================================================================

# This is the map projection we want to plot *onto*
map_proj = ccrs.LambertConformal(central_longitude=-30, central_latitude=50) # 25, 55

p = ds2.mpsl_dev.plot(transform=ccrs.PlateCarree(),  # the data's projection
             col='WR', col_wrap=2,  # multiplot settings
             aspect=ds.dims['lon'] / ds.dims['lat'],  # for a sensible figsize
             subplot_kws={'projection': map_proj})  # the plot's projection

# Load the country borders
country_borders = cftr.NaturalEarthFeature(
    category='cultural',
    name='admin_0_boundary_lines_land',
    scale='50m',
    facecolor='none')

# We have to set the map's options on all four axes
for ax in p.axes.flat:
    ax.add_feature(country_borders, edgecolor='gray')
    ax.coastlines()
    ax.set_extent([-70, 60, 25, 70]) # West, east, south, north
    # Without this aspect attributes the maps will look chaotic and the
    # "extent" attribute above will be ignored
    # ax.set_aspect('equal', 'box-forced')
plt.show()

