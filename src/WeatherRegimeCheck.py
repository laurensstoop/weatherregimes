#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 10:52:51 2022

@author: Laurens Stoop
"""

# load the dependencies
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import cartopy.feature as cftr
import cartopy.crs as ccrs
# import os



import matplotlib.pylab as pylab
params = {'legend.fontsize': 'xx-large',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'xx-large',
         'axes.titlesize':'xx-large',
         'xtick.labelsize':'xx-large',
         'ytick.labelsize':'xx-large'}
pylab.rcParams.update(params)


#%%
# =============================================================================
# Location of data and model choice
# =============================================================================

# set the data location
project_folder='/Users/3986209/Library/CloudStorage/OneDrive-UniversiteitUtrecht/Projects/weatherregimes/'
# external_drive='/Volumes/ExtremePro1/'
# external_drive='/Volumes/ExtremePro2/'
external_drive='/Users/3986209/Desktop'

# Raw data folder
weather_regimes='data/processed/WR_k6_combo.csv'

# determine the variable to plot 


# VAR='windCF_on'
# VAR='windCF_off'
# VAR='solarCF'
# VAR='ssrd'
# VAR='wspd100m'
VAR='t2m'

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
if VAR in ["solarCF", "windCF_off","windCF_on"]:
    ds = xr.open_mfdataset(external_drive+'/WR-daily/ERA5-EU_CF_*.nc')
    ds[VAR] = ds[VAR]*100
else: 
    ds = xr.open_mfdataset(external_drive+'/WR-daily/ERA5-EU_'+VAR+'_*.nc')
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
# ds2['meanMPSL'] = ds.mpsl.mean('time')

# Determine pressure anomaly that indicates the weather regimes
ds2[VAR+'_dev'] = ds2[VAR] - ds[VAR].mean('time')

# Make some plots for each weather regimes (start with 0-5)
# ds2.sel(WR=0).mpsl_dev.plot()


#%%
# =============================================================================
# Fancy version of plots
# =============================================================================

# This is the map projection we want to plot *onto*
map_proj = ccrs.LambertConformal(central_longitude=15, central_latitude=55) # 25, 55

WR_label = np.array(["SB-", "AR+", "NAO-", "SB+", "NAO+", "AR-"])

ds2 = ds2.assign_coords(WR=WR_label)

if VAR in ["solarCF", "windCF_off","windCF_on"]:
    p_mpsl = ds2[VAR+'_dev'].plot(transform=ccrs.PlateCarree(),  # the data's projection
                 col='WR', col_wrap=3,  # multiplot settings
                 aspect=ds.dims['longitude'] / ds.dims['latitude'],  # for a sensible figsize
                 # SolarPV
                   cmap='PuOr_r', 
                   vmin=-1.5, vmax=1.5,
                   levels=7,
                 # # # windon
                 #   cmap='BrBG_r', 
                 #   vmin=-6, vmax=6,
                 #   levels=9,
                   cbar_kwargs={'label':'SolarPV potential anomaly (%)'},
                  # cbar_kwargs={'label':'Wind generation potential anomaly (%)'},
                 subplot_kws={'projection': map_proj})  # the plot's projection ccrs.EuroPP()
else: 
    p_mpsl = ds2[VAR+'_dev'].plot(transform=ccrs.PlateCarree(),  # the data's projection
                 col='WR', col_wrap=3,  # multiplot settings
                 aspect=ds.dims['lon'] / ds.dims['lat'],  # for a sensible figsize
                 # SSRD
                    # cmap='PuOr_r', 
                    # vmin=-15, vmax=15,
                    # levels=7,
                     # cbar_kwargs={'label':'SSRD anomaly (W/m^2)'},
                 # WSPD
                    # cmap='BrBG_r', 
                    # vmin=-1.2, vmax=1.2,
                    # levels=9,
                    # extend='both',
                    # cbar_kwargs={'label':'100m Windspeed anomaly (m/s)'}, #, 'extend': 'both'},
                 # #T2m
                    cmap='RdBu_r', 
                    vmin=-2, vmax=2,
                    levels=9,
                    extend='both',
                    cbar_kwargs={'label':'2m air temperature anomaly (degC)'},
                 subplot_kws={'projection': map_proj})  # the plot's projection

# Load the country borders
country_borders = cftr.NaturalEarthFeature(
    category='cultural',
    name='admin_0_boundary_lines_land',
    scale='50m',
    facecolor='none')

# We have to set the map's options on all four axes
for ax in p_mpsl.axs.flat:
    ax.add_feature(country_borders, edgecolor='gray')
    ax.coastlines()
    ax.axes.axis("tight")
    ax.set_extent([-10, 40, 32, 70]) # West, east, south, north
    # Without this aspect attributes the maps will look chaotic and the
    # "extent" attribute above will be ignored
    ax.set_aspect(0.58)

# plt.tight_layout()

plt.savefig(project_folder+'results/figures/anom'+VAR+'_WR6.pdf')
plt.savefig(project_folder+'results/figures/anom'+VAR+'_WR6.png')

plt.show()

