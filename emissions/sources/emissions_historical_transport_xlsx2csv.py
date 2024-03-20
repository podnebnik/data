#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 01:06:08 2021

@author: ziga
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os,glob

# global warming potential of gases
gwp = {"co2": 1,
       "ch4": 25,
       "n2o": 298,
       "nox": 0.,
       "co": 1.9,
       "nmvoc": 3.4,
       "so2": 0.,
       "cfc_hfc" : 1.}




year_start = 1986
year_current = datetime.today().year
year_end = year_current - 2

years = np.arange(year_start,year_end+1)
n = years.shape[0]

transport__total = np.zeros(n)
transport__domestic_aviation = np.zeros(n)
transport__road_transporation = np.zeros(n)
transport__road_transporation__cars = np.zeros(n)
transport__road_transporation__light_duty_trucks = np.zeros(n)
transport__road_transporation__heavy_duty_trucks = np.zeros(n)
transport__road_transporation__buses = np.zeros(n)
# transport__road_transporation__heavy_duty_trucks_buses = np.zeros(n)
transport__road_transporation__motorcycles = np.zeros(n)
transport__road_transporation__other = np.zeros(n)
transport__railways = np.zeros(n)
transport__domestic_navigation = np.zeros(n)
transport__other_transportation = np.zeros(n)
transport__international_aviation = np.zeros(n)
transport__international_navigation = np.zeros(n)

def co2equiv(arr,gwp):
    return arr[0]*gwp["co2"] + arr[1]*gwp["ch4"] + arr[2]*gwp["n2o"]

def check_matrix(arr):
    if all([type(x)==str for x in arr]):
        return np.zeros(3)
    else:
        return arr


def check_val(x):
    if type(x)==str:
        return 0
    else:
        return x

i = 0
y = year_start
while y <= year_end:
    print(y)
    # manually loop through sheets
    
    # file_name = glob.glob("SVN_2021__14032021_193543/SVN_{0:04d}_{1:04d}_*.xlsx".format(year_current,y))[0]
    file_name = glob.glob("SVN_20230315/SVN_{0:04d}_{1:04d}_*.xlsx".format(year_current,y))[0]
    
    # Sectoral report for energy, sheet 1 + sheet2
    df = pd.read_excel(file_name,sheet_name="Table1.A(a)s3")
    matrix = df.to_numpy()[7:-2,-3:]
    
    transport__total[i] = co2equiv(matrix[0],gwp)
    transport__domestic_aviation[i] = co2equiv(matrix[6],gwp)
    transport__road_transporation[i] = co2equiv(matrix[10],gwp)
    transport__road_transporation__cars[i] = co2equiv(matrix[18],gwp)
    transport__road_transporation__light_duty_trucks[i] = co2equiv(matrix[26],gwp)
    # transport__road_transporation__heavy_duty_trucks_buses[i] = co2equiv(matrix[34],gwp)
    transport__road_transporation__motorcycles[i] = co2equiv(matrix[42],gwp)
    transport__road_transporation__other[i] = co2equiv(check_matrix(matrix[51]),gwp)
    transport__railways[i] = co2equiv(matrix[52],gwp)
    transport__domestic_navigation[i] = co2equiv(check_matrix(matrix[58]),gwp)
    transport__other_transportation[i] = co2equiv(check_matrix(matrix[66]),gwp)
    
                      
    # add international aviation and navigation
    df = pd.read_excel(file_name,sheet_name="Summary2")
    matrix = df.to_numpy()
    
    transport__international_aviation[i] = matrix[56,-1]
    transport__international_navigation[i] = check_val(matrix[57,-1])
    
    
    # Division between  heavy duty trucks and buses
    file_name = glob.glob("Emisije TGP iz cestnega prometa za Podnebnik razdelitev na potniški in težki tovorni promet.xlsx")[0]
    df = pd.read_excel(file_name)
    matrix = df.to_numpy()[2:,3:]
    transport__road_transporation__heavy_duty_trucks[i] = co2equiv(matrix[::2,i],gwp)
    transport__road_transporation__buses[i] =  co2equiv(matrix[1::2,i],gwp)   
    
    y += 1
    i += 1

#%%
df = pd.DataFrame({
        'year': years.astype(int),
        'total':     transport__total,
        'road_transporation.total': transport__road_transporation,
        'road_transporation.cars':    transport__road_transporation__cars,
        "road_transporation.light_duty_trucks":    transport__road_transporation__light_duty_trucks,
        'road_transporation.heavy_duty_trucks':     transport__road_transporation__heavy_duty_trucks,
        'road_transporation.buses':     transport__road_transporation__buses,
        'road_transporation.motorcycles': transport__road_transporation__motorcycles,
        'road_transporation.other': transport__road_transporation__other,
        'railways': transport__railways,
        'domestic_aviation': transport__domestic_aviation,
        'domestic_navigation': transport__domestic_navigation,
        'other_transportation': transport__other_transportation,
        'international_aviation': transport__international_aviation,
        'international_navigation': transport__international_navigation
        })
df.to_csv("../data/emissions.historical.energy.transport.csv",index=False,float_format='%.2f')
