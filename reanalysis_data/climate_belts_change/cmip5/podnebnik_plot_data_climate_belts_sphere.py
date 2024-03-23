#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 01:06:16 2021

@author: ziga
"""

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
import matplotlib.ticker as mticker
import cartopy.crs as ccrs

from cartopy.mpl.ticker import (LongitudeFormatter, LatitudeFormatter,
                                LatitudeLocator)

import cartopy.feature as cf
import pandas as pd


#%%
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


#%%
# load model orography and land-sea mask data

data = Dataset("../lsm_orog.nc","r")
lsm = data.variables["lsm"]
orog = data.variables["z"] # orography
lons_surf = data.variables["longitude"][:]
lats_surf = data.variables["latitude"][:]

# T to T+1 °C temperature belt
T = 20


var_all=["ensmean"]#,"perc25","perc75"]

for var in var_all:
    
    try:
        os.mkdir(var+"_2difference_sphere_{:02d}_limited".format(T))
    except FileExistsError:
        pass

    # load CMIP6 ensmean data 1850-2099 ensmean was obtained from anomalous tas from CMIP6 models and then ERA5 1981-2010 climatology was added on top
    file = Dataset("ensmean_perc10_perc90_one_per_centre_18502099.nc","r")
    t2m = file.variables[var][:]
    lons_surf = file.variables["lon"][:]
    lats_surf = file.variables["lat"][:]
    
    # merge data and transform from kelvin to celsius scale
    t2m = t2m - 273.15
    n = t2m.shape[0]
    
    # compute 10-year running means
    data = t2m
    data1 = np.reshape(data,(len(data[:,0,0]),len(data[0,:,0])*len(data[0,0,:]))) # reshape 4D to 2D data
    df = pd.DataFrame(data1) # get dataframe
    data1 = df.rolling(window=10,min_periods=1,axis=0,center=True).mean().iloc[:,:].values  # running mean
    data_10yrt = np.reshape(data1,(len(data[:,0,0]),len(data[0,:,0]),len(data[0,0,:]))) # 2D data back to 4D data

  
    j=0# 0. 5
    for i in range(6,n+5,10):
        print(i)
        
        # perform interpolation
        xx = np.arange(0,360,0.25)
        yy = np.arange(-90.,90.1,0.25)
        
        tint = interpolate.interp2d(lons_surf,lats_surf,data_10yrt[i],kind='cubic')
        t2m_int = tint(xx,yy)
        data = t2m_int[:]
        X=data[:,0]
        X=np.reshape(X,(X.size,1))
        data = np.concatenate((data[:,:],X),axis=1)
        
        ln = np.arange(0,360.1,0.25)
        lt = np.arange(-90,90.1,0.25)
        lons,lats = np.meshgrid(ln,lt)
        
#   plt.figure(figsize=(9, 9))
# ax = plt.axes(projection=cartopy.crs.TransverseMercator(32))
# ax.add_feature(cartopy.feature.BORDERS, linestyle='-', alpha=1)
# ax.coastlines(resolution='110m')
# ax.add_feature(cartopy.feature.OCEAN, facecolor=(0.5,0.5,0.5))
# ax.gridlines()
# ax.set_extent ((-7.5, 50, 34, 69), cartopy.crs.PlateCarree())
# plt.show()
        
#       obmocje = np.arange(-8,28.,1.)
        obmocje = np.arange(-2,26.,1.)
        hatches = [None if x != T else '////' for x in obmocje]
        
        fig = plt.figure(figsize=(9, 9))
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.TransverseMercator(32))#ccrs.Orthographic(-10, 42))
        filled_c = ax.contourf(lons, lats, data, obmocje,
                    transform=ccrs.PlateCarree(),
                    cmap=cmap,extend='both',hatches=hatches)
        
        # line_c = ax.contour(lons, lats, data, levels=filled_c.levels,linewidths=0.4,
        #                         colors=['black'],
        #                         transform=ccrs.PlateCarree())
        # line_c2 = ax.contour(lons, lats, data, levels=[55*10**3],linewidths=2,
        #                         colors=['black'],
        #                         transform=ccrs.PlateCarree())
        
        ax.set_title("Povprečna letna temperatura na 2 metrih, {0:4d}-{1:4d}".format(1850+i-5,1850+9+i-5),fontsize=14)
        
        bodr = cf.NaturalEarthFeature(category='cultural', 
    name='admin_0_boundary_lines_land', scale='10m', facecolor='none', alpha=0.7)
        # https://stackoverflow.com/questions/62308857/borders-and-coastlines-interfering-in-python-cartopy
        
        ax.coastlines(resolution='10m')
        ax.add_feature(bodr, linestyle='-')
        # ax.set_global()
        # ax.add_feature(cf.OCEAN,facecolor=(0.5,0.5,0.5))
        
        ax.set_extent ((-7.5, 50, 26, 69), ccrs.PlateCarree())
        # ax.set_extent ((-7.5, 40, 29, 62), ccrs.PlateCarree())
        
        # ax.set_xticks([-15,0,15,30,45,60], ccrs.PlateCarree())
        # ax.set_xticklabels([120., 140., 160., 180., -160., -140., -120.], color='red', weight='bold')
        # ax.set_yticks([30,40,50,60], ccrs.PlateCarree())
        # ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
        
        
        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='white', alpha=0.5, linestyle='-')
        gl.top_labels = False
        gl.left_labels = False
        # gl.xlines = False
        gl.xlocator = mticker.FixedLocator([-15,0,15,30,45,60])
        gl.ylocator = LatitudeLocator()
        gl.xformatter = LongitudeFormatter()
        
        
        fig.colorbar(filled_c,ax=ax,fraction=0.025,pad=0.07,label="°C")#0.045)
        fig.tight_layout()
        
        
        j+=1
        # plt.savefig(var+"_2difference_{0:02d}/difference_{1:4d}_{2:4d}.png".format(T,1850+i-5,1850+9+i-5),dpi=300)
        plt.savefig(var+"_2difference_sphere_{0:02d}_limited_highres/difference_{1:03d}.png".format(T,j),dpi=600)
        plt.clf()
            
        
        
        # fig=plt.figure(5,figsize=(12,8))
        
        
        # # perform interpolation
        # xx = np.arange(0,360,0.25)
        # yy = np.arange(0,180.1,0.25)
        
        # tint = interpolate.interp2d(lons_surf,lats_surf,data_10yrt[i],kind='cubic')
        # t2m_int = tint(xx,yy)
        
        # plt.contour(lons_surf1,lats_surf1,lsm[0],[0.5],color="black",linewidth=4)
        # plt.contourf(xx,yy,t2m_int,np.arange(0,23,1), cmap = cmap,extend="both",hatches=(T+1)*[None]+['//']+5*[None])
        # cbar = plt.colorbar()
        # cbar.set_label("Temperatura [°C]",fontsize=16)
        # for t in cbar.ax.get_yticklabels():
        #       t.set_fontsize(16)
        
        # plt.contour(xx,yy,t2m_int, [T,T+1], colors="grey")
        # # plt.contourf(lons_surf,lats_surf,data_10yrt[i], np.arange(T,T+1.1,1), cmap=plt.get_cmap("Greys"),alpha=0.8, hatches='.')
        # plt.grid()
        
        # plt.xlim([0,30])
        # plt.ylim([30,54])
        # plt.xlabel("Geografska dolžina [°]",fontsize=16)
        # plt.ylabel("Geografska širina [°]",fontsize=16)
        
        # fig.tight_layout()
        # j+=1
        # # plt.savefig(var+"_2difference_{0:02d}/difference_{1:4d}_{2:4d}.png".format(T,1850+i-5,1850+9+i-5),dpi=300)
        # plt.savefig(var+"_2difference_{0:02d}/difference_{1:02d}.png".format(T,j),dpi=300)
        # plt.clf()
        
            
    