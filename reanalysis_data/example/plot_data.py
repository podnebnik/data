#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 01:06:16 2021

@author: ziga
"""

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np

data = Dataset("download.nc","r")

lons = data.variables["longitude"][:]
lats = data.variables["latitude"][:]

t2m = data.variables["t2m"]
evap = data.variables["e"]

data = Dataset("lsm_orog.nc","r")
lsm = data.variables["lsm"]
orog = data.variables["z"] # orography

# plot land sea mask
plt.contour(lons,lats,lsm[0],[0.5],color="black",lw=2)
plt.contour(lons,lats,orog[0],np.array([200,500,1000,1500,2000,2500])* 9.806,color="gray",lw=0.5)

# plot 2m-temperature
plt.contourf(lons,lats,t2m[0]-273, np.arange(268,292,1) - 273, cmap = plt.get_cmap("gist_rainbow_r"))

plt.colorbar()
plt.xlabel("geografska dolžina")
plt.ylabel("geografska širina")
plt.title("Mean 2-meter temperature, October 2020")
