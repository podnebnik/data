#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 23:36:21 2020

@author: ziga
"""

# https://jakevdp.github.io/PythonDataScienceHandbook/04.13-geographic-data-with-basemap.html
# https://jakevdp.github.io/PythonDataScienceHandbook/04.14-visualization-with-seaborn.html

import numpy as np
import netCDF4
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from datetime import datetime

isLeap = lambda x: x % 4 == 0 and (x % 100 != 0 or x % 400 == 0)

# READ DATA
data_t2m_1 = netCDF4.Dataset("summers_t2m_monthly_1950_1978.nc")
data_t2m_2 = netCDF4.Dataset("summers_t2m_monthly_1979_2020.nc")
data_prec_1 = netCDF4.Dataset("summers_prec_monthly_1950_1978.nc")
data_prec_2 = netCDF4.Dataset("summers_prec_monthly_1979_2020.nc")

lat = data_t2m_1.variables['latitude'][:]
lon = data_t2m_1.variables['longitude'][:]
lon, lat = np.meshgrid(lon, lat)


#%%

t2m_1 = (data_t2m_1.variables["t2m"][:]).reshape((29,3,49,49)).mean(axis=1)
prec_1 = (data_prec_1.variables["tp"][:]).reshape((29,3,49,49)).mean(axis=1)*(30+31+31)*1000

t2m_2 = (data_t2m_2.variables["t2m"][:]).reshape((42,3,49,49)).mean(axis=1)
prec_2 = (data_prec_2.variables["tp"][:]).reshape((42,3,49,49)).mean(axis=1)*(30+31+31)*1000

t2m = np.concatenate((t2m_1,t2m_2))
prec = np.concatenate((prec_1,prec_2))

t2m_dev = t2m - t2m[31:61].mean(axis=0)
prec_dev = prec - prec[31:61].mean(axis=0)


# 21:27,17:31 Slovenia
t2m_dev_slo = t2m_dev[:,21:27,17:31].mean(axis=(1,2))
prec_dev_slo = prec_dev[:,21:27,17:31].mean(axis=(1,2))


t2m_dev_slo_trend = np.polyfit(np.arange(0,71),t2m_dev_slo,1)
prec_dev_slo_trend = np.polyfit(np.arange(0,71),prec_dev_slo,1)

def moving_average(a, n=5) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

t2m_dev_slo_ma = moving_average(t2m_dev_slo,10)
prec_dev_slo_ma = moving_average(prec_dev_slo,10)
#%%
fig=plt.figure(figsize=(9,6.2))
plt.plot([-3,3.5],[0,0],"k-",linewidth=2)
plt.plot([0,0],[-240,240],"k-",linewidth=2)

plt.plot(t2m_dev_slo[0:10],prec_dev_slo[0:10],"s",label="1950-1959",markersize=5,color="lightblue")
plt.plot(t2m_dev_slo[10:20],prec_dev_slo[10:20],"s",label="1960-1969",markersize=5,color="green")
plt.plot(t2m_dev_slo[20:30],prec_dev_slo[20:30],"s",label="1970-1979",markersize=5,color="lightgreen")
plt.plot(t2m_dev_slo[30:40],prec_dev_slo[30:40],"s",label="1980-1989",markersize=5,color="wheat")
plt.plot(t2m_dev_slo[40:50],prec_dev_slo[40:50],"s",label="1990-1999",markersize=5,color="orange")
plt.plot(t2m_dev_slo[50:60],prec_dev_slo[50:60],"s",label="2000-2009",markersize=5,color="red")
plt.plot(t2m_dev_slo[60:71],prec_dev_slo[60:71],"s",label="2010-2020",markersize=5,color="darkviolet")

# plt.plot(t2m_dev_slo_ma,prec_dev_slo_ma,"g-")

plt.legend(loc=8,ncol=3)
plt.grid()
plt.text(-2.4,200,"cool & wet",fontsize=16)
plt.text(2.2,200,"hot & wet",fontsize=16)
plt.text(2.2,-210,"hot & dry",fontsize=16)
plt.text(-2.4,-210,"cool & dry",fontsize=16)
plt.xlim([-2.5,3.2])
plt.ylim([-220,220.])
plt.xlabel(r"temperature deviation from 1981-2010 [$^\circ$C]",fontsize=14)
plt.ylabel("precipitation deviation from 1981-2010 [mm]",fontsize=14)
plt.title("ERA5 summer 1950-2020, Slovenia",fontsize=18)
fig.tight_layout(rect=(0,0,1,1),h_pad=0.1,w_pad=0.1,pad=0.1)
plt.savefig("blah.png",dpi=300)

# #%%
# #set up the map

# t2m_dev[-30,23:26,20:26] = -3


# fig = plt.figure(1,figsize=(8, 7))
# m = Basemap(projection='cyl', llcrnrlat=40,urcrnrlat=52,\
#             llcrnrlon=9,urcrnrlon=21,resolution='h')
# im=m.contourf(lon, lat, t2m_dev[-30], np.arange(-5,5.01,0.25),latlon=True, cmap='RdBu_r')
# m.contour(lon, lat, t2m_dev[-1], np.arange(-5,5.01,1.),latlon=True, colors="gray",linewidths=0.8)
# m.drawcountries(linewidth=1.5, color='black', zorder=3)
# m.drawcoastlines(linewidth=1.2,color='gray')
# plt.title('June 2020 Temperature Anomaly vs 2015-2019 (ERA5)',fontsize=16)
# plt.text("")
# cbar=plt.colorbar(im,ticks=np.arange(-5,5.01,1.),fraction=0.046, pad=0.04,extend='both',boundaries=[-6]+list(np.arange(-5,5.01,1)+[6]))
# cbar.set_label(r'$\Delta T$ [$^\circ$C]',fontsize=14)
# cbar.ax.tick_params(labelsize=14)
# fig.tight_layout(rect=(0,0,1,1),h_pad=0.1,w_pad=0.1,pad=0.1)

#%%
# fig = plt.figure(2,figsize=(8, 7))
# m = Basemap(projection='cyl', llcrnrlat=40,urcrnrlat=52,\
#             llcrnrlon=9,urcrnrlon=21,resolution='h')
# im=m.contourf(lon, lat, t2m_dev[0], np.arange(-200,200.1,5.),latlon=True, cmap='BrBG')
# # m.contour(lon, lat, tp_season[-2] - tp_season_clim, np.arange(-200,200.01,20.),latlon=True, colors="gray",linewidths=0.8)
# m.drawcountries(linewidth=1.5, color='black', zorder=3)
# m.drawcoastlines(linewidth=1.2,color='gray')
# plt.title('June 2020 Temperature Anomaly vs 2015-2019 (ERA5)',fontsize=16)
# cbar=plt.colorbar(im,ticks=np.arange(-200,200.01,20.),fraction=0.046, pad=0.04,extend='both',boundaries=[-6]+list(np.arange(-5,5.01,1)+[6]))
# cbar.set_label(r'$\Delta P$ [mm]',fontsize=14)
# cbar.ax.tick_params(labelsize=14)
# fig.tight_layout(rect=(0,0,1,1),h_pad=0.1,w_pad=0.1,pad=0.1)


# fig = plt.figure(3,figsize=(8, 7))
# m = Basemap(projection='cyl', llcrnrlat=40,urcrnrlat=52,\
#             llcrnrlon=9,urcrnrlon=21,resolution='h')
# im=m.contourf(lon, lat, rel_anomalies, np.arange(-0.5,0.51,0.025),latlon=True, cmap='BrBG')
# # m.contour(lon, lat, tp_season[-2] - tp_season_clim, np.arange(-200,200.01,20.),latlon=True, colors="gray",linewidths=0.8)
# m.drawcountries(linewidth=1.5, color='black', zorder=3)
# m.drawcoastlines(linewidth=1.2,color='gray')
# plt.title('June-July-August Mean Precipitation Change 1981-2019 (ERA5)',fontsize=16)
# cbar=plt.colorbar(im,ticks=np.arange(-0.5,0.501,0.1),fraction=0.046, pad=0.04,extend='both',boundaries=[-6]+list(np.arange(-5,5.01,1)+[6]))
# cbar.set_label(r'$\Delta P/<P>$ [%]',fontsize=14)
# cbar.ax.tick_params(labelsize=14)
# fig.tight_layout(rect=(0,0,1,1),h_pad=0.1,w_pad=0.1,pad=0.1)