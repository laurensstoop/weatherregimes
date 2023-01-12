#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 20:38:50 2023

@author: 3986209
"""

import cdsapi
import numpy as np


external_drive='/Volumes/ExtremePro2/ERA5/Geopotential/'

#%%
c = cdsapi.Client()

for Y in np.arange(1979, 2017):
    c.retrieve(
        'reanalysis-era5-pressure-levels',
        {
            'product_type': 'reanalysis',
            'format': 'grib',
            'variable': 'geopotential',
            'pressure_level': '500',
            'month': [
                '01', '02', '03',
                '11', '12',
            ],
            'year': str(Y),
            'day': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
                '13', '14', '15',
                '16', '17', '18',
                '19', '20', '21',
                '22', '23', '24',
                '25', '26', '27',
                '28', '29', '30',
                '31',
            ],
            'time': [
                '00:00', '01:00', '02:00',
                '03:00', '04:00', '05:00',
                '06:00', '07:00', '08:00',
                '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00',
                '15:00', '16:00', '17:00',
                '18:00', '19:00', '20:00',
                '21:00', '22:00', '23:00',
            ],
            'area': [
                80, -90, 20, 30,
            ],
        },
        external_drive+'ERA5-Atlantic_Gph_'+str(Y)+'.grib')