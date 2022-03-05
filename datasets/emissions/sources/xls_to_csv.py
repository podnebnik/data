#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 21:36:15 2021

@author: ziga
"""
import pandas as pd
import numpy as np


df = pd.read_excel("TGP 1986-2019.xlsx", sheet_name = "zgoščen prikaz")
matrix = df.as_matrix()

sectors = matrix[2:,0]
years = matrix[1,1:-1]
values = matrix[2:,1:-1]


df = pd.DataFrame({'year': years.astype(int),
                   'emissions_CO2_equiv.total': values[8,:],
                   'emissions_CO2_equiv.transport':values[0,:],
                   'emissions_CO2_equiv.energy':values[1,:],
                   'emissions_CO2_equiv.industrial':values[2,:],
                   'emissions_CO2_equiv.industrial_fuels':values[3,:],
                   'emissions_CO2_equiv.household_fuels':values[4,:],
                   'emissions_CO2_equiv.agriculture':values[5,:],
                   'emissions_CO2_equiv.waste':values[6,:],
                   'emissions_CO2_equiv.others':values[7,:],})
df.to_csv("emissions_historical.csv",index=False)


#%%
years = np.arange(2020,2031)

df = pd.read_excel("ProjekcijeGHG_Slovenija.xlsx")
matrix = df.as_matrix()
bau = matrix[:11,3]
nepn = matrix[:11,5]
ec = matrix[:11,7]
paris20 = matrix[:11,9]
paris15 = matrix[:11,11]

df = pd.DataFrame({'year': years.astype(int),
                   'emissions_CO2_equiv.bau': bau,
                   'emissions_CO2_equiv.nepn':nepn,
                   'emissions_CO2_equiv.ec':ec,
                   'emissions_CO2_equiv.paris20':paris20,
                   'emissions_CO2_equiv.paris15':paris15})
df.to_csv("emissions_projections.csv",index=False)


#%%
df = pd.read_excel("aviation.xlsx", sheet_name = "OECD.Stat export")
matrix = df.as_matrix()
years = np.arange(1986,2020)
values= matrix[10,6::2]
aviation_residence = np.zeros(34)
aviation_residence[-values.shape[0]:] = values

df = pd.DataFrame({'year': years.astype(int),
                   'emissions_CO2_equiv.aviation_by_residence': aviation_residence})
df.to_csv("emissions_historical_aviation.csv",index=False)


#%%
df = pd.read_excel("TGP 1986-2019.xlsx", sheet_name = "izpis iz poročevalskih tabel")
matrix = df.as_matrix()
sectors = matrix[5:,0]
values = matrix[5:,2:]
years = np.arange(1986,2020)

df = pd.DataFrame({'year': years.astype(int),
                   'emissions_CO2_equiv.energy.total': values[1,:-1],
                   'emissions_CO2_equiv.energy.fuel_combustion.total': values[2,:-1],
                   'emissions_CO2_equiv.energy.fuel_combustion.energy_industries':values[3,:-1],
                   'emissions_CO2_equiv.energy.fuel_combustion.manufactoring_construction':values[4,:-1],
                   'emissions_CO2_equiv.energy.fuel_combustion.transport':values[5,:-1],
                   'emissions_CO2_equiv.energy.fuel_combustion.other_sectors':values[6,:-1],
                   'emissions_CO2_equiv.energy.fuel_combustion.other':values[7,:-1],
                   'emissions_CO2_equiv.energy.fugitive_emissions.total':values[8,:-1],
                   'emissions_CO2_equiv.energy.fugitive_emissions.solid_fuels':values[9,:-1],
                   'emissions_CO2_equiv.energy.fugitive_emissions.oil_gas_other':values[10,:-1]})
df.to_csv("emissions_historical_energy.csv",index=False)

df = pd.DataFrame({'year': years.astype(int),
                   'emissions_CO2_equiv.industrial_processes.total': values[12,:-1],
                   'emissions_CO2_equiv.industrial_processes.mineral_industry': values[13,:-1],
                   'emissions_CO2_equiv.industrial_processes.chemical_industry':values[14,:-1],
                   'emissions_CO2_equiv.industrial_processes.metal_industry':values[15,:-1],
                   'emissions_CO2_equiv.industrial_processes.non_energy_products':values[16,:-1],
                   'emissions_CO2_equiv.industrial_processes.electronic_industry':values[17,:-1],
                   'emissions_CO2_equiv.industrial_processes.product_uses_as_ods':values[18,:-1],
                   'emissions_CO2_equiv.industrial_processes.other_product_manufacture':values[19,:-1]})
df.to_csv("emissions_historical_industrial_processes.csv",index=False)

df = pd.DataFrame({'year': years.astype(int),
                   'emissions_CO2_equiv.agriculture.total': values[21,:-1],
                   'emissions_CO2_equiv.agriculture.enteric_fermentation': values[22,:-1],
                   'emissions_CO2_equiv.agriculture.manure_management':values[23,:-1],
                   'emissions_CO2_equiv.agriculture.agricultural_soils':values[25,:-1],
                   'emissions_CO2_equiv.agriculture.liming':values[28,:-1],
                   'emissions_CO2_equiv.agriculture.urea_application':values[29,:-1],
                   'emissions_CO2_equiv.agriculture.fertilizers':values[30,:-1]})
df.to_csv("emissions_historical_agriculture.csv",index=False)


df = pd.DataFrame({'year': years.astype(int),
                   'emissions_CO2_equiv.lulucf.total': values[32,:-1],
                   'emissions_CO2_equiv.lulucf.forest_land': values[33,:-1],
                   'emissions_CO2_equiv.lulucf.cropland':values[34,:-1],
                   'emissions_CO2_equiv.lulucf.grassland':values[35,:-1],
                   'emissions_CO2_equiv.lulucf.wetlands':values[36,:-1],
                   'emissions_CO2_equiv.lulucf.settlements':values[37,:-1],
                   'emissions_CO2_equiv.lulucf.other_lands':values[38,:-1],
                   'emissions_CO2_equiv.lulucf.harvested_wood':values[39,:-1]})
df.to_csv("emissions_historical_lulucf.csv",index=False)

df = pd.DataFrame({'year': years.astype(int),
                   'emissions_CO2_equiv.waste.total': values[41,:-1],
                   'emissions_CO2_equiv.waste.solid_waste_disposal': values[42,:-1],
                   'emissions_CO2_equiv.waste.biotreatment_solid_waste':values[43,:-1],
                   'emissions_CO2_equiv.waste.incineration':values[44,:-1],
                   'emissions_CO2_equiv.waste.waste_water':values[45,:-1]})
df.to_csv("emissions_historical_waste.csv",index=False)

df = pd.DataFrame({'year': years.astype(int),
                   'emissions_CO2_equiv.international.total': values[49,:-1],
                   'emissions_CO2_equiv.international.aviation': values[50,:-1],
                   'emissions_CO2_equiv.international.navigation': values[51,:-1],
                   })
df.to_csv("emissions_historical_international.csv",index=False)

df = pd.DataFrame({'year': years.astype(int),
                   'emissions_CO2_equiv.biomass.total': values[53,:-1]})
df.to_csv("emissions_historical_biomass.csv",index=False)