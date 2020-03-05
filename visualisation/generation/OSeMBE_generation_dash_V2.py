# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 12:05:23 2020

@author: haukeh
"""

# import tkinter as tk
# from tkinter import filedialog
import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# root = tk.Tk()
# root.withdraw()

# file_path = filedialog.askopenfilename()
df_eg = pd.read_pickle('data\OSeMBE_ProductionByTechnologyAnnual_DataV3_2020-02-26.pkl')
pathways_eg = df_eg.loc[:,'pathway'].unique()
df_eg['region'] = df_eg['info_1'].apply(lambda x: x[:2])
df_eg['tech/reg2'] = df_eg['info_1'].apply(lambda x: x[4:6])
df_eg['unit'] = 'PJ'
regions_eg = np.sort(df_eg.loc[:,'region'].unique())

df_ate = pd.read_pickle('data\OSeMBE_AnnualTechnologyEmission_DataV2_2020-02-14.pkl')
df_c2t = df_ate[df_ate['info_2']=='CO2']
pathways_c2t = df_c2t.loc[:,'pathway'].unique()
df_c2t['region'] = df_c2t['info_1'].apply(lambda x: x[:2])
df_c2t['import/domestic'] = df_c2t['info_1'].apply(lambda x: x[6])
df_c2t['fuel_source'] = df_c2t['info_1'].apply(lambda x: x[2:4]+x[6])
df_c2t = df_c2t[(df_c2t['import/domestic']=='I') | (df_c2t['import/domestic']=='X')]
df_c2t['unit'] = 'kt'
regions_c2t = df_c2t['region'].unique()

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
#%% dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='OSeMBE results'),
    html.H2(children='Power generation'),
    html.Div([        
        html.Label('Electricity generation - Pathway 1'),
        dcc.Dropdown(
            id='pg-pathway-selection-1',
            options = [{'label': i, 'value': i} for i in pathways_eg],
            value = 'B1C0T0E0'
            ),
        html.Label('Electricity generation - Region/Country 1'),
        dcc.Dropdown(
            id='pg-region-country-selection-1',
            options = [{'label': i, 'value': i} for i in regions_eg],
            value = 'AT'
            ),
        dcc.Graph(
            id='Power-generation-1'
            )
        ], style={'width': '49%', 'display': 'inline-block'}
        ),
    html.Div([
        html.Label('Electricity generation - Pathway 2'),
        dcc.Dropdown(
            id='pg-pathway-selection-2',
            options = [{'label': i, 'value': i} for i in pathways_eg],
            value = 'B1C0T0E0'
            ),
        html.Label('Electricity generation - Region/Country 2'),
        dcc.Dropdown(
            id='pg-region-country-selection-2',
            options = [{'label': i, 'value': i} for i in regions_eg],
            value = 'AT'
            ),
        dcc.Graph(
            id='Power-generation-2'
            )
        ],style = {'width': '49%', 'display': 'inline-block', 'float': 'right'}
        ),
    
    html.H2(children='Annual CO2 Emission by Technology'),
    html.Div([
        html.Label('CO2 Emission - Pathway 1'),
        dcc.Dropdown(
            id='c2t-pathway-selection-1',
            options = [{'label': i, 'value': i} for i in pathways_c2t],
            value = 'B1C0T0E0'
            ),
        html.Label('CO2 Emission - Country 1'),
        dcc.Dropdown(
            id='c2t-country-selection-1',
            options = [{'label': i, 'value': i} for i in regions_c2t],
            value = 'AT'
            ),
        dcc.Graph(
            id='c2t-graph-1'
            )
        ], style={'width': '49%', 'display': 'inline-block'}
        ),
    html.Div([
        html.Label('CO2 Emission - Pathway 2'),
        dcc.Dropdown(
            id='c2t-pathway-selection-2',
            options = [{'label': i, 'value': i} for i in pathways_c2t],
            value = 'B1C0T0E0'
            ),
        html.Label('CO2 Emission - Country 2'),
        dcc.Dropdown(
            id='c2t-country-selection-2',
            options = [{'label': i, 'value': i} for i in regions_c2t],
            value = 'AT'
            ),
        dcc.Graph(
            id='c2t-graph-2'
            )
        ], style={'width': '49%', 'display': 'inline-block'}
        )
    ])
# app.css.append_css({
#     'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
# })

@app.callback(
    Output('Power-generation-1', 'figure'),
    [Input('pg-pathway-selection-1', 'value'),
     Input('pg-region-country-selection-1', 'value')])

#%% Function for updating graph
def update_graph_1(selected_pathway, selected_region):
    # selected_pathway = 'B1C0T0E0'
    # selected_region = 'AT'
    countr_el1 = selected_region + 'E1'
    countr_el2 = selected_region + 'E2'
    filtered_df = df_eg[(df_eg['pathway'] == selected_pathway) & ((df_eg['region'] == selected_region)|(df_eg['tech/reg2'] == selected_region)) & ((df_eg['info_2']==countr_el1)|(df_eg['info_2']==countr_el2))]
    filtered_df['tech'] = filtered_df['info_1'].apply(lambda x: x[4:6])
    filtered_df = filtered_df[filtered_df['tech']!= '00']
    # filtered_df['techspec'] = filtered_df['info_1'].apply(lambda x: x[2:])
    filtered_df['production'] = filtered_df.groupby(['info_1','year'])['value'].transform('sum')
    filtered_df = filtered_df[filtered_df['info_2']==countr_el2]
    filtered_df_p = filtered_df.pivot(index='year', columns='info_1',  values='production')
    years = filtered_df['year'].unique()
    traces = []
    fuel_short = pd.DataFrame({'fuel_name':['WI','HY','BF','CO','BM','WS','HF','NU','NG','OC','OI','GO','SO','EL'],'fuel_abr':['wind','hydro','biofuel','coal','biomass','waste','oil','nuclear','gas','ocean','oil','geo','solar','imports']}, columns = ['fuel_name','fuel_abr'])
    #%% Facts dict
    info_dict = {}
    info_dict['Filename'] = ['{}_OSeMBE_plot_generation' .format(pd.to_datetime('today').strftime("%Y-%m-%d"))]
    info_dict['Unit'] = filtered_df.loc[:,'unit'].unique()
    info_dict['Pathway'] = filtered_df.loc[:,'pathway'].unique()
    info_dict['Year'] = filtered_df.loc[:,'year'].unique().tolist()
    info_dict['Y-Axis'] = ['{}'.format(*info_dict['Unit'])]
    techs = np.sort(filtered_df['info_1'].unique())
    for i in techs:
        fuel = i[2:4]
        temp = fuel_short.loc[fuel_short['fuel_name']==fuel,'fuel_abr']
        fuel_code = temp.iloc[0]
        traces.append(dict(
            x = years,
            y = filtered_df_p.loc[:,i],
            hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5,
                      color=colours[fuel_code]),
            stackgroup='one',
            name=i
            ))
    return {
        'data': traces,
        'layout': dict(
            title='Electricity generation in {} in scenario {}'.format(selected_region,selected_pathway),
            yaxis=dict(title=''.join(info_dict['Y-Axis'])),
            font=dict(family='Aleo'),
            )
        }

# @app.callback(
#      Output('Power-generation-2', 'figure'),
#     [Input('pg-pathway-selection-2', 'value'),
#      Input('pg-region-country-selection-2', 'value')])
# #%% Function for updating graph
# def update_graph_2(selected_pathway, selected_region):
#     filtered_df = df_eg[(df_eg['pathway'] == selected_pathway) & (df_eg['region'] == selected_region)]
#     filtered_df_p = filtered_df.pivot(index='year', columns='indicator',  values='value')
#     years = filtered_df['year'].unique()
#     traces = []
#     fuel_short = pd.DataFrame({'fuel_name':['Wind','Hydro','Biofuel liquid','Coal','Biomass solid','Waste non renewable','Oil','Nuclear','Natural gas / non renew.','Ocean','Geothermal','Solar'],'fuel_abr':['wind','hydro','biofuel','coal','biomass','waste','oil','nuclear','gas','ocean','geo','solar']}, columns = ['fuel_name','fuel_abr'])
#     #%% Facts dict
#     info_dict = {}
#     info_dict['Filename'] = ['{}_OSeMBE_plot_generation' .format(pd.to_datetime('today').strftime("%Y-%m-%d"))]
#     info_dict['Unit'] = filtered_df.loc[:,'unit'].unique()
#     info_dict['Pathway'] = filtered_df.loc[:,'pathway'].unique()
#     info_dict['Year'] = filtered_df.loc[:,'year'].unique().tolist()
#     info_dict['Y-Axis'] = ['{}'.format(*info_dict['Unit'])]
#     fuels = np.sort(filtered_df['indicator'].unique())
#     for i in fuels:
#         temp = fuel_short.loc[fuel_short['fuel_name']==i,'fuel_abr']
#         fuel_code = temp.iloc[0]
#         traces.append(dict(
#             x = years,
#             y = filtered_df_p.loc[:,i],
#             hoverinfo='x+y',
#             mode='lines',
#             line=dict(width=0.5,
#                       color=colours[fuel_code]),
#             stackgroup='one',
#             name=i
#             ))
#     return {
#         'data': traces,
#         'layout': dict(
#             title='Electricity generation in {} in scenario {}'.format(selected_region,selected_pathway),
#             yaxis=dict(title=''.join(info_dict['Y-Axis'])),
#             font=dict(family='Aleo'),
#             )
#         }

# @app.callback(
#      Output('c2t-graph-1', 'figure'),
#     [Input('c2t-pathway-selection-1', 'value'),
#      Input('c2t-country-selection-1', 'value')])
# #%% Function for updating graph
# def update_graph_3(selected_pathway, selected_region):
#     # selected_pathway = 'B0C0T0E0'
#     # selected_region = 'DE'
#     filtered_df = df_c2t[(df_c2t['pathway'] == selected_pathway) & (df_c2t['region'] == selected_region)]
#     filtered_df_p = filtered_df.pivot(index='year', columns='fuel_source',  values='value')
#     years = filtered_df['year'].unique()
#     traces = []
#     fuel_short = pd.DataFrame({'fuel_name':['BFI','BFX','BMI','BMX','COI','COX','GOX','HFI','NGI','NGX','OII','OIX','URI','WSX'],'fuel_abr':['biofuel','biofuel','biomass','biomass','coal','coal','geo','oil','gas','gas','oil','oil','nuclear','waste']}, columns = ['fuel_name','fuel_abr'])
#     #%% Facts dict
#     info_dict = {}
#     info_dict['Filename'] = ['{}_OSeMBE_plot_emission' .format(pd.to_datetime('today').strftime("%Y-%m-%d"))]
#     info_dict['Unit'] = filtered_df.loc[:,'unit'].unique()
#     info_dict['Pathway'] = filtered_df.loc[:,'pathway'].unique()
#     info_dict['Year'] = filtered_df.loc[:,'year'].unique().tolist()
#     info_dict['Y-Axis'] = ['{}'.format(*info_dict['Unit'])]
#     fuels = np.sort(filtered_df['fuel_source'].unique())
#     for i in fuels:
#         temp = fuel_short.loc[fuel_short['fuel_name']==i,'fuel_abr']
#         fuel_code = temp.iloc[0]
#         traces.append(dict(
#             x = years,
#             y = filtered_df_p.loc[:,i],
#             hoverinfo='x+y',
#             mode='lines',
#             line=dict(width=0.5,
#                       color=colours[fuel_code]),
#             stackgroup='one',
#             name=i
#             ))
#     return {
#         'data': traces,
#         'layout': dict(
#             title='CO2 Emissions in {} in scenario {}'.format(selected_region,selected_pathway),
#             yaxis=dict(title=''.join(info_dict['Y-Axis'])),
#             font=dict(family='Aleo'),
#             )
#         }

# @app.callback(
#      Output('c2t-graph-2', 'figure'),
#     [Input('c2t-pathway-selection-2', 'value'),
#      Input('c2t-country-selection-2', 'value')])
# #%% Function for updating graph
# def update_graph_4(selected_pathway, selected_region):
#     # selected_pathway = 'B0C0T0E0'
#     # selected_region = 'DE'
#     filtered_df = df_c2t[(df_c2t['pathway'] == selected_pathway) & (df_c2t['region'] == selected_region)]
#     filtered_df_p = filtered_df.pivot(index='year', columns='fuel_source',  values='value')
#     years = filtered_df['year'].unique()
#     traces = []
#     fuel_short = pd.DataFrame({'fuel_name':['BFI','BFX','BMI','BMX','COI','COX','GOX','HFI','NGI','NGX','OII','OIX','URI','WSX'],'fuel_abr':['biofuel','biofuel','biomass','biomass','coal','coal','geo','oil','gas','gas','oil','oil','nuclear','waste']}, columns = ['fuel_name','fuel_abr'])
#     #%% Facts dict
#     info_dict = {}
#     info_dict['Filename'] = ['{}_OSeMBE_plot_emission' .format(pd.to_datetime('today').strftime("%Y-%m-%d"))]
#     info_dict['Unit'] = filtered_df.loc[:,'unit'].unique()
#     info_dict['Pathway'] = filtered_df.loc[:,'pathway'].unique()
#     info_dict['Year'] = filtered_df.loc[:,'year'].unique().tolist()
#     info_dict['Y-Axis'] = ['{}'.format(*info_dict['Unit'])]
#     fuels = np.sort(filtered_df['fuel_source'].unique())
#     for i in fuels:
#         temp = fuel_short.loc[fuel_short['fuel_name']==i,'fuel_abr']
#         fuel_code = temp.iloc[0]
#         traces.append(dict(
#             x = years,
#             y = filtered_df_p.loc[:,i],
#             hoverinfo='x+y',
#             mode='lines',
#             line=dict(width=0.5,
#                       color=colours[fuel_code]),
#             stackgroup='one',
#             name=i
#             ))
#     return {
#         'data': traces,
#         'layout': dict(
#             title='CO2 Emissions in {} in scenario {}'.format(selected_region,selected_pathway),
#             yaxis=dict(title=''.join(info_dict['Y-Axis'])),
#             font=dict(family='Aleo'),
#             )
#         }
if __name__ == '__main__':
    app.run_server(debug=False)