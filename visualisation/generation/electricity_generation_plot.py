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
#%% functions for returning positives and negatives
def positives(value):
    return max(value, 0)
def negatives(value):
    return min(value, 0)
#%% Function to create dfs with import and export of electricity for selected country
def impex(data, path_names, selected_country):
    # selected_country = 'DE' #for testing
    # data = expanded_df #for testing
    # path_names = path_names #for testing
    df_filtered = data[(data['fuel']=='EL')
                       &((data['region']==selected_country)|(data['tech_type']==selected_country))
                       &(data['tech_type']!='00')]
    countries = []
    countries = list(df_filtered['region'].unique())
    countries.extend(df_filtered['tech_type'].unique())
    countries = list(dict.fromkeys(countries))
    df_filtered = df_filtered[df_filtered['info_2'].str.contains('|'.join(countries))]
    df_filtered = df_filtered[df_filtered['info_2'].str.contains('E1')]
    years = pd.Series(df_filtered['year'].unique())
    paths = pd.Series(df_filtered['pathway'].unique())
    neighbours = []
    for i in countries:
        if i != selected_country:
            neighbours.append(i)
    dict_path = {}
    links = list(df_filtered['info_1'].unique())
    label_imp = []
    label_exp = []
    for n in neighbours:
        label_imp.append('Import from '+n)
        label_exp.append('Export to '+n)
    for j in paths:
        i = 0
        net_imp = pd.DataFrame(index=years)
        for link in links:
            imp = df_filtered[(df_filtered['pathway']==j)
                              &(df_filtered['info_1']==link)
                              &(df_filtered['info_2']==(selected_country+'E1'))]
            imp = imp.set_index(years)
            exp = df_filtered[(df_filtered['pathway']==j)
                              &(df_filtered['info_1']==link)
                              &(df_filtered['info_2']==(neighbours[i]+'E1'))]
            exp = exp.set_index(years) 
            net_imp[link] = imp['value'] - exp['value']
            i += 1
        net_imp_pos = pd.DataFrame(index=years,columns=links)
        net_imp_neg = pd.DataFrame(index=years,columns=links)
        for link in links:
            net_imp_pos[link] = net_imp[link].map(positives)
            net_imp_neg[link] = net_imp[link].map(negatives)
        net_imp_pos.columns = label_imp
        net_imp_neg.columns = label_exp
        dict_path[j] = {}
        dict_path[j]['imports']=net_imp_pos
        dict_path[j]['exports']=net_imp_neg
    path_ind = []
    year_ind = []
    df_exports = pd.DataFrame(columns=label_exp)
    df_imports = pd.DataFrame(columns=label_imp)
    for year in years:
        for j in paths:
            df_exports = df_exports.append(dict_path[j]['exports'].loc[year])
            df_imports = df_imports.append(dict_path[j]['imports'].loc[year])
            path_ind.append(path_names[j])
    df_exports = df_exports.set_index([pd.Index(path_ind, name='paths')],append=True)
    df_imports = df_imports.set_index([pd.Index(path_ind, name='paths')],append=True)
    return df_exports, df_imports
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
path_names = {'B1C0T0E0':'REF','B1C0ToE0':'OBS','B1C0TxE0':'CBS'}
for region in facts_dic['regions']:
    print(region)
# selec_region = input('Please select a country from the above listed by typing here:')
selec_region = 'DE'
print(list(colour_schemes.keys()))
# selec_scheme = input('Please select one of the above listed colour schemes by writing it here and confirming by enter:')
selec_scheme = 'dES_colours' 
colours = colour_schemes[selec_scheme]
