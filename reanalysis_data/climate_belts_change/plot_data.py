#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 01:06:16 2021

@author: ziga
"""

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np

# data = Dataset("tas_Amon_CESM1-CAM5_historical_r1i1p1_185001-200512.nc","r")

# lons = data.variables["lon"][:]
# lats = data.variables["lat"][:]

# t2m = data.variables["tas"]
# # evap = data.variables["e"]

# plt.contourf(lons,lats,t2m[-360:].mean(axis=0)-t2m[:360].mean(axis=0));plt.colorbar()

data = Dataset("lsm_orog.nc","r")
lons_surf = data.variables["longitude"][:]
lats_surf = data.variables["latitude"][:]
lsm = data.variables["lsm"]
orog = data.variables["z"] # orography

# # plot land sea mask
# plt.contour(lons_surf,lats_surf,lsm[0],[0.5],color="black",lw=2)
# plt.contour(lons_surf,lats_surf,orog[0],np.array([200,500,1000,1500,2000,2500])* 9.806,color="gray",lw=0.5)

data1 = Dataset("era5_1950_1978.nc","r")
t2m1 = data1.variables["t2m"]

data2 = Dataset("era5_1979_2020.nc","r")
t2m2 = data2.variables["t2m"]

# # plot 2m-temperature
# plt.figure(1)
# plt.contour(lons_surf,lats_surf,lsm[0],[0.5],color="black",lw=2)
# plt.contourf(lons_surf,lats_surf,t2m2[-120:].mean(axis=0) - t2m1[:120].mean(axis=0),np.arange(0,3.5,0.1), cmap = plt.get_cmap("gist_rainbow_r"))
# plt.colorbar()

# plt.figure(2,figsize=(12,8))
# plt.contour(lons_surf,lats_surf,lsm[0],[0.5],color="black",lw=2)
# plt.contourf(lons_surf,lats_surf,t2m1[:120].mean(axis=0)-273,np.arange(0,26,0.5), cmap = plt.get_cmap("gist_rainbow_r"))
# plt.colorbar()

# plt.figure(3,figsize=(12,8))
# plt.contour(lons_surf,lats_surf,lsm[0],[0.5],color="black",lw=2)
# plt.contourf(lons_surf,lats_surf,t2m2[-120:].mean(axis=0)-273,np.arange(0,26,0.5), cmap = plt.get_cmap("gist_rainbow_r"))
# plt.colorbar()

t2m = np.concatenate((t2m1,t2m2),axis=0) - 273
n = t2m.shape[0]

# data_cv = np.zeros((62,52,97,121))

# data_cv_ref = np.zeros((52,97,121))

# for t in range(0,52):
#     data_cv_ref[t] = (t2m[:120].mean(axis=0) > t/2)


# for i in range(0,n-120+1,12):
#     print(i,i//12)
#     for t in range(0,52):
#         data_cv[i//12,t] = (t2m[i:i+120].mean(axis=0) > t/2)


data_10yrt = np.zeros((62,97,121))
for i in range(0,n-120+1,12):
    data_10yrt[i//12] = t2m[i:i+120].mean(axis=0) 


# plt.figure(1)
# plt.contour(lons_surf,lats_surf,lsm[0],[0.5],color="black",lw=2)
# plt.contourf(lons_surf,lats_surf,data_10yrt[61] - data_10yrt[60],np.arange(0,1,0.05), cmap = plt.get_cmap("gist_rainbow_r"))
# plt.colorbar()


plt.figure(2)
plt.contour(lons_surf,lats_surf,lsm[0],[0.5],color="black",lw=2)
plt.contourf(lons_surf,lats_surf,data_10yrt[61],np.arange(0,26,0.5), cmap = plt.get_cmap("gist_rainbow_r"))
# plt.contourf(lons_surf,lats_surf,data_10yrt[61] - data_10yrt[15],np.arange(0,3.5,0.1), cmap = plt.get_cmap("gist_rainbow_r"))
plt.colorbar()
u,v = np.gradient(data_10yrt[0])
plt.quiver(lons_surf,lats_surf,v,-u,angles='xy',scale=100)
plt.savefig("blah.png",dpi=300)

#%%
T2 = data_10yrt[61]
T1 = data_10yrt[0]
gradTy,gradTx = np.gradient(data_10yrt.mean(axis=0))

gradTabs = np.maximum((gradTy**2+gradTx**2)**0.5,np.zeros((97,121))+0.1)
xabs = (T2-T1)/gradTabs

dx = gradTx/ gradTabs*xabs
dy = gradTy/ gradTabs*xabs

length = np.sqrt(dx**2 + dy**2) 

plt.figure(3,figsize=(14,10))
plt.contour(lons_surf,lats_surf,lsm[0],[0.5],color="black",lw=2)
plt.contourf(lons_surf,lats_surf,data_10yrt[61],np.arange(0,26,0.5), cmap = plt.get_cmap("gist_ncar"))
# plt.contourf(lons_surf,lats_surf,data_10yrt[61] - data_10yrt[15],np.arange(0,3.5,0.1), cmap = plt.get_cmap("gist_rainbow_r"))
plt.colorbar()

# plt.quiver(lons_surf,lats_surf,-dx,dy,angles='xy',scale_units='xy',scale=5,color="gray",width=0.001)

lw = (3 * length / length.max()) 
plt.streamplot(lons_surf,lats_surf,-dx,dy,color="black",density=5,zorder=3,linewidth=lw,arrowstyle="fancy")

plt.xlim([0,30])
plt.ylim([30,54])


plt.savefig("blah2.png",dpi=300)

#%%
offset = 0.001
dyear  = 5

n = 61//dyear

lons_year = np.zeros((n,97,121))
lats_year = np.zeros((n,97,121))

lons_year[:,:] = lons_surf
for i in range(97):
    lats_year[:,i,:] = lats_surf[i]


j = 0
for i in range(0,61-dyear,dyear):
    print(i)
    T2 = data_10yrt[i+dyear]
    T1 = data_10yrt[i]
    gradTy,gradTx = np.gradient((data_10yrt[i]+data_10yrt[i+dyear])/2.)
    
    gradTabs = np.maximum((gradTy**2+gradTx**2)**0.5,np.zeros((97,121))+offset)
    xabs = (T2-T1)/gradTabs
    
    dx = gradTx/ gradTabs*xabs
    dy = gradTy/ gradTabs*xabs
    
    lons_year[j] = lons_year[j] +- dx
    lats_year[j] = lats_year[j] + dy
    
    j+=1

# def runningMeanFast(x, N):
#     return np.convolve(x, np.ones((N,))/N)[(N-1):]

# lons_year_smooth = np.zeros((n,97,121))
# lats_year_smooth = np.zeros((n,97,121))
# for j in range(0,97):
#     for i in range(0,121):
#         lons_year_smooth[:,j,i] = runningMeanFast(lons_year[:,j,i], 3)
#         lats_year_smooth[:,j,i] = runningMeanFast(lats_year[:,j,i], 3)

#%%

plt.figure(3)
plt.contour(lons_surf,lats_surf,lsm[0],[0.5],color="black",lw=2)
plt.contourf(lons_surf,lats_surf,data_10yrt[61],np.arange(0,26,0.5), cmap = plt.get_cmap("gist_rainbow_r"))
# plt.contourf(lons_surf,lats_surf,data_10yrt[61] - data_10yrt[15],np.arange(0,3.5,0.1), cmap = plt.get_cmap("gist_rainbow_r"))
plt.colorbar()

# for j in range(0,97,2):
#     for i in range(0,121,2):
#         plt.plot(lons_year[:,j,i],lats_year[:,j,i],"k-",lw=0.05)
# plt.plot(lons_year[:,10,20],lats_year[:,10,20],"k-",lw=0.5)
# plt.plot(lons_year[:,80,77],lats_year[:,80,73],"k-",lw=0.5)

# plt.plot(lons_year_smooth[:,10,20],lats_year_smooth[:,10,20],"r-",lw=0.05)
# plt.plot(lons_year_smooth[:,80,77],lats_year_smooth[:,80,77],"r-",lw=0.05)

plt.quiver(lons_surf,lats_surf,\
            lons_year[-1]-lons_year[0],\
            lats_year[-1]-lats_year[0],\
                angles='xy')


plt.xlim([0,30])
plt.ylim([30,54])

# u,v = np.gradient(data_10yrt[0])
# plt.quiver(lons_surf,lats_surf,-dx,dy,angles='xy',scale=200)
plt.savefig("translation.png",dpi=300)  



# gradTy = -gradTy

# def fun_min(dX,T2,T1,gradTx,gradTy):
#     dy,dx = dX.reshape(2,97,121)
#     return np.sum((T2-T1 + dx*gradTx + dy*gradTy)**2)

# # def jac_fun(dX,T2,T1,gradTx,gradTy):
# #     dy,dx = dX
# #     return 2*(T2-T1 + dx*gradTx + dy*gradTy)*

# dx0 = np.array((np.zeros((97,121)),np.zeros((97,121))))

# from scipy.optimize import minimize
# result  = minimize(fun_min,dx0.flatten(),args=(T2,T1,gradTx,gradTy),options={'disp':True})

# dy,dx = (result.x).reshape(2,97,121)


# for i in range(0,61,5):
#     u,v = np.gradient(data_10yrt[i])

# np.save("lsm",np.array(lsm[0]))
# np.save("t2m",np.array(t2m)) 
# np.save("lons",np.array(lons_surf))
# np.save("lats",np.array(lats_surf))  
# np.save("data_10yrt",data_10yrt)     
# np.save("data_cv",data_cv)    

# plt.colorbar()
# plt.xlabel("geografska dolžina")
# plt.ylabel("geografska širina")
# plt.title("Mean 2-meter temperature, October 2020")


#%%

plt.figure(4,figsize=(14,10))
plt.contour(lons_surf,lats_surf,lsm[0],[0.5],color="black",lw=2)
plt.contourf(lons_surf,lats_surf,data_10yrt[60],np.arange(0,26,0.5), cmap = plt.get_cmap("gist_ncar"))
plt.colorbar()

plt.contour(lons_surf,lats_surf,data_10yrt[60], [9,10], colors="grey")
plt.contourf(lons_surf,lats_surf,data_10yrt[60], np.arange(9,10.1,1), cmap=plt.get_cmap("Greys"),alpha=0.8, hatches='.')


plt.xlim([0,30])
plt.ylim([30,54])

plt.savefig("difference4_2010s.png",dpi=300)


#%%

plt.figure(5,figsize=(14,10))
plt.contour(lons_surf,lats_surf,lsm[0],[0.5],color="black",lw=2)
plt.contourf(lons_surf,lats_surf,data_10yrt[50],np.arange(0,26,0.5), cmap = plt.get_cmap("gist_ncar"))
plt.colorbar()

plt.contour(lons_surf,lats_surf,data_10yrt[50], [9,10], colors="grey")
plt.contourf(lons_surf,lats_surf,data_10yrt[50], np.arange(9,10.1,1), cmap=plt.get_cmap("Greys"),alpha=0.8, hatches='.')


plt.xlim([0,30])
plt.ylim([30,54])

plt.savefig("difference4_2000s.png",dpi=300)
