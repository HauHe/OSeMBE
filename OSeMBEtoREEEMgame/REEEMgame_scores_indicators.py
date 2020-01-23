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
               SELECT nid, pathway, version, region, year, category, indicator, value -- column
               FROM {0}.{1} -- table
               WHERE category = 'Emissions'
                   AND indicator = 'CO2'
                   AND version = 'DataV2'
                   AND year = '2015'
               ORDER BY version, pathway, year; -- sorting  """.format(schema, table_out))
    cap_cost = text("""
               SELECT nid, pathway, version, region, year, category, indicator, value -- column
               FROM {0}.{1} -- table
               WHERE category = 'CapitalCost'
                   AND version = 'DataV2'
                   AND year = '2015'
               ORDER BY version, pathway, year; -- sorting  """.format(schema, table_in))
    new_capa = text("""
               SELECT nid, pathway, version, region, year, category, indicator, value -- column
               FROM {0}.{1} -- table
               WHERE (category = 'New Capacity_Coal'
                       OR category = 'New Capacity_Oil'
                       OR category = 'New Capacity_Natural gas / non renew.'
                       OR category = 'New Capacity_Nuclear'
                       OR category = 'New Capacity_Waste non renewable'
                       OR category = 'New Capacity_Biomass solid'
                       OR category = 'New Capacity_Biofuel liquid'
                       OR category = 'New Capacity_Hydro'
                       OR category = 'New Capacity_Wind'
                       OR category = 'New Capacity_Solar'
                       OR category = 'New Capacity_Geothermal'
                       OR category = 'New Capacity_Ocean') 
                   AND version = 'DataV2'
                   AND year = '2015'
               ORDER BY version, pathway, year; -- sorting  """.format(schema, table_out))
    discount_rate = text("""
               SELECT nid, pathway, version, region, year, category, indicator, value -- column
               FROM {0}.{1} -- table
               WHERE category = 'DiscountRate'
                   AND version = 'DataV2'
                   AND region = 'EU+CH+NO'
                   AND year = '2015'
               ORDER BY version, pathway, year; -- sorting  """.format(schema, table_in))
    oper_life = text("""
               SELECT nid, pathway, version, region, year, category, indicator, value -- column
               FROM {0}.{1} -- table
               WHERE category = 'OperationalLife'
                   AND version = 'DataV2'
                   AND year = '2015'
               ORDER BY version, pathway, year; -- sorting  """.format(schema, table_in))
    inst_capa = text("""
               SELECT nid, pathway, version, region, year, category, indicator, value -- column
               FROM {0}.{1} -- table
               WHERE (category = 'Installed Capacities Public and Industrial Power and CHP Plants by Fuel and Technology_Coal'
                        OR category = 'Installed Capacities Public and Industrial Power and CHP Plants by Fuel and Technology_Oil'
                        OR category = 'Installed Capacities Public and Industrial Power and CHP Plants by Fuel and Technology_Natural gas / non renew.'
                        OR category = 'Installed Capacities Public and Industrial Power and CHP Plants by Fuel and Technology_Nuclear'
                        OR category = 'Installed Capacities Public and Industrial Power and CHP Plants by Fuel and Technology_Waste non renewable'
                        OR category = 'Installed Capacities Public and Industrial Power and CHP Plants by Fuel and Technology_Biomass solid'
                        OR category = 'Installed Capacities Public and Industrial Power and CHP Plants by Fuel and Technology_Biofuel liquid'
                        OR category = 'Installed Capacities Public and Industrial Power and CHP Plants by Fuel and Technology_Hydro'
                        OR category = 'Installed Capacities Public and Industrial Power and CHP Plants by Fuel and Technology_Wind'
                        OR category = 'Installed Capacities Public and Industrial Power and CHP Plants by Fuel and Technology_Solar'
                        OR category = 'Installed Capacities Public and Industrial Power and CHP Plants by Fuel and Technology_Geothermal'
                        OR category = 'Installed Capacities Public and Industrial Power and CHP Plants by Fuel and Technology_Ocean')
                   AND (indicator = 'Heat and Power Unit'
                        OR indicator = 'Combined Cycle'
                        OR indicator = 'CHP'
                        OR indicator = 'Carbon Capture and Storage'
                        OR indicator = 'Steam Turbine'
                        OR indicator = 'Steam Turbine small'
                        OR indicator = 'Steam Turbine large'
                        OR indicator = 'Conventional'
                        OR indicator = 'Gas Turbine old'
                        OR indicator = 'Gas Turbine new'
                        OR indicator = 'Heat and Power Unit small'
                        OR indicator = 'Heat and Power Unit large'
                        OR indicator = 'Run of river'
                        OR indicator = 'Dam <10MW'
                        OR indicator = 'Dam 10-100MW'
                        OR indicator = 'Dam >100MW'
                        OR indicator = 'Pumped Storage <100MW'
                        OR indicator = 'Pumped Storage >100MW'
                        OR indicator = 'CHP old'
                        OR indicator = 'CHP new'
                        OR indicator = 'Fuel cell'
                        OR indicator = 'Generation 2'
                        OR indicator = 'Generation 3'
                        OR indicator = 'Wave'
                        OR indicator = 'Distributed PV'
                        OR indicator = 'Utility PV'
                        OR indicator = 'Offshore'
                        OR indicator = 'Onshore')
                   AND version = 'DataV2'
                   AND year = '2015'
               ORDER BY version, pathway, year; -- sorting  """.format(schema, table_out))
    fix_cost = text("""
               SELECT nid, pathway, version, region, year, category, indicator, value -- column
               FROM {0}.{1} -- table
               WHERE category = 'FixedCost'
                   AND version = 'DataV2'
                   AND year = '2015'
               ORDER BY version, pathway, year; -- sorting  """.format(schema, table_in))
    el_prod = text("""
               SELECT nid, pathway, version, region, year, category, indicator, value -- column
               FROM {0}.{1} -- table
               WHERE (category = 'Electricity Production from Public and Industrial Power and CHP Plants by Fuel and Technology_Coal'
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
                   AND (indicator = 'Heat and Power Unit'
                        OR indicator = 'Combined Cycle'
                        OR indicator = 'CHP'
                        OR indicator = 'Carbon Capture and Storage'
                        OR indicator = 'Steam Turbine'
                        OR indicator = 'Steam Turbine small'
                        OR indicator = 'Steam Turbine large'
                        OR indicator = 'Conventional'
                        OR indicator = 'Gas Turbine old'
                        OR indicator = 'Gas Turbine new'
                        OR indicator = 'Heat and Power Unit small'
                        OR indicator = 'Heat and Power Unit large'
                        OR indicator = 'Run of river'
                        OR indicator = 'Dam <10MW'
                        OR indicator = 'Dam 10-100MW'
                        OR indicator = 'Dam >100MW'
                        OR indicator = 'Pumped Storage <100MW'
                        OR indicator = 'Pumped Storage >100MW'
                        OR indicator = 'CHP old'
                        OR indicator = 'CHP new'
                        OR indicator = 'Fuel cell'
                        OR indicator = 'Generation 2'
                        OR indicator = 'Generation 3'
                        OR indicator = 'Wave'
                        OR indicator = 'Distributed PV'
                        OR indicator = 'Utility PV'
                        OR indicator = 'Offshore'
                        OR indicator = 'Onshore')
                   AND version = 'DataV2'
                   AND year = '2015'
               ORDER BY version, pathway, year; -- sorting  """.format(schema, table_out))
    var_cost = text("""
               SELECT nid, pathway, version, region, year, category, indicator, value -- column
               FROM {0}.{1} -- table
               WHERE category = 'VariableCost'
                   AND version = 'DataV2'
                   AND year = '2015'
               ORDER BY version, pathway, year; -- sorting  """.format(schema, table_in))
    fuel_inp = text("""
               SELECT nid, pathway, version, region, year, category, indicator, value -- column
               FROM {0}.{1} -- table
               WHERE (category = 'Fuel Input to Public and Industrial Power and CHP Plants by Fuel and Technology_Coal'
                        OR category = 'Fuel Input to Public and Industrial Power and CHP Plants by Fuel and Technology_Oil'
                        OR category = 'Fuel Input to Public and Industrial Power and CHP Plants by Fuel and Technology_Natural gas / non renew.'
                        OR category = 'Fuel Input to Public and Industrial Power and CHP Plants by Fuel and Technology_Nuclear'
                        OR category = 'Fuel Input to Public and Industrial Power and CHP Plants by Fuel and Technology_Waste non renewable'
                        OR category = 'Fuel Input to Public and Industrial Power and CHP Plants by Fuel and Technology_Biomass solid'
                        OR category = 'Fuel Input to Public and Industrial Power and CHP Plants by Fuel and Technology_Biofuel liquid'
                        OR category = 'Fuel Input to Public and Industrial Power and CHP Plants by Fuel and Technology_Hydro'
                        OR category = 'Fuel Input to Public and Industrial Power and CHP Plants by Fuel and Technology_Wind'
                        OR category = 'Fuel Input to Public and Industrial Power and CHP Plants by Fuel and Technology_Solar'
                        OR category = 'Fuel Input to Public and Industrial Power and CHP Plants by Fuel and Technology_Geothermal'
                        OR category = 'Fuel Input to Public and Industrial Power and CHP Plants by Fuel and Technology_Ocean')
                   AND (indicator = 'Heat and Power Unit'
                        OR indicator = 'Combined Cycle'
                        OR indicator = 'CHP'
                        OR indicator = 'Carbon Capture and Storage'
                        OR indicator = 'Steam Turbine'
                        OR indicator = 'Steam Turbine small'
                        OR indicator = 'Steam Turbine large'
                        OR indicator = 'Conventional'
                        OR indicator = 'Gas Turbine old'
                        OR indicator = 'Gas Turbine new'
                        OR indicator = 'Heat and Power Unit small'
                        OR indicator = 'Heat and Power Unit large'
                        OR indicator = 'Run of river'
                        OR indicator = 'Dam <10MW'
                        OR indicator = 'Dam 10-100MW'
                        OR indicator = 'Dam >100MW'
                        OR indicator = 'Pumped Storage <100MW'
                        OR indicator = 'Pumped Storage >100MW'
                        OR indicator = 'CHP old'
                        OR indicator = 'CHP new'
                        OR indicator = 'Fuel cell'
                        OR indicator = 'Generation 2'
                        OR indicator = 'Generation 3'
                        OR indicator = 'Wave'
                        OR indicator = 'Distributed PV'
                        OR indicator = 'Utility PV'
                        OR indicator = 'Offshore'
                        OR indicator = 'Onshore')
                   AND version = 'DataV2'
                   AND year = '2015'
               ORDER BY version, pathway, year; -- sorting  """.format(schema, table_out))
    spec_demand = text("""
               SELECT nid, pathway, version, region, year, category, indicator, value -- column
               FROM {0}.{1} -- table
               WHERE category = 'SpecifiedAnnualDemand'
                   AND version = 'DataV2'
                   AND year = '2015'
               ORDER BY version, pathway, year; -- sorting  """.format(schema, table_in))
    el_exchange = text("""
               SELECT nid, pathway, version, region, year, category, indicator, value -- column
               FROM {0}.{1} -- table
               WHERE category = 'Electricity Exchange - Net Imports'
                   AND version = 'DataV2'
                   AND year = '2015'
               ORDER BY version, pathway, year; -- sorting  """.format(schema, table_out))
    
    rawData = pd.read_sql_query(emission, con)
    cap_cost_df = pd.read_sql_query(cap_cost, con)
    new_capa_df = pd.read_sql_query(new_capa, con)
    discount_rate_df = pd.read_sql_query(discount_rate, con)
    oper_life_df = pd.read_sql_query(oper_life, con)
    inst_capa_df = pd.read_sql_query(inst_capa, con)
    fix_cost_df = pd.read_sql_query(fix_cost, con)
    el_prod_df = pd.read_sql_query(el_prod, con)
    var_cost_df = pd.read_sql_query(var_cost, con)
    fuel_inp_df = pd.read_sql_query(fuel_inp, con)
    spec_demand_df = pd.read_sql_query(spec_demand, con)
    el_exchange_df = pd.read_sql_query(el_exchange, con)
    rawData = rawData.append(cap_cost_df, ignore_index = True)
    rawData = rawData.append(new_capa_df, ignore_index = True)
    rawData = rawData.append(discount_rate_df, ignore_index = True)
    rawData = rawData.append(oper_life_df, ignore_index = True)
    rawData = rawData.append(inst_capa_df, ignore_index = True)
    rawData = rawData.append(fix_cost_df, ignore_index = True)
    rawData = rawData.append(el_prod_df, ignore_index = True)
    rawData = rawData.append(var_cost_df, ignore_index = True)
    rawData = rawData.append(fuel_inp_df, ignore_index = True)
    rawData = rawData.append(spec_demand_df, ignore_index = True)
    rawData = rawData.append(el_exchange_df, ignore_index = True)
    
    rawData = rawData.drop(columns = 'version')
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
def co2intensity(rawData, countries, pop_data):
#    rawData = output #for testing
#    pop_data = pop_raw #for testing
    CO2Intensity = pd.DataFrame(columns = ['pathway', 'region', 'year', 'indicator', 'value'])
    emission_data = rawData[rawData['category'] == 'Emissions']
    pathways = emission_data['pathway'].unique().tolist()
    years = emission_data['year'].unique().tolist()
#    emission_data.insert(7, 'population', pd.Series([np.nan]), True)
    for pathway in pathways:
        for country in countries:
            for year in years:
    #            emission_data[(emission_data['pathway']==country) & (emission_data['region']==country)] = pop_data[country].loc[year]
    #            emission_data.loc[(emission_data['region']==country) & (emission_data['year']==year),'population'] = pop_data[country].loc[year]
                value = emission_data.loc[(emission_data['pathway']==pathway) & (emission_data['region']==country) & (emission_data['year']==year),'value'] / pop_data[country].loc[year, 'population']
                CO2Intensity = CO2Intensity.append({"pathway":pathway,"region":country,"year": year, "indicator": "Carbon intensity", "value": value.iloc[0]}, ignore_index = True)
    return CO2Intensity
#%% Calculation of the Discounted Investment per Citizen
def disc_investment():
    Disc_Investment = pd.DataFrame()
    return Disc_Investment
#%% Calculation of Capital Recovery Factor
def crf(rawData):
#    rawData = output #for testing
    req_data = rawData[(rawData['category']=='DiscountRate') | (rawData['category']=='OperationalLife')]
    req_data = req_data.drop_duplicates('indicator')
    req_data = req_data.drop(['pathway', 'region', 'year'], axis=1)
    crf = pd.DataFrame(columns = ['category', 'indicator', 'value'])
    technologies = req_data['indicator'][req_data['category']=='OperationalLife']
    dr = req_data.loc[req_data['category']=='DiscountRate','value']
    for technology in technologies:
        value = (dr.iloc[0]*(1+dr.iloc[0])**req_data.loc[req_data['indicator']==technology,'value'])/((1+dr.iloc[0])**req_data.loc[req_data['indicator']==technology,'value']-1)
        crf = crf.append({"category":'CapitalRecoveryFactor',"indicator":technology,"value":value.iloc[0]}, ignore_index = True)
    return crf
#%% Calculation of the Capital Investment per country, technology and year
def ci():
    rawData = output #for testing
    req_data = rawData[(rawData['category']=='CapitalCost') | (rawData['category'].str.contains('New Capacity_'))]
    cap_cost = [71,74,75,744,76,79,745,80,81,92,94,95,96,97,98,99,100,101,102,103,104,105,106,107,110,111,11,746,113,114,115,116,117,118,119,120,121,125,126,128,129,130,131,132,134,135]
    new_cap = [277,273,274,306,275,244,304,245,246,292,248,249,250,251,252,253,254,255,279,280,281,282,283,284,257,258,259,305,260,261,262,263,264,265,267,268,294,289,290,286,286,286,287,287,270,271]
    ci =pd.DataFrame(columns = ['pathway', 'region', 'year', 'indicator', 'value'])
    pathways = req_data['pathway'].unique().tolist()
    countries = req_data['region'].unique().tolist()
    years = req_data['year'].unique().tolist()
    for pathway in pathways:
        for country in countries:
            for year in years:
                j = 0
                for i in cap_cost:
                    value = req_data.loc[(req_data['pathway']==pathway) & (req_data['region']==country) & (req_data['year']==year) & (req_data['nid']==i), 'value'] * req_data.loc[(req_data['pathway']==pathway) & (req_data['region']==country) & (req_data['year']==year) & (req_data['nid']==new_cap[j]), 'value'] 
                    if not value.empty:
                        ci = ci.append({"pathway":pathway,"region":country,"year":year,"indicator":'CapitalInvestment',"value":value.iloc[0]}, ignore_index = True)
                    j += 1
                    print(j)
            
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
    pop_raw = import_excel(xls,countries)
    
    return raw_data
output = main()
