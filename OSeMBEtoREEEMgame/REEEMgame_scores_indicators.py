# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 08:09:14 2019

@author: haukeh
"""

import pandas as pd
import numpy as np
import sys
import os
import getpass
import json
import pathlib
from sqlalchemy import *

#%%
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
#%% 
def import_reeemdb(con):
    """This function imports data from the REEEMdb
    
    It imports the data needed to perform the calculations of scores and indicators for the the REEEMgame.
    
    Arguments
    ---------
    
    """
    #database info
    schema = 'model_draft'
    table_in = 'reeem_osembe_input'
    table_out = 'reeem_osembe_output'
    emission = text("""
               SELECT nid, pathway, version, region, year, category, indicator, value, unit -- column
               FROM {0}.{1} -- table
               WHERE category = 'Emissions'
                   AND indicator = 'CO2'
                   AND version = 'DataV2'
                   AND year = '2015'
               ORDER BY version, pathway, year; -- sorting  """.format(schema, table_out))
    cap_cost = text("""
               SELECT nid, pathway, version, region, year, category, indicator, value, unit -- column
               FROM {0}.{1} -- table
               WHERE category = 'CapitalCost'
                   AND version = 'DataV2'
                   AND year = '2015'
               ORDER BY version, pathway, year; -- sorting  """.format(schema, table_in))
    new_capa = text("""
               SELECT nid, pathway, version, region, year, category, indicator, value, unit -- column
               FROM {0}.{1} -- table
               WHERE category = 'New Capacity'
                   AND version = 'DataV2'
                   AND year = '2015'
               ORDER BY version, pathway, year; -- sorting  
                    """.format(schema, table_out))
    rawData = pd.read_sql_query(emission, con)
    cap_cost_df = pd.read_sql_query(cap_cost, con)
    rawData = rawData.append(cap_cost_df, ignore_index = True)
    rawData = rawData.append(new_capa, ignore_index = True)
    return rawData
#%% 
def import_excel(file_name, countries):
    """This function imports data on the population projection 
    
    It imports the population for all countries modelled in OSeMBE and returns them as dictionray with a dataframe per country.
    
    Arguments
    ---------
    file_name : str
        File name of the excel file that contains the population data for the EU countries.
    countries : list
        list with the country codes of all modelled countries
    """
    pop_dic = {}
    non_list_countr = ['CH','NO']
    for country in countries:
        pop_dic[country] = pd.DataFrame()
        pop_data = pd.DataFrame(index=pd.Series(range(2015,2051)))
        pop_data['population'] = np.nan
        if country == 'CH' or country == 'NO':
            raw_data = pd.read_excel('pop_projection_NEWAGE_CH_NO.xlsx','MaGe Factors',usecols="AN:BW",nrows=2)
            raw_data.index = non_list_countr
            raw_data = raw_data.transpose()
            raw_data.index = pd.Series(range(2015,2051))
            raw_data = raw_data.multiply(1000)
            pop_data['population'] = raw_data[country]
            pop_dic[country] = pop_data
        else:
            sheet = str(country+'-A')
            years = pd.read_excel(file_name,sheet,usecols="E:L",nrows=1)
            years = years.iloc[0]
            years = years.tolist()
            pop = pd.read_excel(file_name,sheet,usecols="E:L",skiprows=2,nrows=1)
            pop = pop.transpose()
            pop.index = years
            for y in years:
                pop_data.loc[y]['population'] = pop.loc[y]
            pop_data = pop_data.interpolate()
            pop_data = pop_data.multiply(1000000)
            pop_dic[country] = pop_data
    return pop_dic
#%% Calculation of CO2 intensity per citizen
def co2intensity():
    CO2Intensity = pd.DataFrame()
    return CO2Intensity
#%% Calculation of the Discounted Investment per Citizen
def disc_investment():
    Disc_Investment = pd.DataFrame()
    return Disc_Investment
#%% Calculation of Capital Recovery Factor
def crf():
    crf = pd.DataFrame()
    return crf
#%% Calculation of the Capital Investment per country, technology and year
def ci():
    ci =pd.DataFrame()
    return ci
#%% Calculation of the Annualized Investment Cost
def aic():
    aic = pd.DataFrame()
    return aic
#%% Calculation of the Annual Fixed Operating Cost
def afoc():
    AFOC = pd.DataFrame()
    return AFOC
#%% Calculation of the Annual Variable Operating Cost
def avoc():
    AVOC = pd.DataFrame()
    return AVOC
#%% Calculation of the Dpmesstic Electricity Production per country
def dep():
    DEP = pd.DataFrame()
    return DEP
#%% Calculation of the Levelised Cost of Domestic Electricity
def lcode():
    LCoDE = pd.DataFrame
    return LCoDE
#%% Calculation of the countryspecific LCOEs
def lcoe():
    LCOE = pd.DataFrame()
    return LCOE
#%% Calculation of the Share of national electricity demand in the European electricity Demand
def demand_share():
    DemandShare = pd.DataFrame()
    return DemandShare
#%% Calculation of the EULCOE
def eu_lcoe():
    EULCOE = pd.DataFrame()
    return EULCOE
#%% Main function
def main():
    xls = 'EC, 2016 - AppendixRefSce.xls'
    countries = ['AT','BE','BG','CH','CY','CZ','DE','DK','EE','ES','FR','FI','GR','HR','HU','IE','IT','LT','LU','LV','MT','NL','NO','PL','PT','RO','SE','SI','SK','UK']
    reeem_db_con = reeem_session()
    raw_data = import_reeemdb(reeem_db_con)
#    pop_raw = import_excel(xls,countries)
    
    return raw_data
output = main()
