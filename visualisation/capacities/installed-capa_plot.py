# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 16:35:17 2020

@author: haukeh
"""
#Import of required packages
import numpy as np
import pandas as pd
import os
from dash.dependencies import Input, Output
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
    df = df[((df['fuel']!='EL')&(df['fuel']!='OI')) & (df['tech_type']!='00')]
    df['unit'] = 'GW'
    return df

def get_facts(df):
    facts_dic = {}
    facts_dic['pathways'] = df.loc[:,'pathway'].unique()
    facts_dic['regions'] = df.loc[:,'region'].unique()
    facts_dic['unit'] = df.loc[:, 'unit'].unique()
    return facts_dic
#%%
def create_fig(df_exp, country, path):
    traces = []
    # selected_pathway = 'B1C0T0E0'
    # country = 'DE'
    df = df_exp[(df_exp['pathway'] == path) & (df_exp['region'] == country)]
    df_p = df.pivot(index='year', columns='info_1',  values='value')
    fuel_short = pd.DataFrame({'fuel_name':['WI','HY','BF','CO','BM','WS','HF','NU','NG','OC','OI','GO','SO','EL'],'fuel_abr':['wind','hydro','biofuel','coal','biomass','waste','oil','nuclear','gas','ocean','oil','geo','solar','imports']}, columns = ['fuel_name','fuel_abr'])
    info_dict = {}
    info_dict['Unit'] = df.loc[:,'unit'].unique()
    info_dict['Y-Axis'] = ['{}'.format(*info_dict['Unit'])]
    techs = list(df_p)
    years = df['year'].unique()
    for i in techs:
        fuel = i[2:4]
        temp = fuel_short.loc[fuel_short['fuel_name']==fuel,'fuel_abr']
        fuel_code = temp.iloc[0]
        traces.append(dict(
            x = years,
            y = df_p.loc[:,i],
            # hoverinfo='x+y',
            hovertemplate=
            'Capacity: %{y}GW',
            mode='lines',
            line=dict(width=0.5,
                      color=colours[fuel_code]),
            stackgroup='one',
            name=i,
            showlegend = False
            ))
    graph_layout = go.Layout(
        title='Installed power generation capacities in {} in pathway {}'.format(country, path),
        yaxis = dict(title=''.join(info_dict['Y-Axis'])) )
    fig = go.Figure(data=traces, layout=graph_layout )
    return fig

#%% Dictionary with standard dES colour codes
colours = dict(
    coal = 'rgb(0, 0, 0)',
    oil = 'rgb(121, 43, 41)',
    gas = 'rgb(86, 108, 140)',
    nuclear = 'rgb(186, 28, 175)',
    waste = 'rgb(138, 171, 71)',
    biomass = 'rgb(172, 199, 119)',
    biofuel = 'rgb(79, 98, 40)',
    hydro = 'rgb(0, 139, 188)',
    wind = 'rgb(143, 119, 173)',
    solar = 'rgb(230, 175, 0)',
    geo = 'rgb(192, 80, 77)',
    ocean ='rgb(22, 54, 92)',
    imports = 'rgb(232, 133, 2)')

pkl_files = get_file_names()
for file in pkl_files:
    print(file)
selec_pkl_file = input('This script is to visualise installed cpacities. Please select the .pkl file you want to read in. Take care with the spelling!:')
raw_df = read_pkl(selec_pkl_file)
expanded_df = expand_df(raw_df)
facts_dic = get_facts(expanded_df)
for path in facts_dic['pathways']:
    print(path)
selec_path = input('Please select a pathway from the above listed by typing it here:')
for region in facts_dic['regions']:
    print(region)
selec_region = input('Please select a country from the above listed by typing here:')
figure = create_fig(expanded_df, selec_region, selec_path)
plot(figure)
