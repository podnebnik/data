#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 00:44:17 2023

@author: ziga
"""
import requests
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

def point_in_slovenia(lat,lon):
    """Return True if point is in Slovenia, else return False. Extremely slow!"""

    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "format": "json",
        "lat": lat,
        "lon": lon
    }
    response = requests.get(url, params=params).json()
    try: 
        if "Slovenija" in response['address']['country']:
            return True
        else:
            return False
    except KeyError:
        return False


# define area of slovenia
ds = xr.open_dataset("../sources/t2m_1940.nc")
lons = ds["lon"].values
lats = ds["lat"].values
lons_grid,lats_grid = np.meshgrid(lons,lats)
# plt.contourf(lons_grid,lats_grid,ds["t2m"].values[0])

slovenia_mask = np.zeros(lons_grid.shape)

for (i,lon) in enumerate(lons):
    for (j,lat) in enumerate(lats):
        slovenia_mask[j,i] = point_in_slovenia(lat,lon)
        print(i,j,slovenia_mask[j,i])
        
np.save("../aux_files/slovenia_mask.npy",slovenia_mask)
