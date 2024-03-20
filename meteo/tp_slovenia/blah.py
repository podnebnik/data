import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt
from datetime import *

file_t = (pd.read_excel("Ljubljana - Temperatura, padavine 1961-2021.xlsx",sheet_name="Temperatura"))
file_p = (pd.read_excel("Ljubljana - Temperatura, padavine 1961-2021.xlsx",sheet_name="Višina padavin"))

data_t = file_t.values[:,2] 
data_p = file_p.values[:,2]

times = file_t.values[:,1]

#%% povprečna letna temperatura 
t = 0
date0 = datetime(1961,1,1)
date_end = datetime(2021,1,1)

date = date0


data_t_years = []


while t  < :
    
    
    data_t_years.append(data_t_years)
    t += 1




#%%

bins=plt.hist(data_p[:5000],range=[0.1,140],bins=100,fc=(1, 0, 0, 0.3),label="before",density=True)
bins2=plt.hist(data_p[-5000:],range=[0.1,140],bins=100,fc=(0, 0, 1, 0.3),label="now",density=True)
plt.legend()
plt.yscale("log")
plt.xscale("log")
plt.xlim([1,140])
plt.ylabel("verjetnostna gostota")
plt.xlabel("24-urna količina padavin")

#%%

bins=plt.hist(data_t[:5000],range=[-15,35],bins=100,fc=(1, 0, 0, 0.3),label="before",density=True)
bins2=plt.hist(data_t[-5000:],range=[-15,35],bins=100,fc=(0, 0, 1, 0.3),label="now",density=True)
plt.legend()
plt.yscale("log")
# plt.xscale("log")
# plt.xlim([1,140])
plt.ylabel("verjetnostna gostota")
plt.xlabel("24-urna količina padavin")

# times = data_t.values[:,0]

#%% izracun povratnih dob

# interpolate whole dataset to 10 minute intervals
# times_val = np.array([toTimestamp(tt) for tt in times])

# n = (times[-1]-times[0]).days*24*6 + 6 # six 10-minute intervals within 1 hour

# times_dense = np.array([times[0] + i*timedelta(minutes=10) for i in range(n+1)])
# times_dense_val = np.array([toTimestamp(tt) for tt in times_dense])

# slh_dense = np.interp(times_dense_val,times_val,slh)

#%%
import matplotlib.dates as mdates
from matplotlib import pyplot as plt

# fig,ax = plt.subplots(1,1,figsize=(6.4,7))
# ax.plot(times_dense[-1000:],slh_dense[-1000:])
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b-%d'))
# for label in ax.get_xticklabels(which='major'):
#     label.set(rotation=30, horizontalalignment='right')



#%%
# filter dataset with 10-yr moving window

order = 2
fs = 1./600       # sample rate, Hz; 1 measurement every 10 minutes = 60 seconds
cutoff = 1/(3600*24*365*20) 

# put values in yr 2000 to mean valies

t1 = int(np.where(times_dense==datetime(2000,1,1,0,0))[0])
t2 = int(np.where(times_dense==datetime(2000,12,31,23,50))[0])
slh_dense[t1:t2+1] = 217.671

y = butter_lowpass_filter(slh_dense, cutoff, fs, order)
# plot histogram

fig,ax = plt.subplots(1,1,figsize=(6.4,7))
ax.plot(times_dense[::],slh_dense[::])
ax.plot(times_dense[::],y)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b-%d'))
for label in ax.get_xticklabels(which='major'):
    label.set(rotation=30, horizontalalignment='right')

#%% compute variability

#only from time t2 (2001) on

# remove mean sea_level
slh_dense_var = slh_dense[t2+1:-61]-y[t2+1:-61]

# compute daily maximums of detrended sea level
n_days = int(slh_dense_var.shape[0]/6/24)
slh_dense_var_daily_max = np.zeros(n_days)

j = 0
for i in range(n_days):
    slh_dense_var_daily_max[i] = np.max(slh_dense_var[j:j+24*6])
    j += 24*6

#%%
# histogram daily maxes

from scipy.stats import genextreme,gumbel_r,weibull_max,weibull_min

dist_params = genextreme.fit(slh_dense_var_daily_max)
out=plt.hist(slh_dense_var_daily_max,bins=200,density=True)
plt.plot(out[1],genextreme.pdf(out[1],*dist_params))


return_period_days = [30,182,365,730]
for d in return_period_days:
    print("Sea-level of {0:d}-day event: {1:f}".format(d,genextreme.ppf(1.-1./d,*dist_params)))



#%%
# compute daily maximums of detrended sea level
n_years = int(slh_dense_var.shape[0]/6/24/365)
slh_dense_var_yearly_max = np.zeros(n_years)

j = 0
for i in range(n_years):
    slh_dense_var_yearly_max[i] = np.max(slh_dense_var[j:j+24*6*365])
    j += 24*6*365

