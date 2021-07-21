#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 00:30:22 2021

@author: ziga
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# import historical data
df = pd.read_csv("../data/emissions.historical.energy.transport.csv")
data = df.as_matrix()

years = data[:,0]
data = data[:,3:-1]
data = data.transpose()

data_shape = np.shape(data)

def get_cumulated_array(data, **kwargs):
    cum = data.clip(**kwargs)
    cum = np.cumsum(cum, axis=0)
    d = np.zeros(np.shape(data))
    d[1:] = cum[:-1]
    return d  

cumulated_data = get_cumulated_array(data, min=0)
cumulated_data_neg = get_cumulated_array(data, max=0)

# Re-merge negative and positive data.
row_mask = (data<0)
cumulated_data[row_mask] = cumulated_data_neg[row_mask]
data_stack = cumulated_data


# import projections
data_projections_bau = pd.read_csv("../data/emissions.projections.bau.csv")
data_projections_current = pd.read_csv("../data/emissions.projections.current.csv")
data_projections_add = pd.read_csv("../data/emissions.projections.additional_nuclear.csv")
data_projections_ambadd = pd.read_csv("../data/emissions.projections.ambitious_additional_nuclear.csv")


fig,ax = plt.subplots(1,figsize=(22,14))
ax.grid()
ax.set_xlabel("leto",fontsize=18)
ax.set_ylabel(r"emisije [kt ekvivalent CO$_2$]",fontsize=18)
ax.set_xlim([1984,2032])
ax.set_ylim([-1000,8000])
ax.tick_params(axis='both', which='major', labelsize=16)

cols = ["royalblue","blue","darkblue","deepskyblue","lightblue","slategrey","midnightblue","darkturquoise","lightsteelblue","navy","aqua"]
labels = ["avtomobili","lahka tovorna vozila","težka tovoarna vozila in avtobusi","motocikli",\
          "ostala cestna vozila","železniški promet","notranji letalski promet","notranji ladijski promet","ostalo",\
          "mednarodni letalski promet","mednarodni ladijski promet"]
        
for i in np.arange(0, data_shape[0]):
    ax.bar(years, data[i], bottom=data_stack[i], color=cols[i], label=labels[i],align="edge")
ax.plot(years,data[:8].sum(axis=0), lw=5, color="black",label="skupaj")
legend=ax.legend(fontsize=18,ncol=2,bbox_to_anchor=(0.1, -0.1),loc='upper left',title="Zgodovinske vrednosti")
legend.get_title().set_fontsize('18')
    

lines = []
lines += ax.plot(data_projections_bau["year"].values[:11],data_projections_bau["transport"].values[:11],\
         lw=4,label="skupaj - scenarij NEPN\nobstojeci ukrepi",color="darkviolet")
lines += ax.plot(data_projections_current["year"].values[:11],data_projections_current["transport"].values[:11],\
         lw=4,label="skupaj - scenarij NEPN\nobstojeci ukrepi",color="red")
lines += ax.plot(data_projections_add["year"].values[:11],data_projections_add["transport"].values[:11],\
         lw=4,label="skupaj - scenarij NEPN\ndodatni ukrepi",color="darkorange")
lines += ax.plot(data_projections_ambadd["year"].values[:11],data_projections_ambadd["transport"].values[:11],\
         lw=4,label="skupaj - scenarij NEPN\nambiciozni dodatni ukrepi",color="gold")
from matplotlib.legend import Legend
leg = Legend(ax, lines, \
             ["skupaj - scenarij NEPN 'business as usual'",\
              "skupaj - scenarij NEPN obstoječi ukrepi",\
              "skupaj - scenarij NEPN dodatni ukrepi,\nnuklearka",\
              "skupaj - scenarij NEPN\nambiciozni dodatni ukrepi, nuklearka"], \
              fontsize=18,bbox_to_anchor=(0.9, -0.1),loc='upper right',title="Projekcije/zaveze")
legend2 = ax.add_artist(leg)
legend2.get_title().set_fontsize('18')


ax.axvspan(0, 2020, alpha=0.1, color='gray')

#ax.legend(ncol=2,fontsize=18,loc=4)
plt.tight_layout()
plt.savefig("promet.png",dpi=300)
