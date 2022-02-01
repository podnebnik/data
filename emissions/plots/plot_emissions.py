#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 13:16:35 2021

@author: ziga
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os,glob
import matplotlib.pyplot as plt


# import historical data
df = pd.read_csv("../data/emissions.historical.csv")
data = df.to_numpy()

years = data[:,0]
data = np.nan_to_num(data)
data = data[:,2:-1]
data = data.transpose()

# rearrange data, so intl aviation, navigation and biomass burning come last
data = np.concatenate((data[:7],data[10][np.newaxis,:],data[7:10]),axis=0)

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

# import emissions ec, paris15,paris20
data_projections_ec = pd.read_csv("../data/emissions.projections.ec_paris.csv")


fig,ax = plt.subplots(1,figsize=(22,14))
ax.grid()
ax.set_xlabel("leto",fontsize=18)
ax.set_ylabel(r"emisije [kt ekvivalent CO$_2$]",fontsize=18)
ax.set_xlim([1984,2032])
ax.set_ylim([-1000,26000])
ax.tick_params(axis='both', which='major', labelsize=16)
# ax.set_title("Viri emisij toplogrednih plinov",fontsize=18)

cols = ["blueviolet","black","blue","grey","firebrick","orange","darkkhaki","slategray","navy","aqua","saddlebrown"]
labels = ["Oskrba z energijo","Industrija in gradbeništvo","Promet","Industrijski procesi",\
          "Raba goriv v gospodinjstvih,\nkomercialnih stavbah, kmetijstvu,\ngozdarstvu, ribištvu","Kmetijstvo",\
          "Odpadki","Ostalo","Mednarodni letalski promet","Mednarodni ladijski promet","Biomasa (kurjenje lesa,\npožari)"]
hatches = 8*[None] + 3*['//']   
     
for i in np.arange(0, data_shape[0]):
    ax.bar(years, data[i], bottom=data_stack[i], color=cols[i], label=labels[i],align="edge",hatch=hatches[i])
ax.plot(years+0.5,data[:8].sum(axis=0), lw=5, color="black",label="Skupaj - brez biomase \nin mednarodnega prometa")    

legend=ax.legend(fontsize=18,ncol=2,bbox_to_anchor=(0., -0.1),loc='upper left',title="Zgodovinske vrednosti")
legend.get_title().set_fontsize('18')


# Create the second legend and add the artist manually.

lines = []
lines += ax.plot(data_projections_bau["year"].values[:11]+0.5,data_projections_bau["total_source"].values[:11],\
         lw=4,label="skupaj - scenarij NEPN\n'business as usual'",color="darkviolet")
lines += ax.plot(data_projections_current["year"].values[:11]+0.5,data_projections_current["total_source"].values[:11],\
         lw=4,label="skupaj - scenarij NEPN\nobstojeci ukrepi",color="red")
lines += ax.plot(data_projections_add["year"].values[:11]+0.5,data_projections_add["total_source"].values[:11],\
         lw=4,label="skupaj - scenarij NEPN\ndodatni ukrepi,\nnuklearka",color="darkorange")
lines += ax.plot(data_projections_ambadd["year"].values[:11]+0.5,data_projections_ambadd["total_source"].values[:11],\
         lw=4,label="skupaj - scenarij NEPN\nambiciozni dodatni ukrepi,\nnuklearka",color="gold")
lines += ax.plot(data_projections_ec["year"].values[:11]+0.5,data_projections_ec["ec"].values[:11],\
         lw=4,label="skupaj - scenarij skladen \ns cilji Evropske komisije",color="yellowgreen")
lines += ax.plot(data_projections_ec["year"].values[:11]+0.5,data_projections_ec["paris20"].values[:11],\
         lw=4,label="skupaj - scenarij \nPariski sporazum "+r"$\Delta T=$ 2$^\circ$C"+r"$(SLO: \Delta T=$3.2$^\circ$C)",color="lime")
lines += ax.plot(data_projections_ec["year"].values[:11]+0.5,data_projections_ec["paris15"].values[:11],\
         lw=4,label="skupaj - scenarij \nPariski sporazum "+r"$\Delta T=$1.5$^\circ$C "+r"$(SLO: \Delta T=$2.4$^\circ$C)",color="darkgreen")

from matplotlib.legend import Legend
leg = Legend(ax, lines, \
             ["skupaj - scenarij NEPN 'business as usual'",\
              "skupaj - scenarij NEPN obstoječi ukrepi",\
              "skupaj - scenarij NEPN dodatni ukrepi,\nnuklearka",\
              "skupaj - scenarij NEPN\nambiciozni dodatni ukrepi, nuklearka",\
              "skupaj - cilji Evropske komisije",\
              "skupaj - Pariški sporazum "+r"$\Delta T=$ 2$^\circ$C "+r"$(SLO: \Delta T=$3.2$^\circ$C)",\
              "skupaj - Pariški sporazum "+r"$\Delta T=$1.5$^\circ$C "+r"$(SLO: \Delta T=$2.4$^\circ$C)"], \
              fontsize=18,bbox_to_anchor=(1, -0.1),loc='upper right',title="Projekcije/zaveze")
legend2 = ax.add_artist(leg)
legend2.get_title().set_fontsize('18')

ax.axvspan(0, 2021, alpha=0.1, color='gray')

#plt.legend(ncol=2,fontsize=18,bbox_to_anchor=(1.02, 1), loc='upper left')
fig.tight_layout()
fig.savefig("total_2022.png",dpi=300)


##%% read projections (Aljoša Slameršak)
#df = pd.read_excel("../emission_data/ProjekcijeGHG_Slovenija.xlsx")
#emissions_projection = df.as_matrix()
#bau = emissions_projection[:11,3]
#nepn = emissions_projection[:11,5]
#ec = emissions_projection[:11,7]
#paris20 = emissions_projection[:11,9]
#paris15 = emissions_projection[:11,11]
#years_projection = np.arange(2020,2031)
#
#
#
#
##%%
##%% plot data - negative emissions (historical) aggregate
#
#fig,ax = plt.subplots(1,figsize=(22,11))
#ax.grid()
#ax.set_xlabel("leto",fontsize=18)
#ax.set_ylabel(r"emisije [kt CO$_2$ equiv.]",fontsize=18)
#ax.set_xlim([1984,2033])
#ax.set_ylim([-12000,33000])
#ax.tick_params(axis='both', which='major', labelsize=16)
#
#ax.bar(years,emissions_historical[ei["lulucf"]["total"]],align="edge",label="gozd, travniki, kmet. zemlj.\nmokrišča, naselja,\nlesni proizvodi (LULUCF)",color="darkgreen")
#vals_lulucf_bottom = emissions_historical[ei["lulucf"]["total"]]*(emissions_historical[ei["lulucf"]["total"]]>=0)
#
##plt.bar(years,-values_lulucf[2,:],bottom=values_lulucf[0,:]-values_lulucf[1,:],align="edge",label="kmetijska zemljišča",color="yellow")
##plt.bar(years,-values_lulucf[3,:],bottom=values_lulucf[0,:]-values_lulucf[1,:]-values_lulucf[2,:],align="edge",label="travišča",color="lightgreen")
#
#
#
##%% plot data - positive emissions (historial)
#vals_lulucf_bottom = emissions_historical[ei["lulucf"]["total"]]*(emissions_historical[ei["lulucf"]["total"]]>=0)
#
#plt.bar(years,2/3.*values[0,:],bottom=vals_lulucf_bottom,align="edge",label="transport",color="blue",alpha=0.5)
#plt.bar(years,1/3.*values[0,:],bottom=2./3*values[0,:]+vals_lulucf_bot,align="edge",label="tovorni promet",color="blue")
#plt.bar(years,aviation_emissions,bottom=values[0,:]+vals_lulucf_bot,align="edge",label="letalski promet",color="indigo")
#
#
#plt.bar(years,values[1,:],bottom=values[0,:]+vals_lulucf_bot+aviation_emissions,align="edge",label="energetika",color="gray")
#plt.bar(years,values[2,:],bottom=values[0:2,:].sum(axis=0)+vals_lulucf_bot+aviation_emissions,align="edge",label="industrijski procesi",color="red")
#plt.bar(years,values[3,:],bottom=values[0:3,:].sum(axis=0)+vals_lulucf_bot+aviation_emissions,align="edge",label="goriva v industriji",color="lime")
#plt.bar(years,values[4,:],bottom=values[0:4,:].sum(axis=0)+vals_lulucf_bot+aviation_emissions,align="edge",label="goriva v gospodinjstvih in ostala raba",color="fuchsia")
#plt.bar(years,values[5,:],bottom=values[0:5,:].sum(axis=0)+vals_lulucf_bot+aviation_emissions,align="edge",label="kmetijstvo",color="cyan")
#plt.bar(years,values[6,:],bottom=values[0:6,:].sum(axis=0)+vals_lulucf_bot+aviation_emissions,align="edge",label="odpadki",color="yellow")
#plt.bar(years,values[7,:],bottom=values[0:7,:].sum(axis=0)+vals_lulucf_bot+aviation_emissions,align="edge",label="drugo",color="brown")
#
#
#
#
#
##%% plot net emission total
#plt.plot(years+0.5,values_lulucf[0,:]+values[-1,:]+aviation_emissions,"k-",lw=7,label="neto emisije")
#
#
##%% plot emission goals
#plt.plot(years_proj,bau,"r-",label="business as usual",lw=4)
#plt.plot(years_proj,nepn,"m-",label="NEPN SLO",lw=4)
#plt.plot(years_proj,ec,"k-",label="cilj EU 2030",lw=4)
#plt.plot(years_proj,paris20,"g-",label="cilj PA $\Delta T < 2.0^\circ$C (66%)",lw=4)
#plt.plot(years_proj,paris15,"b-",label="cilj PA $\Delta T < 1.5^\circ$C (66%)",lw=4)
#
#
##%% plot projected emissions
#plt.rcParams['hatch.linewidth'] = 1.5
#plt.rcParams.update({'hatch.color': 'white'})
##
#
#
#plt.bar(years_proj,osebni_promet_proj,align="edge",color="blue",alpha=0.5,hatch="/")
#plt.bar(years_proj,tovorni_promet_proj,bottom=osebni_promet_proj,align="edge",color="blue",hatch="/")
#plt.bar(years_proj,values_proj[1,:],bottom=values_proj[0,:],align="edge",color="gray",hatch="/")
#plt.bar(years_proj,values_proj[2,:],bottom=values_proj[0:2,:].sum(axis=0),align="edge",hatch="/",color="red")
#plt.bar(years_proj,values_proj[3,:],bottom=values_proj[0:3,:].sum(axis=0),align="edge",hatch="/",color="lime")
#plt.bar(years_proj,values_proj[4,:],bottom=values_proj[0:4,:].sum(axis=0),align="edge",hatch="/",color="fuchsia")
#plt.bar(years_proj,values_proj[5,:],bottom=values_proj[0:5,:].sum(axis=0),align="edge",hatch="/",color="cyan")
#plt.bar(years_proj,values_proj[6,:],bottom=values_proj[0:6,:].sum(axis=0),align="edge",hatch="/",color="yellow")
#plt.bar(years_proj,values_proj[7,:],bottom=values_proj[0:7,:].sum(axis=0),align="edge",hatch="/",color="brown")
#
#
#plt.vlines(switch_tes_year,0,23000,color="grey")
#plt.vlines(swtich_tetol_year,0,23000,color="grey")
#plt.text(switch_tes_year,24000,"[ukrep] \nTEŠ 5/6 izklop",fontsize=14,horizontalalignment="center",color="gray")
#plt.text(swtich_tetol_year,24000,"[ukrep] \nTETOL izklop",fontsize=14,horizontalalignment="center",color="gray")
#
#
#plt.bar(years_proj,values_lulucf_proj,color="darkgreen",align="edge",hatch="/")
#plt.vlines(switch_ff_year,0,-6000,color="darkgreen")
#plt.text(switch_ff_year,-10000,"[ukrep] \n pogozdovanje\n 300 km$^2$/leto",fontsize=14,\
#         horizontalalignment="center",color="darkgreen")
#
#plt.vlines(2014,0,-7000,color="darkgreen")
#plt.text(2014,-11000,"žledolom: \n poškodovanih\n 5000 km$^2$ gozda",fontsize=14,\
#         horizontalalignment="center",color="darkgreen")
#
#
#plt.vlines(switch_wah,0,26000,color="blue",alpha=0.5)
#plt.text(switch_wah,27000,"[ukrep] \ndelo od doma 2/5 dni\n tedensko",fontsize=14,horizontalalignment="center",color="blue",alpha=0.5)
#
#plt.vlines(2021,0,20000,color="blue",alpha=0.5)
#plt.text(2021,21000,"[ukrep] \n+5%/leto delež EV",fontsize=14,horizontalalignment="center",color="blue",alpha=0.5)
#
#
##%% plot total projected_emissions
#plt.plot(years_proj+0.5,values_lulucf_proj+values_proj.sum(axis=0),"k-",lw=7)#,label="neto emisije [projekcija]")
#
#
#plt.axvspan(0, 2020, alpha=0.1, color='gray')
#plt.legend(ncol=4,fontsize=14,loc=2)
#
#plt.tight_layout()
#plt.savefig("blah.png",dpi=300)