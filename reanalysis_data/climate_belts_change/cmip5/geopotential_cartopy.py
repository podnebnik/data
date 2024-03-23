#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 01:51:22 2021

@author: ziga
"""

import matplotlib.pyplot as plt
import numpy as np

import cartopy.crs as ccrs
from netCDF4 import *
from datetime import  *

file = Dataset("geopotential_2020.nc")["geopotential"]


d = datetime(2020,1,1)

for i in range(366):
    print(i)
    data = file[i]
    
    X=data[:,0]
    X=np.reshape(X,(X.size,1))
    data = np.concatenate((data[:,:],X),axis=1)
    
    ln = np.arange(0,360.1,1.)
    lt = np.arange(-90,90.1,1)
    lons,lats = np.meshgrid(ln,lt)
    
    fig = plt.figure(figsize=(5.9, 5))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())#ccrs.Orthographic(-10, 62))
    filled_c = ax.contourf(lons, lats, data,np.arange(45,60.5,0.5)*10**3,
                transform=ccrs.PlateCarree(),
                cmap='nipy_spectral')
    
    line_c = ax.contour(lons, lats, data, levels=filled_c.levels,linewidths=0.4,
                            colors=['black'],
                            transform=ccrs.PlateCarree())
    line_c2 = ax.contour(lons, lats, data, levels=[55*10**3],linewidths=2,
                            colors=['black'],
                            transform=ccrs.PlateCarree())
    
    ax.set_title(d.strftime("%d%b%Y"))
    
    ax.coastlines()
    ax.set_global()
    
    fig.colorbar(filled_c,ax=ax,fraction=0.025)#0.045)
    fig.tight_layout()
    plt.savefig("animation_figs/geopotential_robinson_{0:03d}.png".format(i),dpi=300)
    plt.clf()
    d = d + timedelta(days=1)
    

    
