#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 09:46:19 2021

@author: Laurens Stoop
"""

# load the dependencies
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import os


# directory definitions
os.chdir('/home/stoop/Documents/Project/WeatherRegimes/')

# Raw data folder
data_falkena_k4='./data/raw/Erai_DJFM_all_season0_k4.npz'
data_falkena_k6='./data/raw/Erai_DJFM_all_season0_k6.npz'

#%%
# =============================================================================
# Loading the data
# =============================================================================


with np.load(data_falkena_k6) as data:
    lst = data.files
    # for item in lst:
    #     print(item)
        # print(data[item])
    lsum = data['L_sum']
    seq = data['sequence']
    th = data['theta']
    dist = data['distance']
    

# Getting the correct sequence data
seq2 = np.argmin(dist, axis=0)

# create a date range
date_range_full = pd.date_range('1979-01-01', '2018-12-31' )

df = pd.Series(seq2).to_frame()
df_time = pd.Series(date_range_full).to_frame()

# name the time column
df = df.rename(columns={0: "WR"})
df_time = df_time.rename(columns={0: "datetime"})
# add an temp column
df_time['test'] = np.zeros(len(date_range_full))

# set the axis
df_time = df_time.set_index('datetime')

#Set a xarray dataset
dsWR  = xr.Dataset.from_dataframe(df)
dst = xr.Dataset.from_dataframe(df_time)

# Drop all but DJFM
dst = dst.where(np.logical_or(dst["datetime.month"]>11, dst["datetime.month"]<4), drop =True)

#transfer back
df2 = dst.to_dataframe()

#combine
df3 = pd.concat([df2, df.set_index(df2.index[:len(df)])], axis=1).drop("test",1)

df.to_csv('./data/processed/WR_k6_value.csv')
df2.to_csv('./data/processed/WR_k6_time.csv')
