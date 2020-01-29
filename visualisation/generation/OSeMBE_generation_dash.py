# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 12:05:23 2020

@author: haukeh
"""

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html

df = pd.read_pickle('B1C0T0E0_generation.pkl')
pathways = df.loc[:,'pathway'].unique()
regions = df.loc[:,'region'].unique()

for pathway in pathways:
    df_path = df[df['pathway']==pathway]
    for region in regions:
        #%% Create df for selected region or country
        df_reg = df_path[df_path['region']==region]
        #%% Stack data / Reshape dataframe
        df_reg_p = df_reg.pivot(index='year', columns='indicator',  values='value')
        #%% Facts dict
        info_dict = {}
        info_dict['Filename'] = ['{}_OSeMBE_plot_generation' .format(pd.to_datetime('today').strftime("%Y-%m-%d"))]
        info_dict['Unit'] = df_reg.loc[:,'unit'].unique()
        info_dict['Pathway'] = df_reg.loc[:,'pathway'].unique()
        info_dict['Year'] = df_reg.loc[:,'year'].unique().tolist()
        info_dict['Region'] = df_reg.loc[:,'region'].unique()
        info_dict['Y-Axis'] = ['{}'.format(*info_dict['Unit'])]
        #%% Plot elements
        years = df_reg['year'].unique()
        coal = dict(
            x=years,
            y=df_reg_p.loc[:,'Coal'],
            hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5,
                     color='rgb(0, 0, 0)'),
            stackgroup='one',
            name = 'Coal'
        )
        oil = dict(
            x=years,
            y=df_reg_p.loc[:,'Oil'],
            hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5,
                     color='rgb(121, 43, 41)'),
            stackgroup='one',
            name = 'HFO'
        )
        gas = dict(
            x=years,
            y=df_reg_p.loc[:,'Natural gas / non renew.'],
            hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5,
                     color='rgb(86, 108, 140)'),
            stackgroup='one',
            name = 'Natural gas'
        )
        nuclear = dict(
            x=years,
            y=df_reg_p.loc[:,'Nuclear'],
            hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5,
                     color='rgb(186, 28, 175)'),
            stackgroup='one',
            name = 'Nuclear'
        )
        waste = dict(
            x=years,
            y=df_reg_p.loc[:,'Waste non renewable'],
            hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5,
                     color='rgb(138, 171, 71)'),
            stackgroup='one',
            name = 'Waste'
        )
        biomass = dict(
            x=years,
            y=df_reg_p.loc[:,'Biomass solid'],
            hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5,
                     color='rgb(172, 199, 119)'),
            stackgroup='one',
            name = 'Biomass'
        )
        biofuel = dict(
            x=years,
            y=df_reg_p.loc[:,'Biofuel liquid'],
            hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5,
                     color='rgb(79, 98, 40)'),
            stackgroup='one',
            name = 'Biofuel'
        )
        hydro = dict(
            x=years,
            y=df_reg_p.loc[:,'Hydro'],
            hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5,
                     color='rgb(0, 139, 188)'),
            stackgroup='one',
            name = 'Hydro'
        )
        wind = dict(
            x=years,
            y=df_reg_p.loc[:,'Wind'],
            hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5,
                     color='rgb(143, 119, 173)'),
            stackgroup='one',
            name = 'Wind'
        )
        solar = dict(
            x=years,
            y=df_reg_p.loc[:,'Solar'],
            hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5,
                     color='rgb(230, 175, 0)'),
            stackgroup='one',
            name = 'Solar'
        )
        geo = dict(
            x=years,
            y=df_reg_p.loc[:,'Geothermal'],
            hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5,
                     color='rgb(192, 80, 77)'),
            stackgroup='one',
            name = 'Geothermal'
        )
        ocean = dict(
            x=years,
            y=df_reg_p.loc[:,'Ocean'],
            hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5,
                     color='rgb(22, 54, 92)'),
            stackgroup='one',
            name = 'Ocean'
        )
    # Set layout
        layout = dict(font=dict(family='Aleo'))
    # layout_generation = go.Layout(
    #     #height=1000, width = 10000,
    #     #title='CO2-Emissions in EU28',
    #     title='Electricity generation in {} in scenario {}'.format(*info_dict_6['Region'],*info_dict_6['Pathway']),
    #     # yaxis=dict(title='CO2-Emissions in Mt') )
    #     yaxis=dict(title=''.join(info_dict_6['Y-Axis'])) )
    
        data = [coal, oil, gas, nuclear, waste, biomass, biofuel, hydro, wind, solar, geo, ocean]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Power generation'),
    
    html.Div(children='''
             Country XY
    '''),
    
    dcc.Graph(
        id='Power generation',
        figure={
            'data': data,
            'layout': layout
            }
        )
    ])
if __name__ == '__main__':
    app.run_server(debug=True)