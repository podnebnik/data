#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Created on Tue Feb 11 00:20:13 2020

@author: ziga
"""


import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-single-levels-monthly-means',
    {
        'product_type': 'monthly_averaged_reanalysis',
        'format': 'netcdf',
        'year': [str(year) for year in range(1940,2024)],
        'month': ['06','07','08'],
        'variable': [
            'total_precipitation'
        ],
        
        'time': '00:00',
        'area': [52, 9, 40, 21], # North, West, South, East. Default: global
        'grid'          : [0.25, 0.25], # Latitude/longitude grid: east-west (longitude) and north-south resolution (latitude). Default: 0.25 x 0.25

    },
    'summers_prec_monthly_1940_2024.nc')




