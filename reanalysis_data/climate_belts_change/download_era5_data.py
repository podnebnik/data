#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 20:16:26 2021

@author: ziga
"""

# import cdsapi

# c = cdsapi.Client()

# c.retrieve(
#     'reanalysis-era5-single-levels-monthly-means',
#     {
#         'format': 'netcdf',
#         'product_type': 'monthly_averaged_reanalysis',
#         'variable': '2m_temperature',
#         'year': [
#             '1979', '1980', '1981',
#             '1982', '1983', '1984',
#             '1985', '1986', '1987',
#             '1988', '1989', '1990',
#             '1991', '1992', '1993',
#             '1994', '1995', '1996',
#             '1997', '1998', '1999',
#             '2000', '2001', '2002',
#             '2003', '2004', '2005',
#             '2006', '2007', '2008',
#             '2009', '2010', '2011',
#             '2012', '2013', '2014',
#             '2015', '2016', '2017',
#             '2018', '2019', '2020'
#         ],
#         'month': [
#             '01', '02', '03',
#             '04', '05', '06',
#             '07', '08', '09',
#             '10', '11', '12',
#         ],
        # 'area': [
        #     54, 0, 30,
        #     30,
        # ],
#         'grid': [0.25, 0.25],
#         'time': '00:00',
#     },
#     'download.nc')



import cdsapi

c = cdsapi.Client()

# c.retrieve(
#     'reanalysis-era5-single-levels-monthly-means-preliminary-back-extension',
#     {
#         'format': 'netcdf',
#         'variable': '2m_temperature',
#         'product_type': 'reanalysis-monthly-means-of-daily-means',
#         'year': [
#             '1950', '1951', '1952',
#             '1953', '1954', '1955',
#             '1956', '1957', '1958',
#             '1959', '1960', '1961',
#             '1962', '1963', '1964',
#             '1965', '1966', '1967',
#             '1968', '1969', '1970',
#             '1971', '1972', '1973',
#             '1974', '1975', '1976',
#             '1977', '1978',
#         ],
#         'month': [
#             '01', '02', '03',
#             '04', '05', '06',
#             '07', '08', '09',
#             '10', '11', '12',
#         ],
#         'area': [
#             54, 0, 30,
#             30,
#         ],
#         'grid': [0.25, 0.25],
#         'time': '00:00',
#     },
#     'era5_1950_1978.nc')




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
        'area': [
            54, 0, 30,
            30,
        ],
        'grid': [0.25, 0.25]
    },
    'lsm_orog.nc')