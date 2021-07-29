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
 
    data.to_csv("..\data\electricity.installed_capacities.csv",index=False)    
    
    
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
 
    data.to_csv("..\data\electricity.additions_retirements.csv",index=False) 
    
    
    # electricity.emissions
    
    data = pd.read_excel("SI Electricity, Emissions, Capacities, Consumption - Publish.xlsx", sheet_name = "EnergyEmissions", header = 4)
    
    data = data.drop([0])
    
    
    data = data[['Year', 'Total', 'Energetika Ljubljana', 'Energetika Maribor', 'TEB',
        'TEŠ', 'TETOL', 'TET', 'Energetika Celje',
       'Enos', 'M-Energetika', 'Petrol Energetika', 'Other',
       'Total all individual sources', 'Residual', '2030 Target']]
    
    data = data.rename(columns = {
        'Year': 'year',
        'Total': 'total', 
        'Energetika Ljubljana': 'energetika_ljubljana', 
        'Energetika Maribor': 'energetika_maribor', 
        'TEB': 'teb',
       'TEŠ': 'test', 
       'TETOL': 'tetol', 
       'TET': 'tet', 
       'Energetika Celje': 'energetika_celje',
       'Enos': 'enos', 
       'M-Energetika': 'm_energetika', 
       'Petrol Energetika': 'petrol_energetika', 
       'Other': 'other',
       'Total all individual sources': 'total-individual', 
       'Residual': 'residual', 
       '2030 Target': 'target_2030'
        })
 
    data.to_csv("..\data\electricity.emissions.csv",index=False) 
    
    
    # electricity.yearly_production
    
    data = pd.read_excel("Energetska bilanca, STAT.si in Podnebnik.xlsx", sheet_name = "Casovnica", header = 0)
    
    data = data[['Leto', 'Skupaj proizvodnja', 'Proizvodnja na pragu-hidroelektrarne', 'Proizvodnja na pragu-hidroelektrarne-od tega s prečrpavanjem',
       'Proizvodnja na pragu-termoelektrarne', 'Biomasa in bioplin', 'NEK',
       'Proizvodnja na pragu-sončne elektrarne', 'Proizvodnja na pragu-vetrne elektrarne', 'Dogodek Zaprtje TEŠ6', 
       'Dogodek Začetek obratovanja NEK2', 'Dogodek 100% razogljičenje', 'Skupna raba (končna + izgube + črpanje)']]
    
    
    data = data.rename(columns = {
        'Leto': 'year',
        'Skupaj proizvodnja': 'total_production', 
        'Proizvodnja na pragu-hidroelektrarne': 'hydro', 
        'Proizvodnja na pragu-hidroelektrarne-od tega s prečrpavanjem': 'pump', 
        'Proizvodnja na pragu-termoelektrarne': 'thermal',
       'Biomasa in bioplin': 'biomass', 
       'NEK': 'nuclear', 
       'Proizvodnja na pragu-sončne elektrarne': 'solar', 
       'Proizvodnja na pragu-vetrne elektrarne': 'wind',
       'Dogodek Zaprtje TEŠ6': 'event_tes6', 
       'Dogodek Začetek obratovanja NEK2': 'event_NEK2', 
       'Dogodek 100% razogljičenje': 'event_greenenergy',
       'Skupna raba (končna + izgube + črpanje)': 'total_consumption'
        })
 
    data.to_csv("..\data\electricity.production.csv",index=False) 
    
    # TODO
    
    # electricity.thermal_units
    # TODO
    
    # create datapackage YAML
    # TODO
    
    #import frictionless
    
    
    