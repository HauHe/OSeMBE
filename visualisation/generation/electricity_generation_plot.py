# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 14:51:38 2020

@author: haukeh
"""

#Import of required packages
import numpy as np
import pandas as pd
import os
import plotly.graph_objs as go
from plotly.offline import plot

#%%
def get_file_names():
    pkl_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith('.pkl'):
                pkl_files.append(file)
    return pkl_files

def read_pkl(pkl_name):
    df = pd.read_pickle(pkl_name)
    return df

def expand_df(df):
    df['region'] = df['info_1'].apply(lambda x: x[:2])
    df['fuel'] = df['info_1'].apply(lambda x: x[2:4])
    df['tech_type'] = df['info_1'].apply(lambda x: x[4:6])
    df['tech_spec'] = df['info_1'].apply(lambda x: x[2:])
    df = df[(df['fuel']!='OI')
            &(df['tech_type']!='00')
            &((df['year']=='2015')|(df['year']=='2020')|(df['year']=='2030')|(df['year']=='2040')|(df['year']=='2050'))]
    df['unit'] = 'PJ'
    return df

def get_facts(df):
    facts_dic = {}
    facts_dic['pathways'] = df.loc[:,'pathway'].unique()
    facts_dic['regions'] = df.loc[:,'region'].unique()
    facts_dic['unit'] = df.loc[:, 'unit'].unique()
    facts_dic['regions'] = np.append(facts_dic['regions'],'EU28')
    return facts_dic
#%% Dictionary of dictionaries with colour schemes
colour_schemes = dict(
    dES_colours = dict(
        Coal = 'rgb(0, 0, 0)',
        Oil = 'rgb(121, 43, 41)',
        Gas = 'rgb(86, 108, 140)',
        Nuclear = 'rgb(186, 28, 175)',
        Waste = 'rgb(138, 171, 71)',
        Biomass = 'rgb(172, 199, 119)',
        Biofuel = 'rgb(79, 98, 40)',
        Hydro = 'rgb(0, 139, 188)',
        Wind = 'rgb(143, 119, 173)',
        Solar = 'rgb(230, 175, 0)',
        Geo = 'rgb(192, 80, 77)',
        Ocean ='rgb(22, 54, 92)',
        Imports = 'rgb(232, 133, 2)'),
    TIMES_PanEU_colours = dict(
        Coal = 'rgb(0, 0, 0)',
        Oil = 'rgb(202, 171, 169)',
        Gas = 'rgb(102, 77, 142)',
        Nuclear = 'rgb(109, 109, 109)',
        Waste = 'rgb(223, 134, 192)',
        Biomass = 'rgb(80, 112, 45)',
        Biofuel = 'rgb(178, 191, 225)',
        Hydro = 'rgb(181, 192, 224)',
        Wind = 'rgb(103, 154, 181)',
        Solar = 'rgb(210, 136, 63)',
        Geo = 'rgb(178, 191, 225)',
        Ocean ='rgb(178, 191, 225)',
        Imports = 'rgb(232, 133, 2)')
    )
#%% Function to create dfs with import and export of electricity for selected country
def impex(data, selected_country):
    selected_country = 'CH' #for testing
    data = expanded_df #for testing
    df_filtered = data[(data['fuel']=='EL')
                       &((data['region']==selected_country)|(data['tech_type']==selected_country))
                       &(data['tech_type']!='00')]
    countries = []
    countries = list(df_filtered['region'].unique())
    countries.extend(df_filtered['tech_type'].unique())
    countries = list(dict.fromkeys(countries))
    df_filtered = df_filtered[df_filtered['info_2'].str.contains('|'.join(countries))]
    df_filtered = df_filtered[df_filtered['info_2'].str.contains('E1')]
    
#%% Function to create figure

#%% main
pkl_files = get_file_names()
for file in pkl_files:
    print(file)
# selec_pkl_file = input('This script is to visualise installed cpacities. Please select the .pkl file you want to read in. Take care with the spelling!:')
selec_pkl_file ='data/OSeMBE_ProductionByTechnologyAnnual_DataV3R1_2020-09-21.pkl'
raw_df = read_pkl(selec_pkl_file)
expanded_df = expand_df(raw_df)
facts_dic = get_facts(expanded_df)
for region in facts_dic['regions']:
    print(region)
# selec_region = input('Please select a country from the above listed by typing here:')
selec_region = 'DE'
print(list(colour_schemes.keys()))
# selec_scheme = input('Please select one of the above listed colour schemes by writing it here and confirming by enter:')
selec_scheme = 'dES_colours' 
colours = colour_schemes[selec_scheme]
