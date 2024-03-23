#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 20:16:26 2021

@author: ziga
"""

import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-land-monthly-means',
    {
        'format': 'netcdf',
        'variable': [
            '2m_temperature', 'total_evaporation',
        ],
        'year': '2020',
        'month': '10',
        'time': '00:00',
        'area': [
            49, 11, 43,
            19,
        ],
        'product_type': 'monthly_averaged_reanalysis',
    },
    'download.nc')


c.retrieve(
    'reanalysis-era5-single-levels-monthly-means',
    {
        'format': 'netcdf',
        'product_type': 'monthly_averaged_reanalysis',
        'variable': [
            'land_sea_mask', 'orography',
        ],
        'year': '1979',
        'month': '01',
        'time': '00:00',
        'area': [
            49, 11, 43,
            19,
        ],
        'grid': [0.1, 0.1]
    },
    'lsm_orog.nc')