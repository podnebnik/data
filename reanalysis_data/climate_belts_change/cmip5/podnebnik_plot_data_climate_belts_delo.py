#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 01:06:16 2021

@author: ziga
"""

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate
# import MEMD_all as memd

# load model orography and land-sea mask data

data = Dataset("../lsm_orog.nc","r")
lsm = data.variables["lsm"]
orog = data.variables["z"] # orography
lons_surf = data.variables["longitude"][:]
lats_surf = data.variables["latitude"][:]

# lons_surf1 = lons_surf1[arg_lon1:arg_lon2+1]
# lats_surf1 = lats_surf1[arg_lat1:arg_lat2+1]
# lsm = lsm[:,arg_lat1:arg_lat2+1,arg_lon1:arg_lon2+1]
# orog = orog[:,arg_lat1:arg_lat2+1,arg_lon1:arg_lon2+1]

var_all=["ensmean","perc25","perc75"]
for var in var_all:
  # load CMIP6 ensmean data 1850-2099 ensmean was obtained from anomalous tas from CMIP6 models and then ERA5 1981-2010 climatology was added on top
  data = Dataset("ensmean_perc25_perc75_18502099.nc","r")
  t2m = data.variables[var][:]
  lons_surf = data.variables["lon"][:]
  lats_surf = data.variables["lat"][:]
  # arg_lat1 = memd.findNearestIndex(lats_surf, 30.)
  # arg_lat2 = memd.findNearestIndex(lats_surf, 55.)
  # arg_lon1 = memd.findNearestIndex(lons_surf, 0.)
  # arg_lon2 = memd.findNearestIndex(lons_surf, 30.)
  # lons_surf = lons_surf[arg_lon1:arg_lon2+1]
  # lats_surf = lats_surf[arg_lat1:arg_lat2+1]

  # t2m = t2m[:,arg_lat1:arg_lat2+1,arg_lon1:arg_lon2+1]

  # merge data and transform from kelvin to celsius scale
  t2m = t2m - 273.15
  n = t2m.shape[0]

  # compute 10-year running means
  data = t2m
  data1 = np.reshape(data,(len(data[:,0,0]),len(data[0,:,0])*len(data[0,0,:]))) # reshape 4D to 2D data
  df = pd.DataFrame(data1) # get dataframe
  data1 = df.rolling(window=10,min_periods=1,axis=0,center=True).mean().iloc[:,:].values  # running mean
  data_10yrt = np.reshape(data1,(len(data[:,0,0]),len(data[0,:,0]),len(data[0,0,:]))) # 2D data back to 4D data


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
  if not os.path.exists(path+var+"_difference_{:02d}".format(T)):
      os.mkdir(path+var+"_difference_{:02d}".format(T))

  for i in range(5,n+5,10):
      fig=plt.figure(5,figsize=(12,8))
      plt.title("Povprečna letna temperatura na 2 metrih, {0:4d}-{1:4d}".format(1850+i-5,1850+9+i-5),fontsize=16)
      plt.contour(lons_surf1,lats_surf1,lsm[0],[0.5],color="black",linewidth=4)
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
      plt.savefig(path+var+"_difference_{0:02d}/difference_{1:4d}_{2:4d}.png".format(T,1850+i-5,1850+9+i-5),dpi=300)
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

  var = "ensmean"

  # T to T+1 °C temperature belt
  T = 20
  if not os.path.exists(var+"_2difference_{:02d}".format(T)):
      os.mkdir(var+"_2difference_{:02d}".format(T))
  j=0
  for i in range(5,n+5,10):
      print(i)
      fig=plt.figure(5,figsize=(12,8))
      plt.title("Povprečna letna temperatura na 2 metrih, {0:4d}-{1:4d}".format(1850+i-5,1850+9+i-5),fontsize=16)
      
      # perform interpolation
      xx = np.arange(0,360,0.25)
      yy = np.arange(0,180.1,0.25)
      
      tint = interpolate.interp2d(lons_surf,lats_surf,data_10yrt[i],kind='cubic')
      t2m_int = tint(xx,yy)
      
      plt.contour(lons_surf1,lats_surf1,lsm[0],[0.5],color="black",linewidth=4)
      plt.contourf(xx,yy,t2m_int,np.arange(0,23,1), cmap = cmap,extend="both",hatches=(T+1)*[None]+['//']+5*[None])
      cbar = plt.colorbar()
      cbar.set_label("Temperatura [°C]",fontsize=16)
      for t in cbar.ax.get_yticklabels():
            t.set_fontsize(16)
      
      plt.contour(xx,yy,t2m_int, [T,T+1], colors="grey")
      # plt.contourf(lons_surf,lats_surf,data_10yrt[i], np.arange(T,T+1.1,1), cmap=plt.get_cmap("Greys"),alpha=0.8, hatches='.')
      plt.grid()
      
      plt.xlim([0,30])
      plt.ylim([30,54])
      plt.xlabel("Geografska dolžina [°]",fontsize=16)
      plt.ylabel("Geografska širina [°]",fontsize=16)
      
      fig.tight_layout()
      j+=1
      # plt.savefig(var+"_2difference_{0:02d}/difference_{1:4d}_{2:4d}.png".format(T,1850+i-5,1850+9+i-5),dpi=300)
      plt.savefig(var+"_2difference_{0:02d}/difference_{1:02d}.png".format(T,j),dpi=300)
      plt.clf()
      
          
    