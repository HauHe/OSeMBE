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
df_eg = pd.read_pickle('data\OSeMBE_generation_2020-02-05.pkl')
df_ate = pd.read_pickle('data\OSeMBE_AnnualTechnologyEmission_DataV2_2020-02-13.pkl')
df_c2t = df_ate[df_ate['info_2']=='CO2']
pathways_eg = df_eg.loc[:,'pathway'].unique()
regions_eg = np.sort(df_eg.loc[:,'region'].unique())
pathways_c2t = df_c2t.loc[:,'pathway'].unique()
df_c2t['region'] = df_c2t['info_1'].apply(lambda x: x[:2])
df_c2t['fuel'] = df_c2t['info_1'].apply(lambda x: x[2:4])

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
    ocean ='rgb(22, 54, 92)')
#%% dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='OSeMBE results'),
    html.H2(children='Power generation'),
    html.Div([        
        html.Label('Pathway 1'),
        dcc.Dropdown(
            id='pathway-selection-1',
            options = [{'label': i, 'value': i} for i in pathways_eg],
            value = 'B1C0T0E0'
            ),
        html.Label('Region/Country 1'),
        dcc.Dropdown(
            id='region-country-selection-1',
            options = [{'label': i, 'value': i} for i in regions_eg],
            value = 'EU+CH+NO'
            ),
        
        dcc.Graph(
            id='Power-generation-1'
            )
        ], style={'width': '49%', 'display': 'inline-block'}),
    html.Div([
        html.Label('Pathway 2'),
        dcc.Dropdown(
            id='pathway-selection-2',
            options = [{'label': i, 'value': i} for i in pathways_eg],
            value = 'B1C0T0E0'
            ),
        html.Label('Region/Country 2'),
        dcc.Dropdown(
            id='region-country-selection-2',
            options = [{'label': i, 'value': i} for i in regions_eg],
            value = 'EU+CH+NO'
            ),
        
        dcc.Graph(
            id='Power-generation-2'
            )
        ],style = {'width': '49%', 'display': 'inline-block', 'float': 'right'})
    ])
# app.css.append_css({
#     'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
# })

@app.callback(
    Output('Power-generation-1', 'figure'),
    [Input('pathway-selection-1', 'value'),
     Input('region-country-selection-1', 'value')])

#%% Function for updating graph
def update_graph_1(selected_pathway, selected_region):
    filtered_df = df_eg[(df_eg['pathway'] == selected_pathway) & (df_eg['region'] == selected_region)]
    filtered_df_p = filtered_df.pivot(index='year', columns='indicator',  values='value')
    years = filtered_df['year'].unique()
    traces = []
    fuel_short = pd.DataFrame({'fuel_name':['Wind','Hydro','Biofuel liquid','Coal','Biomass solid','Waste non renewable','Oil','Nuclear','Natural gas / non renew.','Ocean','Geothermal','Solar'],'fuel_abr':['wind','hydro','biofuel','coal','biomass','waste','oil','nuclear','gas','ocean','geo','solar']}, columns = ['fuel_name','fuel_abr'])
    #%% Facts dict
    info_dict = {}
    info_dict['Filename'] = ['{}_OSeMBE_plot_generation' .format(pd.to_datetime('today').strftime("%Y-%m-%d"))]
    info_dict['Unit'] = filtered_df.loc[:,'unit'].unique()
    info_dict['Pathway'] = filtered_df.loc[:,'pathway'].unique()
    info_dict['Year'] = filtered_df.loc[:,'year'].unique().tolist()
    info_dict['Y-Axis'] = ['{}'.format(*info_dict['Unit'])]
    fuels = np.sort(filtered_df['indicator'].unique())
    for i in fuels:
        temp = fuel_short.loc[fuel_short['fuel_name']==i,'fuel_abr']
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

@app.callback(
     Output('Power-generation-2', 'figure'),
    [Input('pathway-selection-2', 'value'),
     Input('region-country-selection-2', 'value')])
#%% Function for updating graph
def update_graph_2(selected_pathway, selected_region):
    filtered_df = df_eg[(df_eg['pathway'] == selected_pathway) & (df_eg['region'] == selected_region)]
    filtered_df_p = filtered_df.pivot(index='year', columns='indicator',  values='value')
    years = filtered_df['year'].unique()
    traces = []
    fuel_short = pd.DataFrame({'fuel_name':['Wind','Hydro','Biofuel liquid','Coal','Biomass solid','Waste non renewable','Oil','Nuclear','Natural gas / non renew.','Ocean','Geothermal','Solar'],'fuel_abr':['wind','hydro','biofuel','coal','biomass','waste','oil','nuclear','gas','ocean','geo','solar']}, columns = ['fuel_name','fuel_abr'])
    #%% Facts dict
    info_dict = {}
    info_dict['Filename'] = ['{}_OSeMBE_plot_generation' .format(pd.to_datetime('today').strftime("%Y-%m-%d"))]
    info_dict['Unit'] = filtered_df.loc[:,'unit'].unique()
    info_dict['Pathway'] = filtered_df.loc[:,'pathway'].unique()
    info_dict['Year'] = filtered_df.loc[:,'year'].unique().tolist()
    info_dict['Y-Axis'] = ['{}'.format(*info_dict['Unit'])]
    fuels = np.sort(filtered_df['indicator'].unique())
    for i in fuels:
        temp = fuel_short.loc[fuel_short['fuel_name']==i,'fuel_abr']
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
if __name__ == '__main__':
    app.run_server(debug=False)