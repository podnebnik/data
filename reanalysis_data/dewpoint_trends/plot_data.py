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

td = data.variables["d2m"][:504,0,10:14,12:20].mean(axis=2).mean(axis=1)
blah_yr = []
for i in range(0,504,12):
    blah_yr.append(td[i:i+12].mean())

blah_JJA = []
for i in range(0,504,12):
    blah_JJA.append(td[i+5:i+8].mean())

# plt.plot(np.arange(1979,2021,1),np.array(blah_yr)-273,label="year")
plt.plot(np.arange(1979,2021,1),np.array(blah_JJA)-273,label="JJA")
plt.ylabel("dew point T [°C]")
plt.xlabel("year")
plt.title("Mean dew point temperature LAT 45.5N-46.5N, LON 14E-16E")


# data = Dataset("lsm_orog.nc","r")
# lsm = data.variables["lsm"]
# orog = data.variables["z"] # orography
# lons_orog = data.variables["longitude"][:]
# lats_orog = data.variables["latitude"][:]

# # # plot land sea mask
# plt.contour(lons_orog,lats_orog,lsm[0],[0.5],color="black",lw=2)
# plt.contour(lons_orog,lats_orog,orog[0],np.array([200,500,1000,1500,2000,2500])* 9.806,color="gray",lw=0.5)

# # # plot 2m-temperature
# plt.contourf(lons,lats,t2m[0]-273, np.arange(268,292,1) - 273, cmap = plt.get_cmap("gist_rainbow_r"))

# # plt.colorbar()
# # plt.xlabel("geografska dolžina")
# # plt.ylabel("geografska širina")
# # plt.title("Mean 2-meter temperature, October 2020")
