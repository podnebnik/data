import pandas as pd
from datetime import *
import calendar
import numpy as np
from scipy.signal import butter, lfilter, freqz
from scipy import interpolate
import matplotlib.pyplot as plt


def toTimestamp(d):
  return calendar.timegm(d.timetuple())

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

isLeap = lambda x: x % 4 == 0 and (x % 100 != 0 or x % 400 == 0)


#%%
df = pd.read_csv("data/ljubljana_data")
date_strings = df.values[:,2]
# dates_dt = np.array([datetime.strptime(dates[i], "%Y-%m-%d") for i in range(dates.shape[0])])
t_data = df.values[:,3]
snow_data = df.values[:,7]

dates = np.array(date_strings, dtype='datetime64')
months = (dates.astype('datetime64[M]') - dates.astype('datetime64[Y]')).astype(int) + 1
years = dates.astype('datetime64[Y]').astype(int) + 1970

# Define the year (non-leap year)
year = 2023

# Create a range of dates from January 1st to December 31st
start_date = np.datetime64(f'{year}-01-01')
end_date = np.datetime64(f'{year}-12-31')
date_range = np.arange(start_date, end_date + np.timedelta64(1, 'D'))

#%%
# condition for summer months
# condition = (months >= 6) & (months <= 8)

# Use boolean indexing to select the subset of summer dates
# dates_summer = dates[condition]
# tdata_summer = tdata[condition]
# tdata_summer = tdata_summer.astype(float)
# tdata_summer_years = tdata_summer.reshape((76,92)).max(axis=1)

start_year = 1948
end_year = 2023
day_of_year = np.arange(1,366)

tdata_all = np.zeros((end_year-start_year+1,365))
# snowdata_all = np.zeros((end_year-start_year+1,365))

condition = (years==start_year)
t_data_1year = t_data[condition]
snow_data_1year = snow_data[condition]

if isLeap(start_year):
    t_data_1year = np.concatenate((t_data_1year[:59],t_data_1year[60:]))
    # snow_data_1year = np.concatenate((snow_data_1year[:59],snow_data_1year[60:]))
tdata_all[0,:] = t_data_1year

plt.figure(1,figsize=(10,4.5))
plt.plot(day_of_year, t_data_1year, "k-",lw=0.5,alpha=.3)
plt.ylabel("Temperatura [˚C]")
plt.xlabel("Datum")
plt.ylim([-16,31])
tick_dates = date_range[[0,31,59,90,120,151,181,212,243,273,304,334]]
plt.xticks(day_of_year[[0,31,59,90,120,151,181,212,243,273,304,334]], \
           [date.astype(datetime).strftime('%b %d') for date in tick_dates], rotation=45)
plt.title("Povprečna dnevna temperatura - Ljubljana Bežigrad ({0}-{0})".format(start_year))
plt.savefig("plots_slovenia_tmean/plot_{0}.png".format(start_year),dpi=300)

i = 1
for yr in range(start_year+1,end_year+1):
    print(yr)
    condition = (years==yr)
    dates_1year = dates[condition] 
    t_data_1year = t_data[condition]
    snow_data_1year = snow_data[condition]
    if isLeap(yr):
        t_data_1year = np.concatenate((t_data_1year[:59],t_data_1year[60:]))
        # snow_data_1year = np.concatenate((snow_data_1year[:59],snow_data_1year[60:]))
    
    tdata_all[i,:] = t_data_1year
    # snowdata_all[i,:] = snow_data_1year
    
    plt.plot(day_of_year, t_data_1year, "k-",lw=0.5,alpha=.3)
    plt.title("Povprečna dnevna temperatura - Ljubljana Bežigrad ({0}-{1})".format(start_year,yr))
    plt.savefig("plots_slovenia_tmean/plot_{0}.png".format(yr),dpi=300)
    i += 1

plt.plot(day_of_year,np.mean(tdata_all,axis=0),"g-",lw=2,label="Povprečje")
plt.legend(loc=2)
plt.savefig("plots_slovenia_tmean/mean.png",dpi=300)
plt.plot(day_of_year,np.percentile(tdata_all,10,axis=0),"b-",lw=1,label="10. percentil")
plt.plot(day_of_year,np.percentile(tdata_all,90,axis=0),"r-",lw=1,label="90. percentil")
plt.legend(loc=2)
plt.savefig("plots_slovenia_tmean/percentile.png",dpi=300)
plt.plot(day_of_year,np.min(tdata_all,axis=0),"darkblue",lw=1,label="min")
plt.plot(day_of_year,np.max(tdata_all,axis=0),"darkred",lw=1,label="max")
plt.legend(loc=2)
plt.savefig("plots_slovenia_tmean/minmax.png",dpi=300)

#%%
start_year = 1948
end_year = 2023
day_of_year = np.arange(1,366)

tdata_all = np.zeros((end_year-start_year+1,365))
# snowdata_all = np.zeros((end_year-start_year+1,365))

condition = (years==start_year)
t_data_1year = t_data[condition]
snow_data_1year = snow_data[condition]

if isLeap(start_year):
    t_data_1year = np.concatenate((t_data_1year[:59],t_data_1year[60:]))
    # snow_data_1year = np.concatenate((snow_data_1year[:59],snow_data_1year[60:]))
tdata_all[0,:] = t_data_1year



i = 0
for yr in range(start_year,end_year+1):
    print(yr)
    condition = (years==yr)
    dates_1year = dates[condition] 
    t_data_1year = t_data[condition]
    snow_data_1year = snow_data[condition]
    if isLeap(yr):
        t_data_1year = np.concatenate((t_data_1year[:59],t_data_1year[60:]))
        # snow_data_1year = np.concatenate((snow_data_1year[:59],snow_data_1year[60:]))
    
    tdata_all[i,:] = t_data_1year
    # snowdata_all[i,:] = snow_data_1year
    
    plt.figure(1,figsize=(10,4.5))
    plt.ylabel("Temperatura [˚C]")
    plt.xlabel("Datum")
    plt.ylim([-16,31])
    tick_dates = date_range[[0,31,59,90,120,151,181,212,243,273,304,334]]
    plt.xticks(day_of_year[[0,31,59,90,120,151,181,212,243,273,304,334]], \
               [date.astype(datetime).strftime('%b %d') for date in tick_dates], rotation=45)
    plt.title("Povprečna dnevna temperatura - Ljubljana Bežigrad ({0})".format(yr))
    plt.plot(day_of_year, t_data_1year, "k-",lw=0.5,alpha=.7)
    plt.savefig("plots_slovenia_tmean/plotone_{0}.png".format(yr),dpi=300)
    plt.clf()
    i += 1



    
#%%
start_year = 1948
end_year = 2023
day_of_year = np.arange(1,366)

tdata_all = np.zeros((end_year-start_year+1,365))
# snowdata_all = np.zeros((end_year-start_year+1,365))

condition = (years==start_year)
t_data_1year = t_data[condition]
snow_data_1year = snow_data[condition]

if isLeap(start_year):
    t_data_1year = np.concatenate((t_data_1year[:59],t_data_1year[60:]))
    # snow_data_1year = np.concatenate((snow_data_1year[:59],snow_data_1year[60:]))
tdata_all[0,:] = t_data_1year

plt.figure(1,figsize=(10,4.5))
# plt.plot(day_of_year, t_data_1year, "k-",lw=0.5,alpha=.3)
plt.ylabel("Temperatura [˚C]")
plt.xlabel("Datum")
plt.ylim([-16,31])
tick_dates = date_range[[0,31,59,90,120,151,181,212,243,273,304,334]]
plt.xticks(day_of_year[[0,31,59,90,120,151,181,212,243,273,304,334]], \
           [date.astype(datetime).strftime('%b %d') for date in tick_dates], rotation=45)
plt.title("Povprečna dnevna temperatura - Ljubljana Bežigrad ({0}-{0})".format(start_year))
# plt.savefig("plots_slovenia_tmean/plot_{0}.png".format(start_year),dpi=300)

i = 1
for yr in range(start_year+1,end_year+1):
    print(yr)
    condition = (years==yr)
    dates_1year = dates[condition] 
    t_data_1year = t_data[condition]
    snow_data_1year = snow_data[condition]
    if isLeap(yr):
        t_data_1year = np.concatenate((t_data_1year[:59],t_data_1year[60:]))
        # snow_data_1year = np.concatenate((snow_data_1year[:59],snow_data_1year[60:]))
    
    tdata_all[i,:] = t_data_1year
    # snowdata_all[i,:] = snow_data_1year
    if 1951 <= yr <= 1980:
        plt.plot(day_of_year, t_data_1year, "green",lw=0.5,alpha=.5)
        plt.title("Povprečna dnevna temperatura - Ljubljana Bežigrad ({1})".format(start_year,yr))
        plt.savefig("plots_slovenia_tmean/plot_parts_{0}.png".format(yr),dpi=300)
    elif 1991 <= yr <= 2020:
        plt.plot(day_of_year, t_data_1year, "r-",lw=0.5,alpha=0.5)
        plt.title("Povprečna dnevna temperatura - Ljubljana Bežigrad ({1})".format(start_year,yr))
        plt.savefig("plots_slovenia_tmean/plot_parts_{0}.png".format(yr),dpi=300)
    
    i += 1

plt.plot(day_of_year,np.mean(tdata_all[3:33],axis=0),"darkgreen",lw=2,label="Povprečje 1951-1980")
plt.legend(loc=2)
plt.savefig("plots_slovenia_tmean/mean_1951-1980.png",dpi=300)
plt.plot(day_of_year,np.mean(tdata_all[43:73],axis=0),"darkred",lw=2,label="Povprečje 1991-2020")
plt.legend(loc=2)
plt.savefig("plots_slovenia_tmean/mean_1991-2020.png",dpi=300)





# %%

plt.figure(2,figsize=(8,4))
plt.hist(tdata_all[3:33,:].flatten(),np.arange(12,42,0.5),color="green",label="1951-1980",edgecolor="black")
plt.hist(tdata_all[43:73,:].flatten(),np.arange(12,42,0.5),color="red",alpha=0.75,label="1991-2020",edgecolor="black")
plt.xlabel(r"Temperatura [$\degree C$]",fontsize=14)
plt.ylabel("Število dogodkov",fontsize=14)
plt.title("Porazdelitev povprečne dnevne temperature, Ljubljana Bežigrad, JJA")
plt.legend()
plt.savefig("plots_slovenia_tmean/hist_parts.png",dpi=300)





# %%
plt.figure(3,figsize=(8,4))
plt.hist(tdata_summer[:2760],np.arange(12,42,0.5),color="grey",label="1948-1977",edgecolor="black")
plt.hist((tdata_summer[:2760])[tdata_summer[:2760]>35],np.arange(12,42,0.5),color="red",edgecolor="black")
# plt.hist(tdata_summer[4232:],np.arange(12,42,0.5),density=True,color="red",alpha=0.7,label="1993-2023")
plt.xlabel(r"Temperatura [$\degree C$]",fontsize=14)
plt.ylabel("Število dogodkov",fontsize=14)
plt.title("Porazdelitev najvišje dnevne temperature, Ljubljana Bežigrad, JJA")
plt.legend()
plt.savefig("hist3.png",dpi=300)

plt.figure(4,figsize=(8,4))
plt.hist(tdata_summer[4232:],np.arange(12,42,0.5),color="blue",alpha=0.75,label="1994-2023",edgecolor="black")
plt.hist((tdata_summer[4232:])[tdata_summer[4232:]>=35],np.arange(12,42,0.5),color="red",edgecolor="black")
plt.xlabel(r"Temperatura [$\degree C$]",fontsize=14)
plt.ylabel("Število dogodkov",fontsize=14)
plt.title("Porazdelitev najvišje dnevne temperature, Ljubljana Bežigrad, JJA")
plt.legend()
plt.savefig("hist4.png",dpi=300)


# %%

plt.figure(5,figsize=(8,4))
plt.hist(tdata_summer[:2760],np.arange(12,42,0.5),color="grey",label="1948-1977",edgecolor="black")
plt.hist(tdata_summer[4232:],np.arange(12,42,0.5),color="blue",alpha=0.75,label="1994-2023",edgecolor="black")
plt.hist(tdata_summer[4232:]+3,np.arange(12,42,0.5),color="green",alpha=0.75,label="2070-",edgecolor="black")
plt.xlabel(r"Temperatura [$\degree C$]",fontsize=14)
plt.ylabel("Število dogodkov",fontsize=14)
plt.title("Porazdelitev najvišje dnevne temperature, Ljubljana Bežigrad, JJA")
plt.legend()
plt.savefig("hist5.png",dpi=300)


plt.figure(6,figsize=(8,4))
# plt.hist(tdata_summer[:2760],np.arange(12,42,0.5),color="grey",label="1948-1977")
# plt.hist(tdata_summer[4232:],np.arange(12,42,0.5),color="blue",alpha=0.75,label="1994-2023")
plt.hist(tdata_summer[4232:]+3,np.arange(12,42,0.5),color="green",alpha=0.75,label="2070-",edgecolor="black")
plt.hist((tdata_summer[4232:]+3)[tdata_summer[4232:]+3>=35],np.arange(12,42,0.5),color="red",edgecolor="black")
plt.xlabel(r"Temperatura [$\degree C$]",fontsize=14)
plt.ylabel("Število dogodkov",fontsize=14)
plt.title("Porazdelitev najvišje dnevne temperature, Ljubljana Bežigrad, JJA")
plt.legend()
plt.savefig("hist6.png",dpi=300)

# dist_params1 = genextreme.fit(tdata_summer_years[:20])
# out1=plt.hist(tdata_summer_years[:30],np.arange(30,45,0.5),density=True)
# plt.plot(out1[1],genextreme.pdf(out1[1],*dist_params1))

# dist_params2 = genextreme.fit(tdata_summer_years[-20:])
# out2=plt.hist(tdata_summer_years[-30:],np.arange(30,45,0.5),density=True)
# plt.plot(out2[1],genextreme.pdf(out2[1],*dist_params2))

# return_period_years = np.array([10,20,50,100,200,500])
# slh_return_period = []
# for d in return_period_years:
#     ret1 = genextreme.ppf(1.-1./(d),*dist_params1)
#     ret2 = genextreme.ppf(1.-1./(d),*dist_params2)
#     print("Temperature of {0:d}-year event: {1:f}, {2:f}".format(int(d),ret1,ret2))
    # slh_return_period.append(ret)

# tdata_summer_years_months = np.array((tdata_summer_years[:,:30].max(axis=1),\
#                                       tdata_summer_years[:,30:61].max(axis=1),\
#                                       tdata_summer_years[:,61:92].max(axis=1)))

# %%histogram daily maxes

from scipy.stats import genextreme,gumbel_r,weibull_max,weibull_min,genpareto,gengamma,invgauss,invweibull

n1 = 4232 # prvih 30 let podatkov
n2 = 2760 # zadnjih 30 let podatkov

tdata_extremes1 = (tdata_summer[n1:])[tdata_summer[n1:]>30]
tdata_extremes2 = (tdata_summer[:n2])[tdata_summer[:n2]>30]

nn1 = tdata_extremes1.shape[0]
nn2 = tdata_extremes2.shape[0]

dist_params1 = genextreme.fit(tdata_extremes1)
out1=plt.hist(tdata_extremes1,np.arange(30,45,0.5),density=True)
plt.plot(out1[1],genextreme.pdf(out1[1],*dist_params1))

dist_params2 = genextreme.fit(tdata_extremes2)
out2=plt.hist(tdata_extremes2,np.arange(30,45,0.5),density=True)
plt.plot(out2[1],genextreme.pdf(out2[1],*dist_params2))



return_period_years = np.array([10,20,50,100,200,500])
slh_return_period = []
for d in return_period_years:
    ret1 = genextreme.ppf(1.-1./(d),*dist_params1)
    ret2 = genextreme.ppf(1.-1./(d),*dist_params2)
    print("Temperature of {0:d}-year event: {1:f}, {2:f}".format(int(d),ret1,ret2))
    # slh_return_period.append(ret)




# %%
slh = df.values[8559:,1].astype(float)
times_str = df.values[8559:,0] # 8559 is the index of 1.1.1963, 00 time

# date: str-->datetime object
times = np.array([datetime.strptime(times_str[i], "%Y-%m-%d %H:%M:%S") for i in range(len(times_str))])


# interpolate whole dataset to 10 minute intervals
times_val = np.array([toTimestamp(tt) for tt in times])

n = (times[-1]-times[0]).days*24*6 + 6 # six 10-minute intervals within 1 hour

times_dense = np.array([times[0] + i*timedelta(minutes=10) for i in range(n+1)])
times_dense_val = np.array([toTimestamp(tt) for tt in times_dense])

f = interpolate.interp1d(times_val,slh,kind='linear')
slh_dense = f(times_dense_val)

#%%
import matplotlib.dates as mdates
from matplotlib import pyplot as plt

fig,ax = plt.subplots(1,1,figsize=(6.4,7))
# ax.plot(times_dense[-1000:],slh_dense[-1000:])
ax.plot(times_dense[:180],slh_dense[:180],'r-',label="interp 10 min")
ax.plot(times[:30],slh[:30],'k-',label="raw 1h")
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b-%d: %H'))
for label in ax.get_xticklabels(which='major'):
    label.set(rotation=30, horizontalalignment='right')
plt.legend()


#%%
# filter dataset with 10-yr moving window

order = 2
fs = 1./600       # sample rate, Hz; 1 measurement every 10 minutes = 60 seconds
cutoff = 1/(3600*24*365*20) 

# put values in yr 2000 to mean valies

t1 = int(np.where(times_dense==datetime(2000,1,1,0,0))[0])
t2 = int(np.where(times_dense==datetime(2001,1,1,0,0))[0])
# slh_dense[t1:t2+1] = 217.671
slh_dense = np.concatenate((slh_dense[:t1],slh_dense[t2:]))
times_dense = np.concatenate((times_dense[:t1],times_dense[t2:]))

y = butter_lowpass_filter(slh_dense, cutoff, fs, order)
# plot histogram

fig,ax = plt.subplots(1,1,figsize=(6.4,7))
ax.plot(times_dense[::],slh_dense[::])
ax.plot(times_dense[::],y)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b-%d'))
for label in ax.get_xticklabels(which='major'):
    label.set(rotation=30, horizontalalignment='right')

#%% compute variability

#only from time t1 (01-01-2001) to t2 (31-12-2020)  = REFERENCE PERIOD (izhodiscna 0)
t1 = int(np.where(times_dense==datetime(1984,1,1,0,0))[0])
t2 = int(np.where(times_dense==datetime(2021,3,14,0,0))[0])

slh_dense_reference = slh_dense[t1:t2]
slh_mean_reference = y[t1:t2]
times_dense_reference = times_dense[t1:t2]

# remove mean sea_level during the reference period
slh_dense_var = slh_dense_reference - slh_mean_reference

# compute daily maximums of detrended sea level
n_days = int(slh_dense_var.shape[0]/6/24)
slh_dense_var_daily_max = np.zeros(n_days)

j = 0
for i in range(n_days):
    slh_dense_var_daily_max[i] = np.max(slh_dense_var[j:j+24*6])
    j += 24*6

fig,ax = plt.subplots(1,1,figsize=(13,7))
ax.plot(times_dense_reference, slh_dense_reference,"k-",label="data")
ax.plot(times_dense_reference, slh_mean_reference,"r-",label="10-yr low pass running mean")
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b-%d'))
for label in ax.get_xticklabels(which='major'):
    label.set(rotation=30, horizontalalignment='right')
ax.set_ylabel("visina mareograf")
plt.legend()

#%%
fig,ax = plt.subplots(1,1,figsize=(8,7))
ax.hist(slh_dense_var,bins=np.arange(-150,151,5),color="k",density=True,label="all data")
ax.hist(slh_dense_var_daily_max,bins=np.arange(-150,151,5),color="r",density=True, label="daily max")
ax.set_xlabel("odstopanje od povprecne visine gladine")
plt.legend()

#%%
# histogram daily maxes

from scipy.stats import genextreme,gumbel_r,weibull_max,weibull_min

dist_params = genextreme.fit(slh_dense_var_daily_max)
out=plt.hist(slh_dense_var_daily_max,bins=np.arange(-150,151,5),density=True)
plt.plot(out[1],genextreme.pdf(out[1],*dist_params))


return_period_days = [30,182,365,2*365,5*365,10*365,50*365,100*365]
slh_return_period = []
for d in return_period_days:
    ret=genextreme.ppf(1.-1./d,*dist_params)
    print("Sea-level of {0:d}-day event: {1:f}".format(d,ret))
    slh_return_period.append(ret)


# z=0 of lidar data (reference point of geoid) at slh=224 cm
geoid_slh_height =np.zeros((times_dense_reference.shape))+224.
#%%
fig,ax = plt.subplots(1,1,figsize=(13,7))
ax.plot(times_dense_reference, slh_dense_reference,"k-",label="data")
ax.plot(times_dense_reference, slh_mean_reference,"r-",linewidth=3,label="10-yr running mean")
ax.plot(times_dense_reference, geoid_slh_height, color="gray",linewidth=3,label="z=0 of lidar data at slh= 224 cm")
ax.plot(times_dense_reference, slh_mean_reference + slh_return_period[1],"#FFC30F",label="0.5-yr return period")
ax.plot(times_dense_reference, slh_mean_reference + slh_return_period[2],"#FF5733",label="1-yr return period")
ax.plot(times_dense_reference, slh_mean_reference + slh_return_period[3],"#C70039",label="2-yr return period")
ax.plot(times_dense_reference, slh_mean_reference + slh_return_period[4],"#900C3F",label="5-yr return period")
ax.plot(times_dense_reference, slh_mean_reference + slh_return_period[5],"#581845",label="10-yr return period")
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b-%d'))
for label in ax.get_xticklabels(which='major'):
    label.set(rotation=30, horizontalalignment='right')
ax.set_ylabel("sea surface height (mareograph Koper)")
plt.legend()


#%%
df_future = pd.read_csv("SLR.csv")
dates_future_str = df_future.date
dates_future = np.array([datetime.strptime(dates_future_str[i], "%Y-%m-%d") for i in range(len(dates_future_str))])

ssh_historical= df_future.ssh_historical
ssh_rcp45 = df_future.tot_rcp45
ssh_rcp85 = df_future.tot_rcp85

# put historical data to the same reference as measurements: 1991-2005  --> representative of 1. Jan 1999 = 0.7 cm
ssh_historical_mean = ssh_historical[41:56].mean()

ssh_rcp45_merged = np.concatenate((ssh_historical[:56],ssh_rcp45[56:]))
ssh_rcp85_merged = np.concatenate((ssh_historical[:56],ssh_rcp85[56:]))


order = 2
fs = 1./(3600*24*365)       # sample rate, Hz; 1 measurement every 10 minutes = 60 seconds
cutoff = 1/(3600*24*365*20) 

ssh_rcp45_smoothed = butter_lowpass_filter(ssh_rcp45_merged, cutoff, fs, order)
ssh_rcp85_smoothed = butter_lowpass_filter(ssh_rcp85_merged, cutoff, fs, order)

plt.plot(dates_future,ssh_rcp45_merged)
plt.plot(dates_future,ssh_rcp45_smoothed)

plt.plot(dates_future,ssh_rcp85_merged)
plt.plot(dates_future,ssh_rcp85_smoothed)

slh_mean_reference_mean = slh_mean_reference.mean()
offset = ssh_rcp45_smoothed[41]
ssh_rcp45_smoothed = (ssh_rcp45_smoothed - offset)*100 + slh_mean_reference_mean
ssh_rcp85_smoothed = (ssh_rcp85_smoothed - offset)*100 + slh_mean_reference_mean

#%%
fig,ax = plt.subplots(1,1,figsize=(13,7))
ax.plot(times_dense_reference, slh_dense_reference,"k-",label="data")
ax.plot(times_dense_reference, slh_mean_reference,"r-",linewidth=3,label="10-yr running mean")
ax.plot(times_dense_reference, geoid_slh_height, color="gray",linewidth=3,label="z=0 of lidar data at slh= 224 cm")
ax.plot(times_dense_reference, slh_mean_reference + slh_return_period[1],"#FFC30F",label="0.5-yr return period")
ax.plot(times_dense_reference, slh_mean_reference + slh_return_period[2],"#FF5733",label="1-yr return period")
ax.plot(times_dense_reference, slh_mean_reference + slh_return_period[3],"#C70039",label="2-yr return period")
ax.plot(times_dense_reference, slh_mean_reference + slh_return_period[4],"#900C3F",label="5-yr return period")
ax.plot(times_dense_reference, slh_mean_reference + slh_return_period[5],"#581845",label="10-yr return period")
ax.plot(times_dense_reference, slh_mean_reference + slh_return_period[6],"#581845",label="50-yr return period")
ax.plot(dates_future[71:], ssh_rcp45_smoothed[71:], color="blue",linewidth=2,label="RCP4.5 10-yr running mean")
ax.plot(dates_future[71:], ssh_rcp45_smoothed[71:] + slh_return_period[1], color="#FFC30F",label="RCP4.5 0.5-yr return period")
ax.plot(dates_future[71:], ssh_rcp45_smoothed[71:] + slh_return_period[2], color="#FF5733",label="RCP4.5 1-yr return period")
ax.plot(dates_future[71:], ssh_rcp45_smoothed[71:] + slh_return_period[3], color="#C70039",label="RCP4.5 2-yr return period")
ax.plot(dates_future[71:], ssh_rcp45_smoothed[71:] + slh_return_period[4], color="#900C3F",label="RCP4.5 5-yr return period")
ax.plot(dates_future[71:], ssh_rcp45_smoothed[71:] + slh_return_period[5], color="#581845",label="RCP4.5 10-yr return period")
ax.plot(dates_future[71:], ssh_rcp45_smoothed[71:] + slh_return_period[6], color="#581845",label="RCP4.5 50-yr return period")
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b-%d'))
for label in ax.get_xticklabels(which='major'):
    label.set(rotation=30, horizontalalignment='right')
ax.set_ylabel("sea surface height (mareograph Koper)")
plt.legend()



#%%

fig,ax = plt.subplots(1,1,figsize=(13,7))
ax.plot(times_dense_reference, slh_dense_reference,"k-",label="data")
ax.plot(times_dense_reference, slh_mean_reference,"r-",linewidth=3,label="10-yr running mean")
ax.plot(times_dense_reference, geoid_slh_height, color="gray",linewidth=3,label="z=0 of lidar data at slh= 224 cm")
ax.plot(times_dense_reference, slh_mean_reference + slh_return_period[1],"#FFC30F",label="0.5-yr return period")
ax.plot(times_dense_reference, slh_mean_reference + slh_return_period[2],"#FF5733",label="1-yr return period")
ax.plot(times_dense_reference, slh_mean_reference + slh_return_period[3],"#C70039",label="2-yr return period")
ax.plot(times_dense_reference, slh_mean_reference + slh_return_period[4],"#900C3F",label="5-yr return period")
ax.plot(times_dense_reference, slh_mean_reference + slh_return_period[5],"#581845",label="10-yr return period")
ax.plot(dates_future[71:], ssh_rcp85_smoothed[71:], color="blue",linewidth=2,label="RCP8.5 10-yr running mean")
ax.plot(dates_future[71:], ssh_rcp85_smoothed[71:] + slh_return_period[1], color="#FFC30F",label="RCP8.5 0.5-yr return period")
ax.plot(dates_future[71:], ssh_rcp85_smoothed[71:] + slh_return_period[2], color="#FF5733",label="RCP8.5 1-yr return period")
ax.plot(dates_future[71:], ssh_rcp85_smoothed[71:] + slh_return_period[3], color="#C70039",label="RCP8.5 2-yr return period")
ax.plot(dates_future[71:], ssh_rcp85_smoothed[71:] + slh_return_period[4], color="#900C3F",label="RCP8.5 5-yr return period")
ax.plot(dates_future[71:], ssh_rcp85_smoothed[71:] + slh_return_period[5], color="#581845",label="RCP8.5 10-yr return period")
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b-%d'))
for label in ax.get_xticklabels(which='major'):
    label.set(rotation=30, horizontalalignment='right')
ax.set_ylabel("sea surface height (mareograph Koper)")
plt.legend()

#%%
data = {'Dates': dates_future_str[71:], \
        'return_05': ssh_rcp85_smoothed[71:] + slh_return_period[1],\
        'return_1':  ssh_rcp85_smoothed[71:] + slh_return_period[2],\
        'return_2':  ssh_rcp85_smoothed[71:] + slh_return_period[3],\
        'return_5':  ssh_rcp85_smoothed[71:] + slh_return_period[4],\
        'return_10': ssh_rcp85_smoothed[71:] + slh_return_period[5]}
df = pd.DataFrame(data)

df.to_csv('rcp85_return_periods.csv', index=False)


data = {'Dates': dates_future_str[71:], \
        'return_05': ssh_rcp45_smoothed[71:] + slh_return_period[1],\
        'return_1':  ssh_rcp45_smoothed[71:] + slh_return_period[2],\
        'return_2':  ssh_rcp45_smoothed[71:] + slh_return_period[3],\
        'return_5':  ssh_rcp45_smoothed[71:] + slh_return_period[4],\
        'return_10': ssh_rcp45_smoothed[71:] + slh_return_period[5]}
df = pd.DataFrame(data)

df.to_csv('rcp45_return_periods.csv', index=False)











