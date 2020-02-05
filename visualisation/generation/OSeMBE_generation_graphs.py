# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 13:26:45 2020

@author: haukeh
"""

# basic
import sys
import getpass
import pandas as pd
import pathlib
from sqlalchemy import *
# plot
import plotly.graph_objs as go
import plotly.offline as pltly

pltly.init_notebook_mode(connected=True)


#%%Database Connection

# This function creates a database connection to the reeem_db.
# The default user is reeem_vis, a user that has only read rights.

# This section establishes the database connection and asks for the password.
# The username can be changed in the corresponding function above.
# If you don't have a username or forgot your password please contact your database admins.

def reeem_session():
    """SQLAlchemy session object with valid connection to reeem database"""
    
    print('Please provide connection parameters to database:\n' +
              'Hit [Enter] to take defaults')
    host = '130.226.55.43' # input('host (default 130.226.55.43): ')
    port = '5432' # input('port (default 5432): ')
    database = 'reeem' # input("database name (default 'reeem'): ")
    user = 'reeem_vis' # input('user (default postgres): ')
    # password = input('password: ')
    password = getpass.getpass(prompt='password: ',
                                   stream=sys.stderr)
    con = create_engine(
            'postgresql://' + '%s:%s@%s:%s/%s' % (user,
                                                  password,
                                                  host,
                                                  port,
                                                  database)).connect()
    print('Password correct! Database connection established.')
    return con

con = reeem_session()

#%% Table Info
# Database
schema = 'model_draft'
table_in = 'reeem_osembe_input'
table_out = 'reeem_osembe_output'
folder = 'osembe'

pathlib.Path('data/'+folder).mkdir(parents=True, exist_ok=True) 
print("Database Schema:", schema +'\n'+ "Input table:", table_in +'\n'+ 
      "Output table:", table_out +'\n'+ "Created folder:", folder )

#%% List of Pathways in database
# Pathways
column = 'pathway,version' # id, pathway, version, region, year, indicator, category, value, unit
sql = text("""
    SELECT  'In' AS data, {3}, count(*) AS count
    FROM    {0}.{1}
    WHERE version = 'DataV2'
    GROUP BY {3} 
    UNION ALL 
    SELECT  'Out' AS data, {3}, count(*) AS count
    FROM    {0}.{2}
    WHERE version = 'DataV2'
    GROUP BY {3} 
    ORDER BY {3}; """.format(schema, table_in, table_out, column))
df_path = pd.read_sql_query(sql, con)

pathway = 'B1C0T0E0'
#%% Database query for the electricity generation data
# Database select (SQL)
sql = text("""
    SELECT  pathway, version, region, year, category, indicator, value, unit  -- column
    FROM    {0}.{1}                               -- table
    WHERE   pathway = '{2}'
        AND (category = 'Electricity Production from Public and Industrial Power and CHP Plants by Fuel and Technology_Coal'
            OR category = 'Electricity Production from Public and Industrial Power and CHP Plants by Fuel and Technology_Oil'
            OR category = 'Electricity Production from Public and Industrial Power and CHP Plants by Fuel and Technology_Natural gas / non renew.'
            OR category = 'Electricity Production from Public and Industrial Power and CHP Plants by Fuel and Technology_Nuclear'
            OR category = 'Electricity Production from Public and Industrial Power and CHP Plants by Fuel and Technology_Waste non renewable'
            OR category = 'Electricity Production from Public and Industrial Power and CHP Plants by Fuel and Technology_Biomass solid'
            OR category = 'Electricity Production from Public and Industrial Power and CHP Plants by Fuel and Technology_Biofuel liquid'
            OR category = 'Electricity Production from Public and Industrial Power and CHP Plants by Fuel and Technology_Hydro'
            OR category = 'Electricity Production from Public and Industrial Power and CHP Plants by Fuel and Technology_Wind'
            OR category = 'Electricity Production from Public and Industrial Power and CHP Plants by Fuel and Technology_Solar'
            OR category = 'Electricity Production from Public and Industrial Power and CHP Plants by Fuel and Technology_Geothermal'
            OR category = 'Electricity Production from Public and Industrial Power and CHP Plants by Fuel and Technology_Ocean')
        AND (indicator = 'Coal'
            OR indicator = 'Oil'
            OR indicator = 'Natural gas / non renew.'
            OR indicator = 'Nuclear'
            OR indicator = 'Waste non renewable'
            OR indicator = 'Biomass solid'
            OR indicator = 'Biofuel liquid'
            OR indicator = 'Hydro'
            OR indicator = 'Wind'
            OR indicator = 'Solar'
            OR indicator = 'Geothermal'
            OR indicator = 'Ocean')
        --AND framework = 'FrameworkNA'              
        AND version = 'DataV2'                    -- filter 3
    ORDER BY pathway, version, year;              -- sorting """.format(schema, table_out, pathway))
df_6 = pd.read_sql_query(sql, con)
#print(df_6)
# print(df_6.region.unique())

#%% regions in dataframe
regions = df_6.loc[:,'region'].unique()

#%% Loop over all regions in dataframe

for region in regions:
    #%% Create df for selected region or country
    df_6_reg = df_6[df_6['region']==region]
    df_6_reg.head(5)
    #%% Stack data
    # Reshape dataframe
    
    df_6p = df_6_reg.pivot(index='year', columns='indicator',  values='value')
    df_6p.head(5)
    
    #%% Facts dict
    
    info_dict_6 = {}
    info_dict_6['Filename'] = ['{}_reeem_plot_6' .format(pd.to_datetime('today').strftime("%Y-%m-%d"))]
    info_dict_6['Unit'] = df_6.loc[:,'unit'].unique()
    info_dict_6['Pathway'] = df_6.loc[:,'pathway'].unique()
    info_dict_6['Year'] = df_6.loc[:,'year'].unique().tolist()
    info_dict_6['Region'] = df_6_reg.loc[:,'region'].unique()
    info_dict_6['Y-Axis'] = ['{}'.format(*info_dict_6['Unit'])]
    
    #%% Interactive Plot
    x = df_6['year'].unique()
    
    coal = dict(
        x=x,
        y=df_6p.loc[:,'Coal'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5,
                 color='rgb(0, 0, 0)'),
        stackgroup='one',
        name = 'Coal'
    )
    oil = dict(
        x=x,
        y=df_6p.loc[:,'Oil'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5,
                 color='rgb(121, 43, 41)'),
        stackgroup='one',
        name = 'HFO'
    )
    gas = dict(
        x=x,
        y=df_6p.loc[:,'Natural gas / non renew.'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5,
                 color='rgb(86, 108, 140)'),
        stackgroup='one',
        name = 'Natural gas'
    )
    nuclear = dict(
        x=x,
        y=df_6p.loc[:,'Nuclear'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5,
                 color='rgb(186, 28, 175)'),
        stackgroup='one',
        name = 'Nuclear'
    )
    waste = dict(
        x=x,
        y=df_6p.loc[:,'Waste non renewable'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5,
                 color='rgb(138, 171, 71)'),
        stackgroup='one',
        name = 'Waste'
    )
    biomass = dict(
        x=x,
        y=df_6p.loc[:,'Biomass solid'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5,
                 color='rgb(172, 199, 119)'),
        stackgroup='one',
        name = 'Biomass'
    )
    biofuel = dict(
        x=x,
        y=df_6p.loc[:,'Biofuel liquid'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5,
                 color='rgb(79, 98, 40)'),
        stackgroup='one',
        name = 'Biofuel'
    )
    hydro = dict(
        x=x,
        y=df_6p.loc[:,'Hydro'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5,
                 color='rgb(0, 139, 188)'),
        stackgroup='one',
        name = 'Hydro'
    )
    wind = dict(
        x=x,
        y=df_6p.loc[:,'Wind'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5,
                 color='rgb(143, 119, 173)'),
        stackgroup='one',
        name = 'Wind'
    )
    solar = dict(
        x=x,
        y=df_6p.loc[:,'Solar'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5,
                 color='rgb(230, 175, 0)'),
        stackgroup='one',
        name = 'Solar'
    )
    geo = dict(
        x=x,
        y=df_6p.loc[:,'Geothermal'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5,
                 color='rgb(192, 80, 77)'),
        stackgroup='one',
        name = 'Geothermal'
    )
    ocean = dict(
        x=x,
        y=df_6p.loc[:,'Ocean'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5,
                 color='rgb(22, 54, 92)'),
        stackgroup='one',
        name = 'Ocean'
    )
    # Set layout
    layout_generation = go.Layout(
        #height=1000, width = 10000,
        #title='CO2-Emissions in EU28',
        title='Electricity generation in {} in scenario {}'.format(*info_dict_6['Region'],*info_dict_6['Pathway']),
        # yaxis=dict(title='CO2-Emissions in Mt') )
        yaxis=dict(title=''.join(info_dict_6['Y-Axis'])) )
    
    data = [coal, oil, gas, nuclear, waste, biomass, biofuel, hydro, wind, solar, geo, ocean]
    
    #%% Build and show graph
    fig = go.Figure(data=data, layout=layout_generation)
    pltly.iplot(fig)
    
    #%% Save graphs as html
    
    htmlname = 'data/{}_{}.html' .format(*info_dict_6['Pathway'],*info_dict_6['Region'])
    pltly.plot(fig, filename=htmlname)