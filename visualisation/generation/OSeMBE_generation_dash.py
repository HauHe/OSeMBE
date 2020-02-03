# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 12:05:23 2020

@author: haukeh
"""

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

df = pd.read_pickle('B1C0T0E0_generation.pkl')
pathways = df.loc[:,'pathway'].unique()
regions = df.loc[:,'region'].unique()

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
    html.H1(children='Power generation'),
    
    html.Label('Pathway'),
    dcc.Dropdown(
        id='pathway-selection',
        options = [{'label': i, 'value': i} for i in pathways],
        value = 'B1C0T0E0'
        ),
    
    dcc.Dropdown(
        id='region-country-selection',
        options = [{'label': i, 'value': i} for i in regions],
        value = 'EU+CH+NO'
        ),
    
    dcc.Graph(
        id='Power-generation'
        )
    ])

@app.callback(
    Output('Power-generation', 'figure'),
    [Input('pathway-selection', 'value'),
     Input('region-country-selection', 'value')])

#%% Function for updating graph
def update_graph(selected_pathway, selected_region):
    filtered_df = df[(df['pathway'] == selected_pathway) & (df['region'] == selected_region)]
    filtered_df_p = filtered_df.pivot(index='year', columns='indicator',  values='value')
    years = filtered_df['year'].unique()
    traces = []
    fuel_abre = pd.DataFrame({'fuel_name':['Wind','Hydro','Biofuel liquid','Coal','Biomass solid','Waste non renewable','Oil','Nuclear','Natural gas / non renew.','Ocean','Geothermal','Solar'],'fuel_abr':['wind','hydro','biofuel','coal','biomass','waste','oil','nuclear','gas','ocean','geo','solar']}, columns = ['fuel_name','fuel_abr'])
    #%% Facts dict
    info_dict = {}
    info_dict['Filename'] = ['{}_OSeMBE_plot_generation' .format(pd.to_datetime('today').strftime("%Y-%m-%d"))]
    info_dict['Unit'] = filtered_df.loc[:,'unit'].unique()
    info_dict['Pathway'] = filtered_df.loc[:,'pathway'].unique()
    info_dict['Year'] = filtered_df.loc[:,'year'].unique().tolist()
    info_dict['Y-Axis'] = ['{}'.format(*info_dict['Unit'])]
    for i in filtered_df['indicator'].unique():
        temp = fuel_abre.loc[fuel_abre['fuel_name']==i,'fuel_abr']
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