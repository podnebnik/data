#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 03:12:49 2023

@author: ziga
"""

import xarray as xr
import os
import numpy as np
from subprocess import call
import pandas as pd
import time


def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()
    

folder_path = '../sources'
file_list = [f for f in os.listdir(folder_path) if f.endswith('.nc')]

# set initial time to 01-01-1900
last_archived_day = np.datetime64('1900-01-01T00:00:00.000000000')

for file_path in file_list:
    ds = xr.open_dataset(os.path.join(folder_path, file_path))
    last_day_file = ds.time.values[-1]
    if last_day_file > last_archived_day:
        last_archived_day = last_day_file

# download all data from (last_archived_day + 1 day) until (today - 7 days)    
start_date = last_archived_day + np.timedelta64(1, 'D')
end_date = np.datetime64('today') -  np.timedelta64(7, 'D') + np.timedelta64(1, 'D')

if start_date < end_date:
    print("Download data from {0} to {1}".format(start_date.astype('datetime64[D]'),end_date.astype('datetime64[D]')))
else:
    print("No data to download.")


for curr_date in np.arange(start_date, end_date, np.timedelta64(1, 'D')):
    print(curr_date)
    
    year = curr_date.astype('datetime64[Y]').astype(int) + 1970
    month = curr_date.astype('datetime64[M]').astype(int) % 12 + 1
    day = (curr_date.astype('datetime64[D]') - curr_date.astype('datetime64[M]') + 1).astype(int)
    
    print(year, month,day)

    # download daily data from ERA5
    replace_line("workflow_daily.py", 16, "year = {:03d}\n".format(year))
    replace_line("workflow_daily.py", 17, "month = {:2d}\n".format(month))
    replace_line("workflow_daily.py", 18, "day = {:2d}\n".format(day))
    call("python workflow_daily.py",shell=True)
    time.sleep(5)
    if day == 1 and month == 1:
        call("mv *.nc ../sources/t2m_{0}.nc".format(year),shell=True)
    else:
        call("mv *.nc ../temp/t2m_append.nc",shell=True)
        
        # Open and concatenate the files along the "time" dimension
        ds = xr.open_mfdataset(["../sources/t2m_{0}.nc".format(year),"../temp/t2m_append.nc"], combine="nested", concat_dim="time")
        
        # Save the concatenated file
        ds.to_netcdf("../temp/new.nc".format(year))
        call("mv ../temp/new.nc ../sources/t2m_{0}.nc".format(year),shell=True)
        call("rm ../temp/*",shell=True)
