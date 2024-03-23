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


#%% plot temperature gradients
plt.figure(1)
plt.contour(lons_surf,lats_surf,lsm[0],[0.5],color="black",lw=2)
plt.contourf(lons_surf,lats_surf,data_10yrt[61],np.arange(0,26,0.5), cmap = plt.get_cmap("gist_rainbow_r"))
# plt.contourf(lons_surf,lats_surf,data_10yrt[61] - data_10yrt[15],np.arange(0,3.5,0.1), cmap = plt.get_cmap("gist_rainbow_r"))
plt.colorbar()
u,v = np.gradient(data_10yrt[0])
plt.quiver(lons_surf,lats_surf,v,-u,angles='xy',scale=100)
plt.savefig("gradients.png",dpi=300)

#%% plot climate belt translation length
T2 = data_10yrt[61]
T1 = data_10yrt[0]
gradTy,gradTx = np.gradient(data_10yrt.mean(axis=0))

gradTabs = np.maximum((gradTy**2+gradTx**2)**0.5,np.zeros((97,121))+0.1)
xabs = (T2-T1)/gradTabs

dx = gradTx/ gradTabs*xabs
dy = gradTy/ gradTabs*xabs

length = np.sqrt(dx**2 + dy**2) 

plt.figure(2,figsize=(14,10))
plt.contour(lons_surf,lats_surf,lsm[0],[0.5],color="black",lw=2)
plt.contourf(lons_surf,lats_surf,data_10yrt[61],np.arange(0,26,0.5), cmap = plt.get_cmap("gist_ncar"))
plt.colorbar()

lw = (5 * length / length.max()) 
plt.streamplot(lons_surf,lats_surf,-dx,dy,color="black",density=5,zorder=3,linewidth=lw,arrowstyle="fancy")
# clr = 5*length/(0.1*length.max())
# plt.streamplot(lons_surf,lats_surf,-dx,dy,color=clr,density=5,zorder=3,linewidth=1,arrowstyle="fancy",cmap=plt.get_cmap("binary"))

plt.xlim([0,30])
plt.ylim([30,54])

plt.savefig("climate_translation.png",dpi=300)


#%%

# plt.figure(3,figsize=(14,10))
# plt.contour(lons_surf,lats_surf,lsm[0],[0.5],color="black",lw=2)
# plt.contourf(lons_surf,lats_surf,data_10yrt[60],np.arange(0,26,0.5), cmap = plt.get_cmap("gist_ncar"))
# plt.colorbar()

# plt.contour(lons_surf,lats_surf,data_10yrt[60], [9,10], colors="grey")
# plt.contourf(lons_surf,lats_surf,data_10yrt[60], np.arange(9,10.1,1), cmap=plt.get_cmap("Greys"),alpha=0.8, hatches='.')

# plt.xlim([0,30])
# plt.ylim([30,54])

# plt.savefig("difference4_2010s.png",dpi=300)


# #%%

# plt.figure(4,figsize=(14,10))
# plt.contour(lons_surf,lats_surf,lsm[0],[0.5],color="black",lw=2)
# plt.contourf(lons_surf,lats_surf,data_10yrt[50],np.arange(0,26,0.5), cmap = plt.get_cmap("gist_ncar"))
# plt.colorbar()

# plt.contour(lons_surf,lats_surf,data_10yrt[50], [9,10], colors="grey")
# plt.contourf(lons_surf,lats_surf,data_10yrt[50], np.arange(9,10.1,1), cmap=plt.get_cmap("Greys"),alpha=0.8, hatches='.')


# plt.xlim([0,30])
# plt.ylim([30,54])

# plt.savefig("difference4_2000s.png",dpi=300)


#%% 8-9°C belts

import os

# set all values lower than 0 to 0
data_10yrt[data_10yrt<0] = 0

# T to T+1 °C temperature belt
T = 18
if not os.path.exists("difference_{:02d}".format(T)):
    os.mkdir("difference_{:02d}".format(T))

for i in range(62):
    plt.figure(5,figsize=(14,10))
    plt.title("2m mean temperature {0:4d}-{1:4d}, 18-19°C temperature belt".format(1950+i,1950+9+i),fontsize=16)
    plt.contour(lons_surf,lats_surf,lsm[0],[0.5],color="black",lw=2)
    plt.contourf(lons_surf,lats_surf,data_10yrt[i],np.arange(0,26,0.5), cmap = plt.get_cmap("gist_ncar"))
    plt.colorbar()
    
    plt.contour(lons_surf,lats_surf,data_10yrt[i], [18,19], colors="grey")
    plt.contourf(lons_surf,lats_surf,data_10yrt[i], np.arange(18,19.1,1), cmap=plt.get_cmap("Greys"),alpha=0.8, hatches='.')
    
    
    plt.xlim([0,30])
    plt.ylim([30,54])
    
    plt.savefig("difference_{0:02d}/difference_{1:4d}_{2:4d}.png".format(T,1950+i,1950+9+i),dpi=300)
    plt.clf()
    