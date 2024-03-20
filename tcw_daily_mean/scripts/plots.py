#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 13:13:29 2023

@author: ziga
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import matplotlib.dates as mdates



#%% VARIABLE
var = "tcw"


today = date.today()
day_of_year = (today - date(today.year, 1, 1)).days + 1

#%% plot annual mean 2m temperature in Slovenia between 1940 and 2022

var_annual_means = pd.read_csv("../data/{0}_annual_means.csv".format(var))

# Get today's date and day of year
today = date.today()
day_of_year = (today - date(today.year, 1, 1)).days + 1

# Read in annual mean TCW data for Slovenia
with open("../data/{0}_annual_means.csv".format(var), "r") as f:
    data = pd.read_csv(f)

# Plot the data
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(data["Year"].values, data[var].values, "r-")
ax.set_xlabel("Year")
ax.set_ylabel("Total column water [kg/m$^2$]")
ax.set_title("Annual mean total column water over Slovenia (1940-2022)")
ax.grid()
plt.tight_layout()


#%% contour plot of daily 2m temperature in Slovenia

var_daily = pd.read_csv("../data/{0}_table_doy.csv".format(var))
cols = list(range(1,85))  # columns 1, 3, and 4 (0-indexed)
data = var_daily.iloc[:, cols].values

fig = plt.figure(2,figsize=(10,4.))
ax = fig.add_subplot(111)
cnt=ax.contourf(range(1940,2024),var_daily["Day_of_year"].values,data,np.arange(0,30.1,2.,),\
                cmap=plt.get_cmap("terrain_r"),extend='max',interpolation='none')

# ax.set_title("Annual mean total column water over Slovenia (1940-2023)",fontsize=16)
ax.set_title("Količina vode v atmosferskem stolpcu nad Slovenijo (1940-2023)",fontsize=16)
ax.set_xlabel("Leto",fontsize=14)
ax.set_ylabel(r"Dan v letu",fontsize=14)
ax.grid()
cbar = fig.colorbar(cnt,pad=0.01)
# cbar.ax.set_ylabel(r'Total column water [kg/m$^2$]')
cbar.ax.set_ylabel(r'Količina vode [kg/m$^2$]')
plt.tight_layout()
fig.savefig("../plots/tcw_slovenia_daily_raw.png",dpi=300)


#%% plot annual mean total column water vapour in Slovenia between 1940 and 2022
tcw_summer=data[151:243].mean(axis=0)
tcw_annual=data.mean(axis=0)

# Plot the data
fig, ax = plt.subplots(figsize=(8, 5))
# ax.plot(range(1940,2023), tcw_annual[:-1], "r-",label="Annual mean")
ax.plot(range(1940,2024), tcw_summer, "r-")
ax.set_xlabel("Year")
ax.set_ylabel("Total column water [kg/m$^2$]")
ax.set_title("Summer (JJA) total column water over Slovenia (1940-2022)")
ax.grid()
plt.tight_layout()
fig.savefig("../plots/tcw_slovenia_summer.png")

#%%
# Plot the data
fig, ax = plt.subplots(figsize=(8, 5))
# ax.plot(range(1940,2023), tcw_annual[:-1], "r-",label="Annual mean")
ax.hist((data[151:243,22:52]).flatten(),np.arange(6,40.1,1.),density=True,label="1961-1990",color="brown",alpha=0.5)
ax.hist((data[151:243,75:85]).flatten(),np.arange(6,40.1,1.),density=True,label="2014-2023",color="blue",alpha=0.5)
ax.set_xlabel("Total column water [kg/m$^2$]")
ax.set_ylabel("Probability density")
ax.set_title("Summer (JJA) total column water over Slovenia")
ax.grid()
ax.legend()
plt.tight_layout()
fig.savefig("../plots/tcw_slovenia_summer_histogram.png")

#%%
# Plot the data
fig, ax = plt.subplots(figsize=(8, 5))
# ax.plot(range(1940,2023), tcw_annual[:-1], "r-",label="Annual mean")
ax.hist((data[151:243,22:52]).flatten(),np.arange(6,40.1,1.),density=True,label="1961-1990",color="brown",alpha=0.6,edgecolor="k")
ax.hist((data[151:243,75:85]).flatten(),np.arange(6,40.1,1.),density=True,label="2014-2023",color="blue",alpha=0.6,edgecolor="k")
ax.set_xlabel("Količina vode [kg/m$^2$]")
ax.set_ylabel("Verjetnostna gostota")
ax.set_title("Količina vode v stolpcu nad Slovenijo (JJA)")
ax.grid()
ax.legend()
plt.tight_layout()
fig.savefig("../plots/tcw_slovenia_summer_histogram_slo.png")

#%% contour plot of daily 2m temperature in Slovenia
import numpy.ma as ma
# Load data from CSV
t2m_daily = pd.read_csv("../data/t2m_table_doy.csv")
cols = list(range(1, 85))  # columns 1 to 84 (0-indexed)
data = t2m_daily.iloc[:, cols].values

# Create a figure and axis
fig, ax = plt.subplots(figsize=(20,6))

# Define x (years) and y (day of year) values
years = np.arange(1940, 2024)
doys= t2m_daily["Day_of_year"].values

# Define the levels for the color contour
levels = np.arange(-10, 23, 2)

data = data-273.15


# Create a pcolormesh plot
pcm = ax.pcolormesh(years, doys, data, cmap=plt.get_cmap("nipy_spectral"), vmin=-10, vmax=22)

# Set labels and title
ax.set_xlabel("Leto", fontsize=14)
ax.set_ylabel("Dan v letu", fontsize=14)
ax.grid()

# Add a colorbar
cbar = fig.colorbar(pcm, pad=0.01,extend='both')
cbar.ax.set_ylabel(r'Povprečna dnevna T na 2 m [$^\circ$C]')

# Save the figure
plt.tight_layout()
fig.savefig("../plots/t2m_slovenia_daily_raw_pcolormesh.png")

# Show the plot (optional)
plt.show()

#%% contour plot of daily 2m temperature in Slovenia - 15-day moving average

t2m_daily = pd.read_csv("../data/t2m_table_doy_ma_7day.csv")
cols = list(range(1,84))  # columns 1, 3, and 4 (0-indexed)
data = t2m_daily.iloc[:, cols].values

fig = plt.figure(3,figsize=(20,6))
ax = fig.add_subplot(111)
cnt=ax.contourf(range(1941,2024),t2m_daily["Day_of_year"].values,data-273.15,np.arange(-10,23,2.,),cmap=plt.get_cmap("nipy_spectral"),extend='both')
ax.set_xlabel("Leto",fontsize=14)
ax.set_ylabel(r"Dan v letu",fontsize=14)
ax.grid()
cbar = fig.colorbar(cnt,pad=0.01)
cbar.ax.set_ylabel(r'Povprečna dnevna T na 2 m [$^\circ$C]')
fig.tight_layout()
fig.savefig("../plots/t2m_slovenia_daily_7dayma.png")



#%% contour plot of daily 2m temperature in Slovenia - 15-day moving average

t2m_daily = pd.read_csv("../data/t2m_table_doy_ma_15day.csv")
cols = list(range(1,84))  # columns 1, 3, and 4 (0-indexed)
data = t2m_daily.iloc[:, cols].values

fig = plt.figure(4,figsize=(20,6))
ax = fig.add_subplot(111)
cnt=ax.contourf(range(1941,2024),t2m_daily["Day_of_year"].values,data-273.15,np.arange(-10,23,2.,),cmap=plt.get_cmap("nipy_spectral"),extend='both')
ax.set_xlabel("Leto",fontsize=14)
ax.set_ylabel(r"Dan v letu",fontsize=14)
ax.grid()
cbar = fig.colorbar(cnt,pad=0.01)
cbar.ax.set_ylabel(r'Povprečna dnevna T na 2 m [$^\circ$C]')
plt.tight_layout()
fig.savefig("../plots/t2m_slovenia_daily_15dayma.png")



#%% contour plot of daily 2m temperature in Slovenia - 31-day moving average

t2m_daily = pd.read_csv("../data/t2m_table_doy_ma_31day.csv")
cols = list(range(1,84))  # columns 1, 3, and 4 (0-indexed)
data = t2m_daily.iloc[:, cols].values

fig = plt.figure(4,figsize=(20,6))
ax = fig.add_subplot(111)
cnt=ax.contourf(range(1941,2024),t2m_daily["Day_of_year"].values,data-273.15,np.arange(-10,23,2.,),cmap=plt.get_cmap("nipy_spectral"),extend='both')
ax.set_xlabel("Leto",fontsize=14)
ax.set_ylabel(r"Dan v letu",fontsize=14)
ax.grid()
cbar = fig.colorbar(cnt,pad=0.01)
cbar.ax.set_ylabel(r'Povprečna dnevna T na 2 m [$^\circ$C]')
plt.tight_layout()
fig.savefig("../plots/t2m_slovenia_daily_31dayma.png")



#%% contour plot of daily 2m temperature in Slovenia - 31-day moving average + change of average day with 10°C daily mean temperature

# add lines which mark average day_of_year with 10°C mean daily T
def find_day(x,y,value):
    # Perform linear interpolation
    for i in range(len(x)-1):
        # print(i,y[i],value,y[i+1])
        if y[i] <= value <= y[i+1] or y[i] >= value >= y[i+1]:
            x_value = x[i] + (value-y[i])*(x[i+1]-x[i])/(y[i+1]-y[i])
            break
    return x_value

t2m_daily = pd.read_csv("../data/t2m_table_doy_ma_61day.csv")
cols = list(range(1,83))  # columns 1, 3, and 4 (0-indexed)
data = t2m_daily.iloc[:, cols].values

data_half1 = data[:183,:]
data_half2 = data[183:,:]
doy1 = np.arange(1,184)
doy2 = np.arange(184,366)

# Value to interpolate
value = 283 # K = 10°C

day_value1 = np.zeros(82)
day_value2 = np.zeros(82)

for k in range(82):
    day_value1[k] = find_day(doy1,data_half1[:,k],value)
    day_value2[k] = find_day(doy2,data_half2[:,k],value)

times = np.arange(1941,2023)
c10_1 = np.polyfit(times, day_value1, 1)
c10_2 = np.polyfit(times, day_value2, 1)


fig = plt.figure(5,figsize=(20,6))
ax = fig.add_subplot(111)
cnt=ax.contourf(range(1941,2023),t2m_daily["Day_of_year"].values,data-273.15,np.arange(-10,23,2.,),cmap=plt.get_cmap("nipy_spectral"),extend='both')
ax.set_xlabel("Leto",fontsize=14)
ax.set_ylabel(r"Dan v letu",fontsize=14)
ax.grid()
ax.plot(times, times*c10_1[0]+c10_1[1],"k--")
ax.plot(times, times*c10_2[0]+c10_2[1],"k--")
cbar = fig.colorbar(cnt,pad=0.01)
cbar.ax.set_ylabel(r'Povprečna dnevna T na 2 m [$^\circ$C]')
plt.tight_layout()
fig.savefig("../plots/t2m_slovenia_daily_61dayma.png")


#%% contour plot of monthly-mean 2m temperature in Slovenia

t2m_monthly_means = pd.read_csv("../data/t2m_table_monthly_means.csv")
cols = list(range(1,13))  # columns 1, 3, and 4 (0-indexed)
data = t2m_monthly_means.iloc[:, cols].values

fig = plt.figure(6,figsize=(20,6))
ax = fig.add_subplot(111)
cnt=ax.contourf(t2m_monthly_means["Year"].values,range(1,13),data.T-273.15,np.arange(-10,23,2.,),cmap=plt.get_cmap("nipy_spectral"),extend='both')
ax.set_xlabel("Leto",fontsize=14)
ax.set_ylabel(r"Mesec",fontsize=14)
ax.grid()
cbar = fig.colorbar(cnt)
cbar.ax.set_ylabel(r'Povprečna mesečna T na 2 m [$^\circ$C]')
plt.tight_layout()
fig.savefig("../plots/t2m_slovenia_monthly_means.png")



#%% contour plot of monthly-mean 2m temperature deviations from 1981-2010 climate mean

# compute deviations from 1981-2010

years = t2m_monthly_means["Year"].values
ind1 = np.argwhere(years==1981)[0,0]
ind2 = np.argwhere(years==2010)[0,0]

t2m_mean = data[ind1:ind2+1,:].mean(axis=0)

fig = plt.figure(7,figsize=(20,6))
ax = fig.add_subplot(111)
cnt=ax.contourf(t2m_monthly_means["Year"].values,range(1,13),data.T-t2m_mean.reshape((-1, 1)),np.arange(-7,7.1,1.,),cmap=plt.get_cmap("seismic"),extend='both')
ax.set_xlabel("Leto",fontsize=14)
ax.set_ylabel(r"Mesec",fontsize=14)

#indicate reference period
# ax.contourf(t2m_monthly_means["Year"].values,range(1,13), z, n_levels, colors='none',
#                   hatches=['\\\\'],
#                   extend='lower')

ax.grid()
cbar = fig.colorbar(cnt)
cbar.ax.set_ylabel(r'Odstopanje povprečne mesečne T na 2 m [$^\circ$C]')
plt.tight_layout()
fig.savefig("../plots/t2m_slovenia_monthly_means_deviations.png")


#%% plot of temperatures for the last 12 months - comparison to 1981-2010 mean and percentiles

isLeap = lambda x: x % 4 == 0 and (x % 100 != 0 or x % 400 == 0)

var_daily = pd.read_csv('../data/{0}.csv'.format(var))
var_daily["Date"] = pd.to_datetime(var_daily['Date'])

var_daily_7dayma = pd.read_csv('../data/{0}_ma_7day.csv'.format(var))
var_daily_7dayma["Date"] = pd.to_datetime(var_daily_7dayma['Date'])

ndays = var_daily.shape[0]
last_year = var_daily["Date"].dt.year[ndays-1]
    

ind2 = var_daily["tcw"].last_valid_index()

ind1 = ind2-365


var_daily_filtered = pd.read_csv('../data/{0}_table_doy_ma_7day.csv'.format(var))
year1 = 1961
year2 = 1990
col1 = np.argwhere(var_daily_filtered.columns==str(year1))[0,0]
col2 = np.argwhere(var_daily_filtered.columns==str(year2))[0,0]
cols = list(range(col1,col2+1))  # columns 1, 3, and 4 (0-indexed)
var_mean = (var_daily_filtered.iloc[:, cols].values).mean(axis=1)
var_mean_shifted = np.concatenate((var_mean[day_of_year:],var_mean[:day_of_year]))

fig = plt.figure(8,figsize=(14,6))
ax = fig.add_subplot(111)
ax.plot(var_daily["Date"][ind1:ind2],var_daily["tcw"][ind1:ind2],"k-",label="TCW")
# ax.plot(t2m_daily_7dayma["Date"][ndays-365:ndays],t2m_daily_7dayma["t2m"][ndays-365:ndays],"k-",label="$T_7$")
ax.plot(var_daily["Date"][ind1:ind2],var_mean_shifted,"r-",label="Mean TCW (1961-1990)")

ax.fill_between(var_daily["Date"][ind1:ind2], var_mean_shifted, var_daily["tcw"][ind1:ind2], var_mean_shifted>var_daily["tcw"][ind1:ind2],
                  color='brown', alpha=.4)
ax.fill_between(var_daily["Date"][ind1:ind2], var_mean_shifted, var_daily["tcw"][ind1:ind2], var_mean_shifted<var_daily["tcw"][ind1:ind2],
                  color='green', alpha=.4)

date_form = mdates.DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(date_form)

ax.set_ylabel(r"Total column water kg/m$^2$",fontsize=14)
ax.set_title("Daily mean total column water (TCW) in the last 365 days, and deviation from 7-day MA 1961-1990 (ECMWF ERA5)",fontsize=14)

# add ARSO recordings
timestamps = [pd.Timestamp('2023-06-07 00:00:00'),\
                  pd.Timestamp('2023-06-08 00:00:00'),\
                  pd.Timestamp('2023-06-09 00:00:00'),\
                  pd.Timestamp('2023-06-10 00:00:00'),\
                  pd.Timestamp('2023-06-11 00:00:00'),\
                  pd.Timestamp('2023-06-21 00:00:00'),\
                  pd.Timestamp('2023-06-22 00:00:00'),\
                  pd.Timestamp('2023-06-23 00:00:00'),\
                  pd.Timestamp('2023-06-27 00:00:00'),\
                  pd.Timestamp('2023-07-03 00:00:00'),\
                  pd.Timestamp('2023-07-12 00:00:00'),\
                  pd.Timestamp('2023-07-13 00:00:00'),\
                  pd.Timestamp('2023-07-17 00:00:00'),\
                  pd.Timestamp('2023-07-18 00:00:00'),\
                  pd.Timestamp('2023-07-19 00:00:00'),\
                  pd.Timestamp('2023-07-20 00:00:00'),\
                  pd.Timestamp('2023-07-21 00:00:00'),\
                  pd.Timestamp('2023-07-22 00:00:00'),\
                  pd.Timestamp('2023-07-24 00:00:00'),\
                  pd.Timestamp('2023-07-25 00:00:00'),\
                  pd.Timestamp('2023-07-26 00:00:00'),\
                  pd.Timestamp('2023-07-30 00:00:00'),\
                  pd.Timestamp('2023-08-01 00:00:00'),\
                  pd.Timestamp('2023-08-03 00:00:00'),\
                  pd.Timestamp('2023-08-04 00:00:00'),\
                  pd.Timestamp('2023-08-28 00:00:00'),\
                  pd.Timestamp('2023-08-29 00:00:00'),\
                  pd.Timestamp('2023-08-30 00:00:00'),\
                ]
ax.plot(timestamps,np.zeros(len(timestamps))+40,"bo",label="Extreme precipitation \nevent (summer)")

ax.legend(fontsize=14)
ax.grid()
plt.tight_layout()
fig.savefig("../plots/tcw_last_year.png")



#%%
# fig = plt.figure(2,figsize=(14,6))
# ax = fig.add_subplot(111)
# # ax.plot(dayofyr,t2m_running_mean,"k-",label="$\overline{T}$ (1981-2010)")
# #ax.fill_between(range(365),t2m_running_95,t2m_running_05,facecolor="k",alpha=0.3,label=r"5 - 95 perc")

# t2m_61_90_running_mean = np.convolve(np.concatenate((t2m_61_90_mean[-3:],t2m_61_90_mean,t2m_61_90_mean[:3])), np.ones(T)/T, mode='valid')
# ax.plot(dayofyr,t2m_61_90_running_mean,"k-",label="$\overline{T}$ (1961-1990)")


# ax.plot(dayofyr[:len(t2m_2022_running_mean)],t2m_2022_running_mean,"r-",label="T (2022)")

# # t2m_running_mean_red = t2m_running_mean[:len(t2m_2022_running_mean)]
# t2m_running_mean_red = t2m_61_90_running_mean[:len(t2m_2022_running_mean)]

# ax.fill_between(range(len(t2m_2022_running_mean)), t2m_running_mean_red, t2m_2022_running_mean, t2m_running_mean_red>t2m_2022_running_mean,
#                   color='blue', alpha=.4)
# ax.fill_between(range(len(t2m_2022_running_mean)), t2m_running_mean_red, t2m_2022_running_mean, t2m_running_mean_red<t2m_2022_running_mean,
#                   color='red', alpha=.4)

# ax.set_ylabel(r"$T$",fontsize=14)
# ax.set_xlabel("Datum")
# ax.set_title("Povprečje 1961-1990 (7-dnevno drseče) in odstopanje v 2022 (ECMWF ERA5)")

# # Major ticks
# ax.set_xticks([0,31,59,90,120,151,182,212,243,277,304,334])
# ax.set_xticklabels([])
# ax.tick_params(axis='x', which="major", length=5)

# # Minor ticks
# ax.set_xticks([15,45,74,105,135,166,197,227,258,292,319,349],minor=True)
# ax.set_xticklabels(["januar", "februar", "marec", "april","maj",\
#                     "junij", "julij", "avgust", "september",\
#                         "oktober","november", "december"],rotation=30,fontsize=13,minor=True)
# ax.tick_params(axis='x', which="minor",length=0)
# ax.legend(fontsize=14)
# ax.grid()
# plt.tight_layout()
# fig.savefig("t2m_2022_2.png")

#%%
# #%%

# dayofyr = np.arange(365)
# t2m = np.zeros((72,365))

# # READ DATA
# i = 0
# for yr in range(1981,2011):
#     data = netCDF4.Dataset("/media/ziga/DATADRIVE1/podnebne_spremembe/slovenija/t2m_"+str(yr)+".nc")
#     data_values = data["t2m"][:]-273.
#     t2m_area = data_values[:,21:27,17:31].mean(axis=(1,2))
#     if isLeap(yr):
#         t2m[i] = np.concatenate((t2m_area[:59],t2m_area[60:]))
#     else:
#         t2m[i] = t2m_area
        
#     i += 1
    
# data2022_1 = netCDF4.Dataset("/media/ziga/DATADRIVE1/podnebne_spremembe/slovenija/t2m_2022_1-9.nc")
# data2022_2 = netCDF4.Dataset("/media/ziga/DATADRIVE1/podnebne_spremembe/slovenija/t2m_2022_10.nc")
# data_values_1 = data2022_1["t2m"][:]-273.
# data_values_2 = data2022_2["t2m"][:]-273.
# t2m_2022_1 = data_values_1[:,21:27,17:31].mean(axis=(1,2))
# t2m_2022_2 = data_values_2[:,21:27,17:31].mean(axis=(1,2))
# t2m_2022 = np.concatenate((t2m_2022_1,t2m_2022_2))

# data2022 = netCDF4.Dataset("/media/ziga/DATADRIVE1/podnebne_spremembe/slovenija/t2m_2022.nc")
# data_values = data2022["t2m"][:]-273.
# t2m_2022 = data_values[:,21:27,17:31].mean(axis=(1,2))

# data2021 = netCDF4.Dataset("/media/ziga/DATADRIVE1/podnebne_spremembe/slovenija/t2m_2021.nc")
# data_values = data2021["t2m"][:]-273.
# t2m_2021 = data_values[:,21:27,17:31].mean(axis=(1,2))
 

# t2m_61_90 = np.zeros((30,365))
# t2m_91_20 = np.zeros((30,365))
# t2m_10_21 = np.zeros((12,365))
# t2m_50_22 = np.zeros((73,365))

# # READ DATA
# i = 0
# for yr in range(1961,1991):
#     data = netCDF4.Dataset("/media/ziga/DATADRIVE1/podnebne_spremembe/slovenija/t2m_"+str(yr)+".nc")
#     data_values = data["t2m"][:]-273.
#     t2m_area = data_values[:,21:27,17:31].mean(axis=(1,2))
#     if isLeap(yr):
#         t2m_61_90[i] = np.concatenate((t2m_area[:59],t2m_area[60:]))
#     else:
#         t2m_61_90[i] = t2m_area
        
#     i += 1

# t2m_61_90_mean = np.mean(t2m_61_90[:i,:],axis=0)


# # READ DATA
# i = 0
# for yr in range(1991,2021):
#     data = netCDF4.Dataset("/media/ziga/DATADRIVE1/podnebne_spremembe/slovenija/t2m_"+str(yr)+".nc")
#     data_values = data["t2m"][:]-273.
#     t2m_area = data_values[:,21:27,17:31].mean(axis=(1,2))
#     if isLeap(yr):
#         t2m_91_20[i] = np.concatenate((t2m_area[:59],t2m_area[60:]))
#     else:
#         t2m_91_20[i] = t2m_area
        
#     i += 1

# t2m_91_20_mean = np.mean(t2m_91_20[:i,:],axis=0)
    
# # READ DATA
# i = 0
# for yr in range(2010,2022):
#     data = netCDF4.Dataset("/media/ziga/DATADRIVE1/podnebne_spremembe/slovenija/t2m_"+str(yr)+".nc")
#     data_values = data["t2m"][:]-273.
#     t2m_area = data_values[:,21:27,17:31].mean(axis=(1,2))
#     if isLeap(yr):
#         t2m_10_21[i] = np.concatenate((t2m_area[:59],t2m_area[60:]))
#     else:
#         t2m_10_21[i] = t2m_area
        
#     i += 1
    
# t2m_10_21_mean = np.mean(t2m_10_21[:i,:],axis=0) 
   

# i = 0
# for yr in range(1950,2023):
#     data = netCDF4.Dataset("/media/ziga/DATADRIVE1/podnebne_spremembe/slovenija/t2m_"+str(yr)+".nc")
#     data_values = data["t2m"][:]-273.
#     t2m_area = data_values[:,21:27,17:31].mean(axis=(1,2))
#     if isLeap(yr):
#         t2m_50_22[i] = np.concatenate((t2m_area[:59],t2m_area[60:]))
#     else:
#         t2m_50_22[i] = t2m_area
        
#     i += 1
    
# t2m_50_22_mean = np.mean(t2m_50_22[:i,:],axis=1) 
   
# #%% running means
# T=7
# t2m_mean = np.mean(t2m[:i,:],axis=0)
# t2m_95 = np.percentile(t2m[:i,:],95,axis=0)
# t2m_05 = np.percentile(t2m[:i,:],5,axis=0)

# t2m_running_mean = np.convolve(np.concatenate((t2m_mean[-3:],t2m_mean,t2m_mean[:3])), np.ones(T)/T, mode='valid')
# t2m_running_95 = np.convolve(np.concatenate((t2m_95[-3:],t2m_95,t2m_95[:3])), np.ones(T)/T, mode='valid')
# t2m_running_05 = np.convolve(np.concatenate((t2m_05[-3:],t2m_05,t2m_05[:3])), np.ones(T)/T, mode='valid')

# t2m_2022_running_mean = np.convolve(np.concatenate((t2m_2021[-3:],t2m_2022)), np.ones(T)/T, mode='valid')





# #%%
# fig = plt.figure(4,figsize=(14,6))
# ax = fig.add_subplot(111)
# # ax.plot(dayofyr,t2m_running_mean,"k-",label="$\overline{T}$ (1981-2010)")
# #ax.fill_between(range(365),t2m_running_95,t2m_running_05,facecolor="k",alpha=0.3,label=r"5 - 95 perc")
# t2m_61_90_max = t2m_50_22[11:40,:].max(axis=0)
# ax.plot(dayofyr,t2m_61_90_max,"k-",label="max (1961-1990)")

# ax.plot(dayofyr[:len(t2m_2022)],t2m_2022,"r-",label="T (2022)")

# condition = t2m_2022>t2m_61_90_max
# ax.plot(dayofyr[:len(t2m_2022)][condition],np.zeros(365)[condition]-5,"ro",label="T(2022) > max(1961-1990)")


# ax.set_ylabel(r"$T$",fontsize=14)
# ax.set_xlabel("Datum")
# ax.set_title("Primerjava maksimumov 1961-1990 in leta 2022")

# # Major ticks
# ax.set_xticks([0,31,59,90,120,151,182,212,243,277,304,334])
# ax.set_xticklabels([])
# ax.tick_params(axis='x', which="major", length=5)

# # Minor ticks
# ax.set_xticks([15,45,74,105,135,166,197,227,258,292,319,349],minor=True)
# ax.set_xticklabels(["januar", "februar", "marec", "april","maj",\
#                     "junij", "julij", "avgust", "september",\
#                         "oktober","november", "december"],rotation=30,fontsize=13,minor=True)
# ax.tick_params(axis='x', which="minor",length=0)
# ax.legend(fontsize=14)
# ax.grid()
# plt.tight_layout()
# fig.savefig("t2m_2022_3.png")


# #%% running means
# T=31
# S = int((T-1)/2)

# # t2m_95 = np.percentile(t2m[:i,:],95,axis=0)
# # t2m_05 = np.percentile(t2m[:i,:],5,axis=0)

# t2m_61_90_running_mean = np.convolve(np.concatenate((t2m_61_90_mean[-S:],t2m_61_90_mean,t2m_61_90_mean[:S])), np.ones(T)/T, mode='valid')
# t2m_91_20_running_mean = np.convolve(np.concatenate((t2m_91_20_mean[-S:],t2m_91_20_mean,t2m_91_20_mean[:S])), np.ones(T)/T, mode='valid')
# t2m_10_21_running_mean = np.convolve(np.concatenate((t2m_10_21_mean[-S:],t2m_10_21_mean,t2m_10_21_mean[:S])), np.ones(T)/T, mode='valid')
# # t2m_running_95 = np.convolve(np.concatenate((t2m_95[-3:],t2m_95,t2m_95[:3])), np.ones(T)/T, mode='valid')
# # t2m_running_05 = np.convolve(np.concatenate((t2m_05[-3:],t2m_05,t2m_05[:3])), np.ones(T)/T, mode='valid')

# blah=np.zeros(365)
# blah[:]=20.04545936379381

# fig = plt.figure(3,figsize=(14,6))
# ax = fig.add_subplot(111)
# ax.plot(dayofyr,t2m_61_90_running_mean,"k-",label="$\overline{T}$ (1961-1990)")
# # ax.plot(dayofyr,t2m_91_20_running_mean,"r-",label="$\overline{T}$ (1991-2020)")
# ax.plot(dayofyr,t2m_10_21_running_mean,color="red",label="$\overline{T}$ (2010-2021)")
# ax.plot(dayofyr,t2m_10_21_running_mean+2.7,color="darkred",label="$\overline{T}$ (naivna\nekstrapolacija +2.7°C 2071-2100)")

# ax.fill_between(dayofyr, t2m_10_21_running_mean, blah, t2m_10_21_running_mean>blah,
#                   color='red', alpha=.4)
# ax.fill_between(dayofyr, t2m_10_21_running_mean+2.7,blah , t2m_10_21_running_mean+2.7>blah,
#                   color='darkred', alpha=.4)

# ax.set_ylabel(r"$T$",fontsize=14)
# ax.set_xlabel("Datum")
# ax.set_title("Primerjava dolgoletnih povprečij (ECMWF ERA5)")

# # Major ticks
# ax.set_xticks([0,31,59,90,120,151,182,212,243,277,304,334])
# ax.set_xticklabels([])
# ax.tick_params(axis='x', which="major", length=5)

# # Minor ticks
# ax.set_xticks([15,45,74,105,135,166,197,227,258,292,319,349],minor=True)
# ax.set_xticklabels(["januar", "februar", "marec", "april","maj",\
#                     "junij", "julij", "avgust", "september",\
#                         "oktober","november", "december"],rotation=30,fontsize=13,minor=True)
# ax.tick_params(axis='x', which="minor",length=0)
# ax.legend(fontsize=14)
# ax.grid()
# plt.tight_layout()
# fig.savefig("blah3.png")
