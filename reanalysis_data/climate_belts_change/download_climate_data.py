#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 20:16:26 2021

@author: ziga
"""

# import cdsapi

# c = cdsapi.Client()

# c.retrieve(
#     'projections-cmip5-monthly-single-levels',
#     {
#         'ensemble_member': 'r1i1p1',
#         'format': 'zip',
#         'variable': '2m_temperature',
#         'experiment': 'historical',
#         'model': 'cesm1_cam5',
#         'period': '185001-200512',
#     },
#     'download.zip')

import cdsapi

c = cdsapi.Client()

# c.retrieve(
#     'projections-cmip5-monthly-single-levels',
#     {
#         'ensemble_member': 'r1i1p1',
#         'format': 'zip',
#         'variable': '2m_temperature',
#         'experiment': 'rcp_4_5',
#         'model': 'cesm1_cam5',
#         'period': '200601-210012',
#     },
#     'download_future_rcp45.zip')



# 'area': [
#             49, 11, 43,
#             19,
#         ],
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
        'grid': [0.25, 0.25]
    },
    'lsm_orog.nc')