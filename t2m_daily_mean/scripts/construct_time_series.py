#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 20:07:55 2022

@author: ziga
"""


import numpy as np
import netCDF4
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import xarray as xr
import requests
import os

#%% FUNCTIONS

isLeap = lambda x: x % 4 == 0 and (x % 100 != 0 or x % 400 == 0)

#%% SCRIPT

folder_path = '../sources'
file_list = [f for f in os.listdir(folder_path) if f.endswith('.nc')]

# arbitrary dates which get rewritten
first_archived_day = np.datetime64('2200-01-01')
last_archived_day = np.datetime64('1800-01-01')


for file_path in file_list:
    ds = xr.open_dataset(os.path.join(folder_path, file_path))
    first_day_file = ds.time.values[0]
    last_day_file = ds.time.values[-1]
    
    if first_day_file < first_archived_day:
        first_archived_day = first_day_file
    
    if last_day_file > last_archived_day:
        last_archived_day = last_day_file


first_archived_day_year = np.datetime64(str(first_archived_day.astype('datetime64[Y]'))) - np.timedelta64(0, 'D')
last_archived_day_year = np.datetime64(str(last_archived_day.astype('datetime64[Y]'))) + np.timedelta64(1, 'Y') \
    -  np.timedelta64(1, 'D')

dates_array = np.arange(first_archived_day_year, last_archived_day_year+np.timedelta64(1, 'D'), np.timedelta64(1, 'D'))
dates_array = pd.to_datetime(dates_array) # transform to pandas
t2m_array = np.zeros(dates_array.shape)
# t2m_array_rec = np.zeros(dates_array.shape)

# search for start_year and end_year of the dataset
start_year = dates_array[0].year
end_year = dates_array[-1].year


# load mask for Slovenia
slovenia_mask = np.load("../aux_files/slovenia_mask.npy")
n_points_slo = np.sum(slovenia_mask)

# loop through years from start year to end year
d = 0
for yyyy in range(start_year,end_year+1):
    print(yyyy)
    data = xr.open_dataset("../sources/t2m_{0:04d}.nc".format(yyyy))
    
    nd_data = data["t2m"].shape[0]
    
    for k in range(0,nd_data):
        t2m_array[d] = np.sum(data["t2m"].values[k]*slovenia_mask)/n_points_slo
        # t2m_array_rec[d] = data["t2m"].values[k,21:27,17:31].mean()
        d += 1

t2m_array[d:] = np.nan

#%% Smooth the data
# three options: raw-daily, 7-day moving average, 15-day moving average
t2m_array_7 = np.convolve(t2m_array, np.ones(7)/7, mode='same') # 3 day shift
t2m_array_15 = np.convolve(t2m_array, np.ones(15)/15, mode='same') # 7 day shift
t2m_array_31 = np.convolve(t2m_array, np.ones(31)/31, mode='same') # 15 day shift
t2m_array_61 = np.convolve(t2m_array, np.ones(61)/61, mode='same') # 30 day shift

# Create boolean mask to filter out al February 29ths 
mask1 = np.logical_and(dates_array.month == 2, dates_array.day == 29)
# mask2 = np.logical_or(dates_array.year == end_year, dates_array.year == start_year)
mask = mask1 #np.logical_or(mask1,mask2)

# Filter out February 29th dates using boolean mask
filtered_dates = dates_array[~mask]
filtered_t2m_array = t2m_array[~mask]
filtered_t2m_array_7 = t2m_array_7[~mask]
filtered_t2m_array_15 = t2m_array_15[~mask]
filtered_t2m_array_31 = t2m_array_31[~mask]
filtered_t2m_array_61 = t2m_array_61[~mask]

#%%  EXPORT DATA

# export raw time series
df = pd.DataFrame({'Date': dates_array, 't2m': t2m_array})
df = df.set_index('Date')
df.to_csv('../data/t2m.csv')


# export 7-day smoothed time-series
df = pd.DataFrame({'Date': dates_array[3:], 't2m': t2m_array_7[3:]})
df = df.set_index('Date')
df.to_csv('../data/t2m_ma_7day.csv')

df = pd.DataFrame({'Date': dates_array[7:], 't2m': t2m_array_15[7:]})
df = df.set_index('Date')
df.to_csv('../data/t2m_ma_15day.csv')


# export table of t2m for day_of_year for each year 
t2m_matrix = filtered_t2m_array.reshape((end_year-start_year+1,365))

df_dict = {'Day_of_year': np.arange(1,366)}
i = 0
for yyyy in range(start_year,end_year+1):
    key = f"{yyyy}"
    value = t2m_matrix[i,:]
    df_dict[key] = value
    i += 1

df = pd.DataFrame(df_dict)
df = df.set_index('Day_of_year')
df.to_csv('../data/t2m_table_doy.csv')


# export table of smoothed t2m for day_of_year for each year 
t2m_matrix = filtered_t2m_array_7.reshape((end_year-start_year+1,365))

df_dict = {'Day_of_year': np.arange(1,366)}
i = 1
for yyyy in range(start_year+1,end_year+1):
    key = f"{yyyy}"
    value = t2m_matrix[i,:]
    df_dict[key] = value
    i += 1

df = pd.DataFrame(df_dict)
df = df.set_index('Day_of_year')
df.to_csv('../data/t2m_table_doy_ma_7day.csv')


t2m_matrix = filtered_t2m_array_15.reshape((end_year-start_year+1,365))

df_dict = {'Day_of_year': np.arange(1,366)}
i = 1
for yyyy in range(start_year+1,end_year+1):
    key = f"{yyyy}"
    value = t2m_matrix[i,:]
    df_dict[key] = value
    i += 1

df = pd.DataFrame(df_dict)
df = df.set_index('Day_of_year')
df.to_csv('../data/t2m_table_doy_ma_15day.csv')


t2m_matrix = filtered_t2m_array_31.reshape((end_year-start_year+1,365))

df_dict = {'Day_of_year': np.arange(1,366)}
i = 1
for yyyy in range(start_year+1,end_year+1):
    key = f"{yyyy}"
    value = t2m_matrix[i,:]
    df_dict[key] = value
    i += 1

df = pd.DataFrame(df_dict)
df = df.set_index('Day_of_year')
df.to_csv('../data/t2m_table_doy_ma_31day.csv')


t2m_matrix = filtered_t2m_array_61.reshape((end_year-start_year+1,365))

df_dict = {'Day_of_year': np.arange(1,366)}
i = 1
for yyyy in range(start_year+1,end_year+1):
    key = f"{yyyy}"
    value = t2m_matrix[i,:]
    df_dict[key] = value
    i += 1

df = pd.DataFrame(df_dict)
df = df.set_index('Day_of_year')
df.to_csv('../data/t2m_table_doy_ma_61day.csv')

# export table of t2m monthly-means for each year 

df_dict = {'Year': np.arange(start_year,end_year+1)}
i = 0
for mm in range(1,13):
    key = f"{mm}"
    t2m_monthly_means = np.zeros((end_year-start_year+1))
    j = 0
    for yyyy in range(start_year,end_year+1):
        t2m_monthly_means[j] = filtered_t2m_array[np.logical_and(filtered_dates.month==mm, filtered_dates.year==yyyy)].mean()
        j += 1
    value = t2m_monthly_means
    df_dict[key] = value
    i += 1

df = pd.DataFrame(df_dict)
df = df.set_index('Year')
df.to_csv('../data/t2m_table_monthly_means.csv')


# export table of t2m seasonal-means for each year 
# ddf_dict = {'Year': np.arange(start_year,end_year+1)}
# i = 0
# for season in [[12,1,2]]:
#     key = f"{mm}"
#     t2m_monthly_means = np.zeros((end_year-start_year+1))
#     j = 0
#     for yyyy in range(start_year+1,end_year+1):
#         t2m_monthly_means[j] = filtered_t2m_array[np.logical_and(np.logical_or(filtered_dates.month==mm%12,\
#                                                                                filtered_dates.month==mm%12,
#                                                                                filtered_dates.month==mm%12),\
#                                                                  filtered_dates.year==yyyy)].mean()
#         j += 1
#     value = t2m_monthly_means.mean()
#     df_dict[key] = value
#     i += 1

# df = pd.DataFrame(df_dict)
# df = df.set_index('Year')
# df.to_csv('../data/t2m_table_seasonal_means.csv')

# define climatological averages for different n-year periods for each of 365 calendar days
# 1941-1970
t2m_matrix = filtered_t2m_array.reshape((end_year-start_year+1,365))
t2m_clima = t2m_matrix[1941-start_year:1970-start_year+1,:].mean(axis=0)
df = pd.DataFrame({'Day_of_year': np.arange(1,366),'t2m': t2m_clima})
df = df.set_index('Day_of_year')
df.to_csv('../data/t2m_table_doy_1941_1970.csv')

# 1951-1980
t2m_matrix = filtered_t2m_array.reshape((end_year-start_year+1,365))
t2m_clima = t2m_matrix[1951-start_year:1980-start_year+1,:].mean(axis=0)
df = pd.DataFrame({'Day_of_year': np.arange(1,366),'t2m': t2m_clima})
df = df.set_index('Day_of_year')
df.to_csv('../data/t2m_table_doy_1951_1980.csv')

# 1961-1990
t2m_matrix = filtered_t2m_array.reshape((end_year-start_year+1,365))
t2m_clima = t2m_matrix[1961-start_year:1990-start_year+1,:].mean(axis=0)
df = pd.DataFrame({'Day_of_year': np.arange(1,366),'t2m': t2m_clima})
df = df.set_index('Day_of_year')
df.to_csv('../data/t2m_table_doy_1961_1990.csv')

# 1971-2000
t2m_matrix = filtered_t2m_array.reshape((end_year-start_year+1,365))
t2m_clima = t2m_matrix[1971-start_year:2000-start_year+1,:].mean(axis=0)
df = pd.DataFrame({'Day_of_year': np.arange(1,366),'t2m': t2m_clima})
df = df.set_index('Day_of_year')
df.to_csv('../data/t2m_table_doy_1971_2000.csv')

# 1981-2010
t2m_matrix = filtered_t2m_array.reshape((end_year-start_year+1,365))
t2m_clima = t2m_matrix[1981-start_year:2010-start_year+1,:].mean(axis=0)
df = pd.DataFrame({'Day_of_year': np.arange(1,366),'t2m': t2m_clima})
df = df.set_index('Day_of_year')
df.to_csv('../data/t2m_table_doy_1981_2010.csv')

# 1991-2020
t2m_matrix = filtered_t2m_array.reshape((end_year-start_year+1,365))
t2m_clima = t2m_matrix[1991-start_year:2020-start_year+1,:].mean(axis=0)
df = pd.DataFrame({'Day_of_year': np.arange(1,366),'t2m': t2m_clima})
df = df.set_index('Day_of_year')
df.to_csv('../data/t2m_table_doy_1991_2020.csv')

# annual means
t2m_annual_means = np.zeros((end_year-start_year))
i = 0
for yyyy in range(start_year,end_year):
    t2m_annual_means[i] = t2m_array[dates_array.year == yyyy].mean()
    i += 1

df_dict = {'Year': np.arange(start_year,end_year),}
df = pd.DataFrame({'Year': np.arange(start_year,end_year),'t2m_annual': t2m_annual_means})
df = df.set_index('Year')
df.to_csv('../data/t2m_annual_means.csv')


