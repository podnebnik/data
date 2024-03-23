#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 01:06:16 2021

@author: ziga
"""

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np

# load model orography and land-sea mask data
data = Dataset("lsm_orog.nc","r")
lons_surf = data.variables["longitude"][:]
lats_surf = data.variables["latitude"][:]
lsm = data.variables["lsm"]
orog = data.variables["z"] # orography

# load ERA5 reanalysis data 1950-1978
data1 = Dataset("era5_1950_1978.nc","r")
t2m1 = data1.variables["t2m"]

# load ERA5 reanalysis data 1979-2020
data2 = Dataset("era5_1979_2020.nc","r")
t2m2 = data2.variables["t2m"]

# merge data and transform from kelvin to celsius scale
t2m = np.concatenate((t2m1,t2m2),axis=0) - 273.15
n = t2m.shape[0]

# compute 10-year running means
data_10yrt = np.zeros((62,97,121))
for i in range(0,n-120+1,12):
    data_10yrt[i//12] = t2m[i:i+120].mean(axis=0) 




#%% create own colormap
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable

# create colormap
# ---------------

# create a colormap that consists of
# - 1/5 : custom colormap, ranging from white to the first color of the colormap
# - 4/5 : existing colormap

# set upper part: 4 * 256/4 entries
cmap = mpl.cm.jet(np.arange(256))

cmap[200:210,0:3] = 0.5
cmap = mpl.colors.ListedColormap(cmap, name='myColorMap', N=cmap.shape[0])
# # set lower part: 1 * 256/4 entries
# # - initialize all entries to 1 to make sure that the alpha channel (4th column) is 1
# lower = np.ones((int(256/4),4))
# # - modify the first three columns (RGB):
# #   range linearly between white (1,1,1) and the first color of the upper colormap
# for i in range(3):
#   lower[:,i] = np.linspace(1, upper[0,i], lower.shape[0])

# # combine parts of colormap
# cmap = np.vstack(( lower, upper ))

# # convert to matplotlib colormap
# cmap = mpl.colors.ListedColormap(cmap, name='myColorMap', N=cmap.shape[0])

#%% 8-9°C belts

import os

# set all values lower than 0 to 0
# data_10yrt[data_10yrt<0] = 0

# T to T+1 °C temperature belt
T = 16
if not os.path.exists("difference_{:02d}".format(T)):
    os.mkdir("difference_{:02d}".format(T))

for i in range(1,62,10):
    fig=plt.figure(5,figsize=(12,8))
    plt.title("Povprečna letna temperatura na 2 metrih, {0:4d}-{1:4d}".format(1950+i,1950+9+i),fontsize=16)
    plt.contour(lons_surf,lats_surf,lsm[0],[0.5],color="black",linewidth=4)
    plt.contourf(lons_surf,lats_surf,data_10yrt[i],np.arange(0,22,1), cmap = cmap,extend="both",hatches=(T+1)*[None]+['.']+5*[None])
    cbar = plt.colorbar()
    cbar.set_label("Temperatura [°C]",fontsize=16)
    for t in cbar.ax.get_yticklabels():
         t.set_fontsize(16)
    
    plt.contour(lons_surf,lats_surf,data_10yrt[i], [T,T+1], colors="grey")
    # plt.contourf(lons_surf,lats_surf,data_10yrt[i], np.arange(T,T+1.1,1), cmap=plt.get_cmap("Greys"),alpha=0.8, hatches='.')
    plt.grid()
    
    plt.xlim([0,30])
    plt.ylim([30,54])
    plt.xlabel("Geografska dolžina [°]",fontsize=16)
    plt.ylabel("Geografska širina [°]",fontsize=16)
    
    fig.tight_layout()
    plt.savefig("difference_{0:02d}/difference_{1:4d}_{2:4d}.png".format(T,1950+i,1950+9+i),dpi=300)
    plt.clf()
    
    
#%% 8-9°C belts

import os
from matplotlib.colors import LinearSegmentedColormap


colors = np.array([(203, 235, 246),\
          (167, 191, 217),\
          (140, 153, 188),\
          (151, 78, 168),\
          (131, 15, 116),\
          (11, 20, 79),\
          (14, 38, 128),\
          (34, 59, 151),\
          (28, 73, 154),\
          (40, 89, 165),\
          (27, 106, 163),\
          (29, 155, 196),\
          (28, 164, 188),\
          (100, 198, 199),\
          (134, 202, 187),\
          (145, 224, 167),\
          (199, 238, 191),\
          (246, 253, 209),\
          (253, 236, 167),\
          (248, 218, 119),\
          (252, 179, 77),\
          (252, 140, 68),\
          (248, 81, 39),\
          (245, 47, 38),\
          (209, 11, 38),\
          (156, 4, 42),\
          (118, 3, 36),\
          (24,0,12)])/256.
    
    
    
    
cmap = LinearSegmentedColormap.from_list("col_temp", colors, N=100)

# T to T+1 °C temperature belt
T = 17
if not os.path.exists("2difference_{:02d}".format(T)):
    os.mkdir("2difference_{:02d}".format(T))

for i in range(1,62,10):
    fig=plt.figure(5,figsize=(12,8))
    plt.title("Povprečna letna temperatura na 2 metrih, {0:4d}-{1:4d}".format(1950+i,1950+9+i),fontsize=16)
    plt.contour(lons_surf,lats_surf,lsm[0],[0.5],color="black",linewidth=4)
    plt.contourf(lons_surf,lats_surf,data_10yrt[i],np.arange(0,22,1), cmap = cmap,extend="both",hatches=(T+1)*[None]+['//']+5*[None])
    cbar = plt.colorbar()
    cbar.set_label("Temperatura [°C]",fontsize=16)
    for t in cbar.ax.get_yticklabels():
          t.set_fontsize(16)
    
    plt.contour(lons_surf,lats_surf,data_10yrt[i], [T,T+1], colors="grey")
    # plt.contourf(lons_surf,lats_surf,data_10yrt[i], np.arange(T,T+1.1,1), cmap=plt.get_cmap("Greys"),alpha=0.8, hatches='.')
    plt.grid()
    
    plt.xlim([0,30])
    plt.ylim([30,54])
    plt.xlabel("Geografska dolžina [°]",fontsize=16)
    plt.ylabel("Geografska širina [°]",fontsize=16)
    
    fig.tight_layout()
    plt.savefig("2difference_{0:02d}/difference_{1:4d}_{2:4d}.png".format(T,1950+i,1950+9+i),dpi=300)
    plt.clf()
    
        
    