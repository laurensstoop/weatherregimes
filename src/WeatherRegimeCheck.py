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
import os

# set the data location
project_folder='/Users/3986209/Library/CloudStorage/OneDrive-UniversiteitUtrecht/Projects/weatherregimes/'

# Raw data folder
weather_regimes='data/processed/WR_k6_combo.csv'

#%%
# =============================================================================
# Getting the Weather Regime files
# =============================================================================

# open the .csv of the data
df = pd.read_csv(project_folder+weather_regimes, delimiter=';')

