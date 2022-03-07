# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 20:32:41 2021

@author: janb
"""

import pandas as pd
import numpy as np


### Transformation of Podnebnik's Electricity source data to .csv


if __name__ == '__main__':
    
    # electricity.installed_sources
    data = pd.read_excel("SI Electricity, Emissions, Capacities, Consumption - Publish.xlsx", sheet_name = "InstalledCapacities", header = 3)

    data = data[['Year', 'Total [MW]', 'Thermal Power', 'Run-of-River hydro power',
       'Mixed hydro power', 'Pumped hydro power', 'Geothermal', 'Wind',
       'Solar thermal', 'Solar photovoltaic', 'Tide, wave, ocean', 'Nuclear',
       'Other fuels n.e.c.', 'Consumption [TWh]']]

                
    data = data.rename(columns = {
        'Year': 'year', 
        'Total [MW]': 'total', 
        'Thermal Power': 'thermal', 
        'Run-of-River hydro power': 'hydro',
        'Mixed hydro power': 'mixed_hydro', 
        'Pumped hydro power': 'pump_hydro', 
        'Geothermal': 'geothermal', 
        'Wind': 'wind',
        'Solar thermal': 'solar_thermal', 
        'Solar photovoltaic': 'solar', 
        'Tide, wave, ocean': 'wave', 
        'Nuclear': 'nuclear',
        'Other fuels n.e.c.': 'other', 
        'Consumption [TWh]': 'consumption'
        })
 
    data.to_csv("../data/electricity.installed_capacities.csv",index=False)    
    
    
    # electricity.additions_retirements
    
    data = pd.read_excel("SI Electricity, Emissions, Capacities, Consumption - Publish.xlsx", sheet_name = "InstalledCapacities", header = 3)
    
    data = data[['Year', 'Wind.1', 'Solar photovoltaic.1', 'Run-of-River hydro power.1',
       'Pumped hydro power.1', 'Nuclear.1', 'Thermal Power.1',
       'Thermal Power Decommissions']]

                
    data = data.rename(columns = {
        'Year': 'year',
        'Wind.1': 'additions_wind', 
        'Solar photovoltaic.1': 'additions_solar', 
        'Run-of-River hydro power.1': 'additions_hydro',
        'Pumped hydro power.1': 'additions_pump_hydro', 
        'Nuclear.1': 'additions_nuclear', 
        'Thermal Power.1': 'additions_thermal',
        'Thermal Power Decommissions': 'retirements_thermal'
        })
 
    data.to_csv("../data/electricity.additions_retirements.csv",index=False) 
    
    
    # electricity.emissions
    
    data = pd.read_excel("SI Electricity, Emissions, Capacities, Consumption - Publish.xlsx", sheet_name = "EnergyEmissions", header = 4)
    
    data = data.drop([0])
    
    
    data = data.rename(columns = {
        'Year': 'year',
        'Total': 'total', 
        'Energetika Ljubljana': 'energetika_ljubljana', 
        'Energetika Maribor': 'energetika_maribor', 
        'TEB': 'teb',
        'TEŠ': 'tes', 
        'TETOL': 'tetol', 
        'TET': 'tet', 
        'Energetika Celje': 'energetika_celje',
        'Enos': 'enos_energetika', 
        'M-Energetika': 'm_energetika', 
        'Petrol Energetika': 'petrol_energetika', 
        'Other': 'other',
        'Total all individual sources': 'total__individual', 
        'Residual': 'total__residual', 
        '2030 Target': 'target_2030'
        })

    data = data[[
        'year', 'total', 'total__individual', 'total__residual', 'target_2030',
        'tes', 'tetol', 'teb', 'tet',
        'energetika_ljubljana', 'energetika_maribor', 'energetika_celje',
        'enos_energetika', 'petrol_energetika', 'm_energetika', 'other']]
    
    data.to_csv("../data/electricity.emissions.csv",index=False) 
    
    
    # electricity.hydro_units
    # TODO
    
    # electricity.thermal_units
    # TODO
    
    # create datapackage YAML
    # TODO
    
    #import frictionless
    
    
    
