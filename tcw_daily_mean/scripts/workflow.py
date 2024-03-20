#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 00:07:39 2021

@author: zaplotnikz
"""

import cdstoolbox as ct
# Efficiently process 1 year of ERA5 data
# The most efficient way to process a large amount of hourly ERA5 data
# is to retrieve 1 month at a time, process these data, and append the
# results to an output file.
# In the example below, the daily mean 2m temperature is calculated for 2019.
 
@ct.application(title='Download data')
@ct.output.download()
def application():
    count=1
    for yr in ['2022']:
        for mn in ['01', '02','03','04', '05', '06','07', '08', '09','10', '11', '12']:
             data = ct.catalogue.retrieve(
             'reanalysis-era5-single-levels',
             {
             'product_type': 'reanalysis',
             'variable': 'total_column_water',
             'year': yr,
             'month': mn,
             'day': ['01', '02', '03','04', '05', '06','07', '08', '09','10', '11', '12','13', '14', '15','16', '17', '18','19', '20', '21','22', '23', '24','25', '26', '27','28', '29', '30', '31'],
             'time': ['00:00', '01:00', '02:00','03:00', '04:00', '05:00','06:00', '07:00', '08:00','09:00', '10:00', '11:00','12:00', '13:00', '14:00','15:00', '16:00', '17:00','18:00', '19:00', '20:00','21:00', '22:00', '23:00'],
             'grid': [0.25,0.25],
             'area': [52, 9, 40, 21],
             }
             )
             day_mean=ct.climate.daily_mean(data,keep_attrs=True)
             if count == 1:
                 day_mean_all=day_mean
             else:       
                 day_mean_all=ct.cube.concat([day_mean_all, day_mean], dim='time')
             count = count + 1
             
    return day_mean_all
