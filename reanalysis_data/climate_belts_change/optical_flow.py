#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 02:24:11 2021

@author: ziga
"""

import matplotlib.pyplot as plt

import cv2 as cv
import numpy as np

lsm = np.load("lsm.npy")
t2m = np.load("t2m.npy")
lons = np.load("lons.npy")
lats = np.load("lats.npy")
data_cv = np.load("data_cv.npy")
data_10yrt = np.load("data_10yrt.npy")

data_10yrt = 255/data_10yrt.max()*data_10yrt//1

#flow = cv.calcOpticalFlowFarneback(data_10yrt[20], data_10yrt[61], None, 0.5, 3, 30, 20, 7, 1.2, 0)
flow = cv.calcOpticalFlowFarneback(data_cv[0,35], data_cv[61,35], None, 0.5, 3, 3, 20, 7, 1.5, 0)
#for i in range(1,60):
#    print(i)
#    flow = flow + cv.calcOpticalFlowFarneback(data_cv[i,30], data_cv[i+1,30], None, 0.5, 3, 15, 3, 5, 1.2, 0)


# # plot 2m-temperature
# plt.figure(1)
# plt.contour(lons_surf,lats_surf,lsm[0],[0.5],color="black",lw=2)
# plt.contourf(lons_surf,lats_surf,t2m2[-120:].mean(axis=0) - t2m1[:120].mean(axis=0),np.arange(0,3.5,0.1), cmap = plt.get_cmap("gist_rainbow_r"))
# plt.colorbar()

# plt.figure(2,figsize=(12,8))
# plt.contour(lons_surf,lats_surf,lsm[0],[0.5],color="black",lw=2)
# plt.contourf(lons_surf,lats_surf,t2m1[:120].mean(axis=0)-273,np.arange(0,26,0.5), cmap = plt.get_cmap("gist_rainbow_r"))
# plt.colorbar()

plt.figure(3,figsize=(12,8))
plt.contour(lons,lats,lsm,[0.5],color="black",lw=2)
plt.contourf(lons,lats,t2m[-120:].mean(axis=0),np.arange(0,26,0.5), cmap = plt.get_cmap("gist_rainbow_r"))
plt.colorbar()

plt.quiver(lons,lats,flow[:,:,0],flow[:,:,1])
plt.savefig("blah.png",dpi=300)