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
df_eg = pd.read_pickle('data\OSeMBE_ProductionByTechnologyAnnual_DataV3R1_2020-07-09.pkl')
pathways_eg = df_eg.loc[:,'pathway'].unique()
df_eg['region'] = df_eg['info_1'].apply(lambda x: x[:2])
df_eg['fuel'] = df_eg['info_1'].apply(lambda x: x[2:4])
df_eg['tech'] = df_eg['info_1'].apply(lambda x: x[4:6])
df_eg['unit'] = 'PJ'
regions_eg = np.sort(df_eg.loc[:,'region'].unique())

df_ate = pd.read_pickle('data\OSeMBE_AnnualTechnologyEmission_DataV3R1_2020-07-09.pkl')
df_c2t = df_ate[df_ate['info_2']=='CO2']
pathways_c2t = df_c2t.loc[:,'pathway'].unique()
df_c2t['region'] = df_c2t['info_1'].apply(lambda x: x[:2])
df_c2t['import/domestic'] = df_c2t['info_1'].apply(lambda x: x[6])
df_c2t['fuel_source'] = df_c2t['info_1'].apply(lambda x: x[2:4]+x[6])
df_c2t = df_c2t[(df_c2t['import/domestic']=='I') | (df_c2t['import/domestic']=='X')]
df_c2t['unit'] = 'kt'
regions_c2t = df_c2t['region'].unique()

df_tca = pd.read_pickle('data\OSeMBE_TotalCapacityAnnual_DataV3R1_2020-07-09.pkl')
pathways_tca = df_tca.loc[:,'pathway'].unique()
df_tca['region'] = df_tca['info_1'].apply(lambda x: x[:2])
df_tca['fuel'] = df_tca['info_1'].apply(lambda x: x[2:4])
df_tca['tech'] = df_tca['info_1'].apply(lambda x: x[4:6])
df_tca = df_tca[((df_tca['fuel']!='EL')&(df_tca['fuel']!='OI')) & (df_tca['tech']!='00')]
df_tca['unit'] = 'GW'
regions_tca = df_tca['region'].unique()

if np.logical_and((pathways_eg==pathways_c2t).all(), (pathways_c2t==pathways_tca).all()) == False:
    print('WARNING: It seems you are importing your results from files that contain different numbers of scenarios.')
    # If more result parameter are added this could be updated following this approach: https://stackoverflow.com/questions/37777529/comparing-multiple-numpy-arrays
print('Section 1 run')

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
#%% functions for returning positives and negatives
def positives(value):
    return max(value, 0)
def negatives(value):
    return min(value, 0)
#%% function to create df with import and export of electricity for selected country
def impex(selected_pathway, selected_country):
    # selected_pathway = 'B1C0T0E0'
    # selected_country = 'CH'
    df = df_eg[(df_eg['fuel']=='EL')&((df_eg['region']==selected_country)|(df_eg['tech']==selected_country))&(df_eg['tech']!='00')&(df_eg['pathway']==selected_pathway)]
    countries = []
    countries = list(df['region'].unique())
    countries.extend(df['tech'].unique())
    countries = list(dict.fromkeys(countries))
    df = df[df['info_2'].str.contains('|'.join(countries))]
    df = df[df['info_2'].str.contains('E1')]
    years = pd.Series(df['year'].unique())
    net_imp = pd.DataFrame(index=years)
    neighbours = []
    for i in countries:
        if i != selected_country:
            neighbours.append(i)
    links = list(df['info_1'].unique())
    label_imp = []
    label_exp = []
    i = 0
    for link in links:
        imp = df[(df['info_1']==link) & (df['info_2']==(selected_country+'E1'))]
        imp = imp.set_index(years)
        exp = df[(df['info_1']==link) & (df['info_2']==(neighbours[i]+'E1'))]
        exp = exp.set_index(years) 
        net_imp[link] = imp['value'] - exp['value']
        label_imp.append(link+'_imp')
        label_exp.append(link+'_exp')
        i += 1
    net_imp_pos = pd.DataFrame(index=years,columns=links)
    net_imp_neg = pd.DataFrame(index=years,columns=links)
    for link in links:
        net_imp_pos[link] = net_imp[link].map(positives)
        net_imp_neg[link] = net_imp[link].map(negatives)
    net_imp_pos.columns = label_imp
    net_imp_neg.columns = label_exp
    return net_imp_neg, net_imp_pos
        
#%% dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='OSeMBE results'),
    
    html.H2(children='Total Annual Capacity'),
    html.Div([
        html.Label('Installed power generation capacity - Pathway 1'),
        dcc.Dropdown(
            id='tca-pathway-selection-1',
            options = [{'label': i, 'value': i} for i in pathways_tca],
            value = 'B1C0T0E0'
            ),
        html.Label('Installed power generation capacity - Country 1'),
        dcc.Dropdown(
            id='tca-country-selection-1',
            options = [{'label': i, 'value': i} for i in regions_tca],
            value = 'AT'
            ),
        dcc.Graph(
            id='tca-graph-1'
            )
        ], style={'width': '49%', 'display': 'inline-block'}
        ),
    html.Div([
        html.Label('Installed power generation capacity - Pathway 2'),
        dcc.Dropdown(
            id='tca-pathway-selection-2',
            options = [{'label': i, 'value': i} for i in pathways_tca],
            value = 'B1C0T0E0'
            ),
        html.Label('Installed power generation capacity - Country 2'),
        dcc.Dropdown(
            id='tca-country-selection-2',
            options = [{'label': i, 'value': i} for i in regions_tca],
            value = 'AT'
            ),
        dcc.Graph(
            id='tca-graph-2'
            )
        ], style={'width': '49%', 'display': 'inline-block'}
        ),
    
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
    # selected_region = 'CH'
    countr_el1 = selected_region + 'E1'
    countr_el2 = selected_region + 'E2'
    filtered_df = df_eg[
        (df_eg['pathway'] == selected_pathway) 
        & (df_eg['region'] == selected_region) 
        & ((df_eg['info_2']==countr_el1)|(df_eg['info_2']==countr_el2)) 
        & (df_eg['fuel']!='EL') 
        & (df_eg['tech']!='00')]
    
    filtered_df['production'] = filtered_df.groupby(['info_1','year'])['value'].transform('sum')
    filtered_df = filtered_df[filtered_df['info_2']==countr_el2]
    filtered_df_p = filtered_df.pivot(index='year', columns='info_1',  values='production')
    elexp, elimp = impex(selected_pathway, selected_region)
    df_graph = elimp
    # df_graph = df_graph.join(pos_imp)
    df_graph = df_graph.join(filtered_df_p)
    df_graph = df_graph[(df_graph.T != 0).any()]
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
    techs_exp = list(elexp)
    for i in techs_exp:
        fuel = i[2:4]
        temp = fuel_short.loc[fuel_short['fuel_name']==fuel,'fuel_abr']
        fuel_code = temp.iloc[0]
        traces.append(dict(
            x = years,
            y = elexp.loc[:,i],
            # hoverinfo='x+y',
            name = i,
            hovertemplate=
            '<br>Production: %{y}PJ</br>'+
            'Year: %{x}',
            mode='line',
            line=dict(width=0.5,
                      color=colours[fuel_code]),
            stackgroup='one',
            showlegend = False
            ))
    techs = list(df_graph)
    for i in techs:
        fuel = i[2:4]
        temp = fuel_short.loc[fuel_short['fuel_name']==fuel,'fuel_abr']
        fuel_code = temp.iloc[0]
        traces.append(dict(
            x = years,
            y = df_graph.loc[:,i],
            # hoverinfo='x+y',
            hovertemplate=
            '<br>Production: %{y}PJ</br>'+
            'Year: %{x}',
            mode='line',
            line=dict(width=0.5,
                      color=colours[fuel_code]),
            stackgroup='two',
            name=i,
            showlegend = False
            ))
    return {
        'data': traces,
        'layout': dict(
            title='Electricity generation in {} in scenario {}'.format(selected_region,selected_pathway),
            yaxis=dict(title=''.join(info_dict['Y-Axis'])),
            hovermode= 'closest',
            font=dict(family='Aleo'),
            )
        }

@app.callback(
      Output('Power-generation-2', 'figure'),
    [Input('pg-pathway-selection-2', 'value'),
      Input('pg-region-country-selection-2', 'value')])
#%% Function for updating graph
def update_graph_2(selected_pathway, selected_region):
    countr_el1 = selected_region + 'E1'
    countr_el2 = selected_region + 'E2'
    filtered_df = df_eg[
        (df_eg['pathway'] == selected_pathway) 
        & (df_eg['region'] == selected_region) 
        & ((df_eg['info_2']==countr_el1)|(df_eg['info_2']==countr_el2)) 
        & (df_eg['fuel']!='EL') 
        & (df_eg['tech']!='00')]
    
    filtered_df['production'] = filtered_df.groupby(['info_1','year'])['value'].transform('sum')
    filtered_df = filtered_df[filtered_df['info_2']==countr_el2]
    filtered_df_p = filtered_df.pivot(index='year', columns='info_1',  values='production')
    elexp, elimp = impex(selected_pathway, selected_region)
    df_graph = elimp
    # df_graph = df_graph.join(pos_imp)
    df_graph = df_graph.join(filtered_df_p)
    df_graph = df_graph[(df_graph.T != 0).any()]
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
    techs_exp = list(elexp)
    for i in techs_exp:
        fuel = i[2:4]
        temp = fuel_short.loc[fuel_short['fuel_name']==fuel,'fuel_abr']
        fuel_code = temp.iloc[0]
        traces.append(dict(
            x = years,
            y = elexp.loc[:,i],
            # hoverinfo='x+y',
            hovertemplate=
            '<br>Production: %{y}PJ</br>'+
            'Year: %{x}',
            mode='line',
            line=dict(width=0.5,
                      color=colours[fuel_code]),
            stackgroup='one',
            name=i,
            showlegend = False
            ))
    techs = list(df_graph)
    for i in techs:
        fuel = i[2:4]
        temp = fuel_short.loc[fuel_short['fuel_name']==fuel,'fuel_abr']
        fuel_code = temp.iloc[0]
        traces.append(dict(
            x = years,
            y = df_graph.loc[:,i],
            # hoverinfo='x+y',
            hovertemplate=
            '<br>Production: %{y}PJ</br>'+
            'Year: %{x}',
            mode='line',
            line=dict(width=0.5,
                      color=colours[fuel_code]),
            stackgroup='two',
            name=i,
            showlegend = False
            ))
    return {
        'data': traces,
        'layout': dict(
            title='Electricity generation in {} in scenario {}'.format(selected_region,selected_pathway),
            yaxis=dict(title=''.join(info_dict['Y-Axis'])),
            hovermode= 'closest',
            font=dict(family='Aleo'),
            )
        }

@app.callback(
      Output('c2t-graph-1', 'figure'),
    [Input('c2t-pathway-selection-1', 'value'),
      Input('c2t-country-selection-1', 'value')])
#%% Function for updating graph
def update_graph_3(selected_pathway, selected_region):
    # selected_pathway = 'B1C0T0E0'
    # selected_region = 'DE'
    filtered_df = df_c2t[(df_c2t['pathway'] == selected_pathway) & (df_c2t['region'] == selected_region)]
    filtered_df_p = filtered_df.pivot(index='year', columns='fuel_source',  values='value')
    years = filtered_df['year'].unique()
    traces = []
    fuel_short = pd.DataFrame({'fuel_name':['BFI','BFX','BMI','BMX','COI','COX','GOX','HFI','NGI','NGX','OII','OIX','URI','WSX'],'fuel_abr':['biofuel','biofuel','biomass','biomass','coal','coal','geo','oil','gas','gas','oil','oil','nuclear','waste']}, columns = ['fuel_name','fuel_abr'])
    #%% Facts dict
    info_dict = {}
    info_dict['Filename'] = ['{}_OSeMBE_plot_emission' .format(pd.to_datetime('today').strftime("%Y-%m-%d"))]
    info_dict['Unit'] = filtered_df.loc[:,'unit'].unique()
    info_dict['Pathway'] = filtered_df.loc[:,'pathway'].unique()
    info_dict['Year'] = filtered_df.loc[:,'year'].unique().tolist()
    info_dict['Y-Axis'] = ['{}'.format(*info_dict['Unit'])]
    fuels = np.sort(filtered_df['fuel_source'].unique())
    for i in fuels:
        temp = fuel_short.loc[fuel_short['fuel_name']==i,'fuel_abr']
        fuel_code = temp.iloc[0]
        traces.append(dict(
            x = years,
            y = filtered_df_p.loc[:,i],
            hovertemplate=
            '<br>CO2: %{y}kt</br>'+
            'Year: %{x}',
            mode='line',
            line=dict(width=0.5,
                      color=colours[fuel_code]),
            stackgroup='one',
            name=i,
            showlegend= False
            ))
    return {
        'data': traces,
        'layout': dict(
            title='CO2 Emissions in {} in scenario {}'.format(selected_region,selected_pathway),
            yaxis=dict(title=''.join(info_dict['Y-Axis'])),
            hovermode= 'closest',
            font=dict(family='Aleo'),
            )
        }

#%% Function for updating graph
@app.callback(
      Output('c2t-graph-2', 'figure'),
    [Input('c2t-pathway-selection-2', 'value'),
      Input('c2t-country-selection-2', 'value')])

def update_graph_4(selected_pathway, selected_region):
    # selected_pathway = 'B0C0T0E0'
    # selected_region = 'DE'
    filtered_df = df_c2t[(df_c2t['pathway'] == selected_pathway) & (df_c2t['region'] == selected_region)]
    filtered_df_p = filtered_df.pivot(index='year', columns='fuel_source',  values='value')
    years = filtered_df['year'].unique()
    traces = []
    fuel_short = pd.DataFrame({'fuel_name':['BFI','BFX','BMI','BMX','COI','COX','GOX','HFI','NGI','NGX','OII','OIX','URI','WSX'],'fuel_abr':['biofuel','biofuel','biomass','biomass','coal','coal','geo','oil','gas','gas','oil','oil','nuclear','waste']}, columns = ['fuel_name','fuel_abr'])
    #%% Facts dict
    info_dict = {}
    info_dict['Filename'] = ['{}_OSeMBE_plot_emission' .format(pd.to_datetime('today').strftime("%Y-%m-%d"))]
    info_dict['Unit'] = filtered_df.loc[:,'unit'].unique()
    info_dict['Pathway'] = filtered_df.loc[:,'pathway'].unique()
    info_dict['Year'] = filtered_df.loc[:,'year'].unique().tolist()
    info_dict['Y-Axis'] = ['{}'.format(*info_dict['Unit'])]
    fuels = np.sort(filtered_df['fuel_source'].unique())
    for i in fuels:
        temp = fuel_short.loc[fuel_short['fuel_name']==i,'fuel_abr']
        fuel_code = temp.iloc[0]
        traces.append(dict(
            x = years,
            y = filtered_df_p.loc[:,i],
            hovertemplate=
            '<br>CO2: %{y}kt</br>'+
            'Year: %{x}',
            mode='lines',
            line=dict(width=0.5,
                      color=colours[fuel_code]),
            stackgroup='one',
            name=i,
            showlegend= False
            ))
    return {
        'data': traces,
        'layout': dict(
            title='CO2 Emissions in {} in scenario {}'.format(selected_region,selected_pathway),
            yaxis=dict(title=''.join(info_dict['Y-Axis'])),
            hovermode= 'closest',
            font=dict(family='Aleo'),
            )
        }
#%% Function for updating graph
@app.callback(
      Output('tca-graph-1', 'figure'),
    [Input('tca-pathway-selection-1', 'value'),
      Input('tca-country-selection-1', 'value')])

def update_graph_5(selected_pathway, selected_region):
    traces = []
    # selected_pathway = 'B1C0T0E0'
    # selected_region = 'DE'
    filtered_df = df_tca[(df_tca['pathway'] == selected_pathway) & (df_tca['region'] == selected_region)]
    filtered_df_p = filtered_df.pivot(index='year', columns='info_1',  values='value')
    fuel_short = pd.DataFrame({'fuel_name':['WI','HY','BF','CO','BM','WS','HF','NU','NG','OC','OI','GO','SO','EL'],'fuel_abr':['wind','hydro','biofuel','coal','biomass','waste','oil','nuclear','gas','ocean','oil','geo','solar','imports']}, columns = ['fuel_name','fuel_abr'])
    info_dict = {}
    info_dict['Unit'] = filtered_df.loc[:,'unit'].unique()
    info_dict['Y-Axis'] = ['{}'.format(*info_dict['Unit'])]
    techs = list(filtered_df_p)
    years = filtered_df['year'].unique()
    for i in techs:
        fuel = i[2:4]
        temp = fuel_short.loc[fuel_short['fuel_name']==fuel,'fuel_abr']
        fuel_code = temp.iloc[0]
        traces.append(dict(
            x = years,
            y = filtered_df_p.loc[:,i],
            # hoverinfo='x+y',
            hovertemplate=
            'Capacity: %{y}GW',
            mode='line',
            line=dict(width=0.5,
                      color=colours[fuel_code]),
            stackgroup='one',
            name=i,
            showlegend = False
            ))
    return {
        'data': traces,
        'layout': dict(
            title='Installed power generation capacity in {} in scenario {}'.format(selected_region,selected_pathway),
            yaxis=dict(title=''.join(info_dict['Y-Axis'])),
            hovermode= 'closest',
            font=dict(family='Aleo'),
            )
        }
#%% Function for updating graph
@app.callback(
      Output('tca-graph-2', 'figure'),
    [Input('tca-pathway-selection-2', 'value'),
      Input('tca-country-selection-2', 'value')])

def update_graph_6(selected_pathway, selected_region):
    traces = []
    # selected_pathway = 'B1C0T0E0'
    # selected_region = 'DE'
    filtered_df = df_tca[(df_tca['pathway'] == selected_pathway) & (df_tca['region'] == selected_region)]
    filtered_df_p = filtered_df.pivot(index='year', columns='info_1',  values='value')
    fuel_short = pd.DataFrame({'fuel_name':['WI','HY','BF','CO','BM','WS','HF','NU','NG','OC','OI','GO','SO','EL'],'fuel_abr':['wind','hydro','biofuel','coal','biomass','waste','oil','nuclear','gas','ocean','oil','geo','solar','imports']}, columns = ['fuel_name','fuel_abr'])
    info_dict = {}
    info_dict['Unit'] = filtered_df.loc[:,'unit'].unique()
    info_dict['Y-Axis'] = ['{}'.format(*info_dict['Unit'])]
    techs = list(filtered_df_p)
    years = filtered_df['year'].unique()
    for i in techs:
        fuel = i[2:4]
        temp = fuel_short.loc[fuel_short['fuel_name']==fuel,'fuel_abr']
        fuel_code = temp.iloc[0]
        traces.append(dict(
            x = years,
            y = filtered_df_p.loc[:,i],
            # hoverinfo='x+y',
            hovertemplate=
            'Capacity: %{y}GW',
            mode='line',
            line=dict(width=0.5,
                      color=colours[fuel_code]),
            stackgroup='one',
            name=i,
            showlegend = False
            ))
    return {
        'data': traces,
        'layout': dict(
            title='Installed power generation capacity in {} in scenario {}'.format(selected_region,selected_pathway),
            yaxis=dict(title=''.join(info_dict['Y-Axis'])),
            hovermode= 'closest',
            font=dict(family='Aleo'),
            )
        }

if __name__ == '__main__':
    app.run_server(debug=False)