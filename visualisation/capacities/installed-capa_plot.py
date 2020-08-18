# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 16:35:17 2020

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
    df = df[((df['fuel']!='EL')&(df['fuel']!='OI')) & (df['tech_type']!='00')]
    df['unit'] = 'GW'
    return df

def get_facts(df):
    facts_dic = {}
    facts_dic['pathways'] = df.loc[:,'pathway'].unique()
    facts_dic['regions'] = df.loc[:,'region'].unique()
    facts_dic['unit'] = df.loc[:, 'unit'].unique()
    facts_dic['regions'] = np.append(facts_dic['regions'],'EU28')
    return facts_dic
#%%
def create_fig(df_exp, country, path):
    fig = go.Figure()
    # df_exp = expanded_df
    # path = 'B1C0T0E0'
    # country = 'DE'
    years = ['2015','2020','2030','2040','2050']
    df = df_exp[(df_exp['pathway'] == path) 
                &((expanded_df['year']==years[0])
                  |(expanded_df['year']==years[1])
                  |(expanded_df['year']==years[2])
                  |(expanded_df['year']==years[3])
                  |(expanded_df['year']==years[4]))]
    fuel_short = pd.DataFrame({'fuel_name':['WI','HY','BF','CO','BM','WS','HF','NU','NG','OC','OI','GO','SO','EL'],'fuel_abr':['wind','hydro','biofuel','coal','biomass','waste','oil','nuclear','gas','ocean','oil','geo','solar','imports']}, columns = ['fuel_name','fuel_abr'])
    fuel_short = fuel_short.sort_values(['fuel_name'])
    info_dict = {}
    info_dict['Unit'] = df.loc[:,'unit'].unique()
    info_dict['Y-Axis'] = ['{}'.format(*info_dict['Unit'])]
    if country == 'EU28':
        df = df[(df['region']=='AT')
               |(df['region']=='BE')
               |(df['region']=='BG')
               |(df['region']=='CY')
               |(df['region']=='CZ')
               |(df['region']=='DE')
               |(df['region']=='DK')
               |(df['region']=='EE')
               |(df['region']=='ES')
               |(df['region']=='FI')
               |(df['region']=='FR')
               |(df['region']=='GR')
               |(df['region']=='HR')
               |(df['region']=='HU')
               |(df['region']=='IE')
               |(df['region']=='IT')
               |(df['region']=='LT')
               |(df['region']=='LU')
               |(df['region']=='LV')
               |(df['region']=='MT')
               |(df['region']=='NL')
               |(df['region']=='PL')
               |(df['region']=='PT')
               |(df['region']=='RO')
               |(df['region']=='SE')
               |(df['region']=='SI')
               |(df['region']=='SK')
               |(df['region']=='UK')]
        df.drop('info_1',axis=1, inplace=True)
        df.drop('region',axis=1, inplace=True)
        techs = df['tech_spec'].unique()
        df_p = pd.DataFrame(index=years, columns=techs)
        for year in years:
            for tech in techs:
                df_p.loc[year, tech] = df.loc[(df['year']==year)&(df['tech_spec']==tech), 'value'].sum()
        df_by_com = pd.DataFrame()
        coms = fuel_short['fuel_name']
        coms = coms[(coms!='EL')&(coms!='OI')]
        for com in coms:    
            com_selec = df_p.filter(regex="\A"+com, axis=1)
            com_sum = com_selec.sum(axis=1)
            df_by_com[com] = com_sum

        for i in coms:
            # i = 'BF'
            temp = fuel_short.loc[fuel_short['fuel_name']==i,'fuel_abr']
            fuel_code = temp.iloc[0]
            fig.add_trace(go.Bar(
                x = years,
                y = df_by_com.loc[:,i],
                name=fuel_code,
                # hoverinfo='x+y',
                hovertemplate=
                'Capacity: %{y}GW',
                marker_color=colours[fuel_code]
                ))
    else:
        df = df[df['region'] == country]
        df_p = df.pivot(index='year', columns='tech_spec',  values='value')
        techs = list(df_p)
        df_by_com = pd.DataFrame()
        coms = fuel_short['fuel_name']
        coms = coms[(coms!='EL')&(coms!='OI')]
        for com in coms:    
            com_selec = df_p.filter(regex="\A"+com, axis=1)
            com_sum = com_selec.sum(axis=1)
            df_by_com[com] = com_sum
        for i in coms:
            temp = fuel_short.loc[fuel_short['fuel_name']==i,'fuel_abr']
            fuel_code = temp.iloc[0]
            fig.add_trace(go.Bar(
                x = years,
                y = df_by_com.loc[:,i],
                name=fuel_code,
                # hoverinfo='x+y',
                hovertemplate=
                'Capacity: %{y}GW',
                marker_color=colours[fuel_code]
                ))
    fig.update_layout(
        barmode='stack',
        plot_bgcolor='rgba(0,0,0,0)',
        title={
            'text':'Installed power generation capacities in {} in pathway {}'.format(country, path),
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis = {'type': 'category'},
        yaxis = dict(title=''.join(info_dict['Y-Axis'])),
        # font=dict(
        #     family="Century Gothic",
        #     size=16)
        )
    # fig = go.Figure(data=traces, layout=graph_layout )
    return fig, df_p

#%% Dictionary of dictionaries with colour schemes
colour_schemes = dict(
    dES_colours = dict(
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
        imports = 'rgb(232, 133, 2)'),
    TIMES_PanEU_colours = dict(
        coal = 'rgb(0, 0, 0)',
        oil = 'rgb(202, 171, 169)',
        gas = 'rgb(102, 77, 142)',
        nuclear = 'rgb(109, 109, 109)',
        waste = 'rgb(223, 134, 192)',
        biomass = 'rgb(80, 112, 45)',
        biofuel = 'rgb(178, 191, 225)',
        hydro = 'rgb(181, 192, 224)',
        wind = 'rgb(103, 154, 181)',
        solar = 'rgb(210, 136, 63)',
        geo = 'rgb(178, 191, 225)',
        ocean ='rgb(178, 191, 225)',
        imports = 'rgb(232, 133, 2)')
    )
#%% main 
pkl_files = get_file_names()
for file in pkl_files:
    print(file)
# selec_pkl_file = input('This script is to visualise installed cpacities. Please select the .pkl file you want to read in. Take care with the spelling!:')
selec_pkl_file = 'OSeMBE_TotalCapacityAnnual_DataV3R1_2020-07-22.pkl'
raw_df = read_pkl(selec_pkl_file)
expanded_df = expand_df(raw_df)
facts_dic = get_facts(expanded_df)
for path in facts_dic['pathways']:
    print(path)
# selec_path = input('Please select a pathway from the above listed by typing it here:')
selec_path = 'B1C0T0E0'
for region in facts_dic['regions']:
    print(region)
# selec_region = input('Please select a country from the above listed by typing here:')
selec_region = 'UK'
print(list(colour_schemes.keys()))
selec_scheme= input('Please select one of the above listed colour schemes by writing it here and confirming by enter:')
colours = colour_schemes[selec_scheme]
figure, table = create_fig(expanded_df, selec_region, selec_path)
plot(figure)
