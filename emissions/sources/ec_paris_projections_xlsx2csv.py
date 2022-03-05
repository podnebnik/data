#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 02:45:52 2021

@author: ziga
"""

import pandas as pd
import numpy as np

years = np.arange(2020,2031)

df = pd.read_excel("ProjekcijeGHG_Slovenija.xlsx")
matrix = df.as_matrix()
bau = matrix[:11,3]
nepn = matrix[:11,5]
ec = matrix[:11,7]
paris20 = matrix[:11,9]
paris15 = matrix[:11,11]

df = pd.DataFrame({'year': years.astype(int),
                   'bau': bau,
                   'nepn':nepn,
                   'ec':ec,
                   'paris20':paris20,
                   'paris15':paris15})
df.to_csv("../data/emissions.projections.ec_paris.csv",index=False)