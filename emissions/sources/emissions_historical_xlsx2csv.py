#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 20:39:49 2021

@author: ziga
"""

import pandas as pd
import numpy as np



df = pd.read_excel("emissions_historical_2023.xlsx",sheet_name="Sheet1")
emissions_historical = df.values[:,1:]

# emission indices from file emissions_total.xlsx
ei= {"total_net" : 0 ,
     "energy" : {
            "total" : 1, 
            "fuel_combustion_activities" : {
                    "total" : 2,
                    "energy_industries" : 3,
                    "manufacturing_construction" : 4,
                    "transport" : 5,
                    "other_sectors" : 6,
                    "other" : 7                            
                    },
            "fugitive_emissions_from_fuels" : {
                    "total" : 8,
                    "solid_fuels" : 9,
                    "oil_natural_gas_and_energy_production" : 10
                    },
            "co2_transport_storage" : 11
            },
    "industrial_processes" : {
            "total" : 12,
            "mineral_industry" : 13,
            "chemical_industry": 14,
            "metal_industry" : 15,
            "non_energy_products_from_fuels" : 16,
            "electronic_industry" : 17,
            "product_usese_as_ODS" : 18,
            "other_product_manufacture_use":19,
            "other": 20
            },
    "agriculture" : {
            "total": 21,
            "enteric_fermentation": 22,
            "manure_management" : 23,
            "rice_cultivation" : 24,
            "agricultural_soils" : 25,
            "prescribed_burning_of_savannas" : 26,
            "field_burning_agricultural_residues" : 27,
            "liming" : 28,
            "urea_application" : 29,
            "carbon_containing_fertilizers" : 30,
            "other" : 31
            },
    "lulucf" : {
            "total" : 32,
            "forest_land" : 33,
            "cropland" : 34,
            "grassland" : 35,
            "wetlands": 36,
            "settlements": 37,
            "other_land": 38,
            "harvested_wood_prducts":39,
            "other" : 40
            },
    "waste": {
            "total" : 41,
            "solid_waste_disposal" : 42,
            "biological_treatment_solid_waste" : 43,
            "incineration_open_burning_waste" : 44,
            "waste_water_treatment_discharge" : 45,
            "other" : 46
            },
    "other" : 47,
    "international_bunkers": {
            "total": 50,
            "aviation" : 51,
            "navigation" : 52
            },
    "multilateral_operations" : 53,
    "co2_emissions_from_biomass" : 54,
    "co2_captured" : 55,
    "longerim_storage_waste_disposal" : 56,
    "indirect_n20" : 57,
    "indirect_co2" : 58,
    "total_source" : 59,
    }
     

years = np.arange(1986,2022)


df = pd.DataFrame({
        'year': years.astype(int),
        'total_source':                     emissions_historical[ei["total_source"]],
        'energy_industries':                emissions_historical[ei["energy"]["fuel_combustion_activities"]["energy_industries"]],
        'manufacturing_construction_fuels': emissions_historical[ei["energy"]["fuel_combustion_activities"]["manufacturing_construction"]],
        'transport':                        emissions_historical[ei["energy"]["fuel_combustion_activities"]["transport"]],
        "industrial_processes":             emissions_historical[ei["industrial_processes"]["total"]],
        'residential_commercial_agricultural_forestry_fishing_fuels':  emissions_historical[ei["energy"]["fuel_combustion_activities"]["other_sectors"]],
        'agriculture':                      emissions_historical[ei["agriculture"]["total"]],
        'waste':                            emissions_historical[ei["waste"]["total"]],
        "international_aviation":           emissions_historical[ei["international_bunkers"]["aviation"]],
        "international_navigation":         emissions_historical[ei["international_bunkers"]["navigation"]],
        'co2_emissions_from_biomass':       emissions_historical[ei["co2_emissions_from_biomass"]],
        'others':                           emissions_historical[ei["energy"]["fuel_combustion_activities"]["other"]] +\
                                            emissions_historical[ei["energy"]["fugitive_emissions_from_fuels"]["total"]],
        'lulucf':                           emissions_historical[ei["lulucf"]["total"]]
        })
df.to_csv("../data/emissions.historical.csv",index=False,float_format='%.2f')
   


df = pd.DataFrame({
        'year': years.astype(int),
        'total':                                                                emissions_historical[ei["energy"]["total"]],
        'fuel_combustion_activities.total':                                     emissions_historical[ei["energy"]["fuel_combustion_activities"]["total"]],
        'fuel_combustion_activities.energy_industries':                         emissions_historical[ei["energy"]["fuel_combustion_activities"]["energy_industries"]],
        'fuel_combustion_activities.manufacturing_construction':                emissions_historical[ei["energy"]["fuel_combustion_activities"]["manufacturing_construction"]],
        'fuel_combustion_activities.transport':                                 emissions_historical[ei["energy"]["fuel_combustion_activities"]["transport"]],
        'fuel_combustion_activities.other_sectors':                             emissions_historical[ei["energy"]["fuel_combustion_activities"]["other_sectors"]],
        'fuel_combustion_activities.other':                                     emissions_historical[ei["energy"]["fuel_combustion_activities"]["other"]],
        'fugitive_emissions_from_fuels.total':                                  emissions_historical[ei["energy"]["fugitive_emissions_from_fuels"]["total"]],
        'fugitive_emissions_from_fuels.solid_fuels':                            emissions_historical[ei["energy"]["fugitive_emissions_from_fuels"]["solid_fuels"]],
        'fugitive_emissions_from_fuels.oil_natural_gas_and_energy_production':  emissions_historical[ei["energy"]["fugitive_emissions_from_fuels"]["oil_natural_gas_and_energy_production"]],
        'co2_transport_storage':                                                emissions_historical[ei["energy"]["co2_transport_storage"]]
        })
df.to_csv("../data/emissions.historical.energy.csv",index=False,float_format='%.2f')
   

df = pd.DataFrame({
        'year': years.astype(int),
        'total':                emissions_historical[ei["industrial_processes"]["total"]],
        'mineral_industry': emissions_historical[ei["industrial_processes"]["mineral_industry"]],
        'chemical_industry':    emissions_historical[ei["industrial_processes"]["chemical_industry"]],
        'metal_industry':     emissions_historical[ei["industrial_processes"]["metal_industry"]],
        'non_energy_products_from_fuels': emissions_historical[ei["industrial_processes"]["non_energy_products_from_fuels"]],
        'electronic_industry': emissions_historical[ei["industrial_processes"]["electronic_industry"]],
        'product_usese_as_ODS': emissions_historical[ei["industrial_processes"]["product_usese_as_ODS"]],
        'other_product_manufacture_use': emissions_historical[ei["industrial_processes"]["other_product_manufacture_use"]],
        'other': emissions_historical[ei["industrial_processes"]["other"]]
        })
df.to_csv("../data/emissions.historical.industrial_processes.csv",index=False,float_format='%.2f')
 

df = pd.DataFrame({
        'year': years.astype(int),
        'total':                emissions_historical[ei["agriculture"]["total"]],
        'enteric_fermentation': emissions_historical[ei["agriculture"]["enteric_fermentation"]],
        'manure_management':    emissions_historical[ei["agriculture"]["manure_management"]],
        'rice_cultivation':     emissions_historical[ei["agriculture"]["rice_cultivation"]],
        'agricultural_soils':     emissions_historical[ei["agriculture"]["agricultural_soils"]],
        'prescribed_burning_of_savannas': emissions_historical[ei["agriculture"]["prescribed_burning_of_savannas"]],
        'field_burning_agricultural_residues': emissions_historical[ei["agriculture"]["field_burning_agricultural_residues"]],
        'liming': emissions_historical[ei["agriculture"]["liming"]],
        'urea_application': emissions_historical[ei["agriculture"]["urea_application"]],
        'carbon_containing_fertilizers': emissions_historical[ei["agriculture"]["carbon_containing_fertilizers"]],
        'other':                emissions_historical[ei["agriculture"]["other"]]
        })
df.to_csv("../data/emissions.historical.agriculture.csv",index=False,float_format='%.2f')


df = pd.DataFrame({
        'year': years.astype(int),
        'total':                emissions_historical[ei["lulucf"]["total"]],
        'forest_land': emissions_historical[ei["lulucf"]["forest_land"]],
        'cropland':    emissions_historical[ei["lulucf"]["cropland"]],
        "grassland":    emissions_historical[ei["lulucf"]["grassland"]],
        'wetlands':     emissions_historical[ei["lulucf"]["wetlands"]],
        'settlements': emissions_historical[ei["lulucf"]["settlements"]],
        'other_land': emissions_historical[ei["lulucf"]["other_land"]],
        'harvested_wood_prducts': emissions_historical[ei["lulucf"]["harvested_wood_prducts"]],
        'other': emissions_historical[ei["lulucf"]["other"]]
        })
df.to_csv("../data/emissions.historical.lulucf.csv",index=False,float_format='%.2f')


df = pd.DataFrame({
        'year': years.astype(int),
        'total':                emissions_historical[ei["waste"]["total"]],
        'solid_waste_disposal': emissions_historical[ei["waste"]["solid_waste_disposal"]],
        'biological_treatment_solid_waste':    emissions_historical[ei["waste"]["biological_treatment_solid_waste"]],
        'incineration_open_burning_waste':    emissions_historical[ei["waste"]["incineration_open_burning_waste"]],
        "waste_water_treatment_discharge":    emissions_historical[ei["waste"]["waste_water_treatment_discharge"]],
        'other':     emissions_historical[ei["waste"]["other"]]
        })
df.to_csv("../data/emissions.historical.waste.csv",index=False,float_format='%.2f')


df = pd.DataFrame({
        'year': years.astype(int),
        'international_bunkers.total':      emissions_historical[ei["international_bunkers"]["total"]],
        'international_bunkers.aviation':   emissions_historical[ei["international_bunkers"]["aviation"]],
        'international_bunkers.navigation': emissions_historical[ei["international_bunkers"]["navigation"]],
        'multilateral_operations':          emissions_historical[ei["multilateral_operations"]],
        'co2_emissions_from_biomass':       emissions_historical[ei["co2_emissions_from_biomass"]],
        'co2_captured':    emissions_historical[ei["co2_captured"]],
        "longerim_storage_waste_disposal":    emissions_historical[ei["longerim_storage_waste_disposal"]],
        "indirect_n20":    emissions_historical[ei["indirect_n20"]],
        "indirect_co2":    emissions_historical[ei["indirect_co2"]]
        })
df.to_csv("../data/emissions.historical.memo_items.csv",index=False,float_format='%.2f')
