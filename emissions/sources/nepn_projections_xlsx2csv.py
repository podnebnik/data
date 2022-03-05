#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 01:06:08 2021

@author: ziga
"""

import pandas as pd
import numpy as np
from scipy.interpolate import interp1d


sp_years = np.arange(2020,2051,5)

df = pd.read_excel("energetska_bilanca_2050_nepn_dps.xlsx",sheet_name="EmisijeTGP")

# current measures
sp_emissions_projections_current = df.as_matrix()[23:44,20:27]

# business as usual
sp_emissions_projections_bau = df.as_matrix()[23:44,60:67]

# additional measures, nuclear
sp_emissions_projections_add_nuc = df.as_matrix()[23:44,28:35]

# additional measures, synthetic
sp_emissions_projections_add_syn = df.as_matrix()[23:44,36:43]

# ambitious additional measures, nuclear
sp_emissions_projections_ambadd_nuc = df.as_matrix()[23:44,44:51]

# ambitious additional measures, synthetic
sp_emissions_projections_ambadd_syn = df.as_matrix()[23:44,52:59]


#%% perform linear interpolation
years = np.arange(2020,2051,1)

fun_emissions_projections_current = interp1d(sp_years,sp_emissions_projections_current,axis=1)
emissions_projections_current = fun_emissions_projections_current(years)

fun_emissions_projections_bau = interp1d(sp_years,sp_emissions_projections_bau,axis=1)
emissions_projections_bau = fun_emissions_projections_bau(years)

fun_emissions_projections_add_nuc = interp1d(sp_years,sp_emissions_projections_add_nuc,axis=1)
emissions_projections_add_nuc = fun_emissions_projections_add_nuc(years)

fun_emissions_projections_add_syn = interp1d(sp_years,sp_emissions_projections_add_syn,axis=1)
emissions_projections_add_syn = fun_emissions_projections_add_syn(years)

fun_emissions_projections_ambadd_nuc = interp1d(sp_years,sp_emissions_projections_ambadd_nuc,axis=1)
emissions_projections_ambadd_nuc = fun_emissions_projections_ambadd_nuc(years)

fun_emissions_projections_ambadd_syn = interp1d(sp_years,sp_emissions_projections_ambadd_syn,axis=1)
emissions_projections_ambadd_syn = fun_emissions_projections_ambadd_syn(years)

#%%
# emission indices from file emissions_total.xlsx
ei= {"energy" : {
            "total" : 0, 
            "fuel_combustion_activities" : {
                    "total" : 1,
                    "energy_industries" : 2,
                    "manufacturing_construction" : 3,
                    "transport" : 4,
                    "other_sectors" : 5,
                    "other" : 6                            
                    },
            "fugitive_emissions_from_fuels" : {
                    "total" : 7,
                    "solid_fuels" : None,
                    "oil_natural_gas_and_energy_production" : None
                    },
            "co2_transport_storage" : None
            },
    "industrial_processes" : {
            "total" : 8,
            "mineral_industry" : None,
            "chemical_industry": None,
            "metal_industry" : None,
            "non_energy_products_from_fuels" : None,
            "electronic_industry" : None,
            "product_usese_as_ODS" : None,
            "other_product_manufacture_use": None,
            "other": None
            },
    "agriculture" : {
            "total": 9,
            "enteric_fermentation": None,
            "manure_management" : None,
            "rice_cultivation" : None,
            "agricultural_soils" : None,
            "prescribed_burning_of_savannas" : None,
            "field_burning_agricultural_residues" : None,
            "liming" : None,
            "urea_application" : None,
            "carbon_containing_fertilizers" : None,
            "other" : None
            },
    "lulucf" : {
            "total" : 10,
            "forest_land" : 11,
            "cropland" : 12,
            "grassland" : 13,
            "wetlands": 14,
            "settlements": 15,
            "other_land": 16,
            "harvested_wood_prducts":17,
            "other" : None
            },
    "waste": {
            "total" : 18,
            "solid_waste_disposal" : None,
            "biological_treatment_solid_waste" : None,
            "incineration_open_burning_waste" : None,
            "waste_water_treatment_discharge" : None,
            "other" : None
            },
    "other" : None,
    "international_bunkers": {
            "total": None,
            "aviation" : None,
            "navigation" : None
            },
    "multilateral_operations" : None,
    "co2_emissions_from_biomass" : None,
    "co2_captured" : None,
    "longerim_storage_waste_disposal" : None,
    "indirect_n20" : None,
    "indirect_co2" : None,
    "total_source" : 19
    }
    
#%% export data    
def export_data(data,years,fnm):    
    df = pd.DataFrame({
            'year': years.astype(int),
            'total_source':                     data[ei["total_source"]],
            'energy_industries':                data[ei["energy"]["fuel_combustion_activities"]["energy_industries"]],
            'manufacturing_construction_fuels': data[ei["energy"]["fuel_combustion_activities"]["manufacturing_construction"]],
            'transport':                        data[ei["energy"]["fuel_combustion_activities"]["transport"]],
            "industrial_processes":             data[ei["industrial_processes"]["total"]],
            'residential_commercial_agricultural_forestry_fishing_fuels':  data[ei["energy"]["fuel_combustion_activities"]["other_sectors"]],
            'agriculture':                      data[ei["agriculture"]["total"]],
            'waste':                            data[ei["waste"]["total"]],
            'others':                           data[ei["energy"]["fuel_combustion_activities"]["other"]] +\
                                                data[ei["energy"]["fugitive_emissions_from_fuels"]["total"]],
            'lulucf':                           data[ei["lulucf"]["total"]]
            })
    df.to_csv(fnm,index=False,float_format='%.2f')
   
    
export_data(emissions_projections_current,years,"../data/emissions.projections.current.csv")
export_data(emissions_projections_bau,years,"../data/emissions.projections.bau.csv")
export_data(emissions_projections_add_nuc,years,"../data/emissions.projections.additional_nuclear.csv")
export_data(emissions_projections_add_syn,years,"../data/emissions.projections.additional_synthetic.csv")
export_data(emissions_projections_ambadd_nuc,years,"../data/emissions.projections.ambitious_additional_nuclear.csv")
export_data(emissions_projections_ambadd_syn,years,"../data/emissions.projections.ambitious_additional_synthetic.csv")