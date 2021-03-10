# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 11:06:25 2020

@author: haukeh
"""
#%%Import of required packages
import sys
import pandas as pd
import csv
from datetime import datetime
#%% Function to read results from csv
def read_csv(scen):
    df = pd.read_csv('{}/results_csv/ProductionByTechnologyAnnual.csv'.format(scen))
    return df
#%% Filter and format df to needed information
def format_df(df):
    df['country'] = df['TECHNOLOGY'].apply(lambda x: x[:2])
    countries = df['country'].unique()
    df['fuel'] = df['TECHNOLOGY'].apply(lambda x: x[2:4])
    df = df[df['fuel']=='EL']
    df['tech_countr'] = df['TECHNOLOGY'].apply(lambda x : x[4:6])
    df = df[df['tech_countr']!='00']
    df = df[(df['YEAR']==2015)
            |(df['YEAR']==2020)
            |(df['YEAR']==2030)
            |(df['YEAR']==2040)
            |(df['YEAR']==2050)]
    df['fuel_countr'] = df['FUEL'].apply(lambda x: x[:2])
    df['fuel_fuel'] = df['FUEL'].apply(lambda x: x[2:])
    df = df[df['fuel_fuel']=='E1']
    return df, countries
#%%
def build_matrix(df, countries, year):    
    #df = df_formated #for testing
    #year = 2015 #for testing
    df = df[df['YEAR']==year]
    matrix = pd.DataFrame(0, index=countries, columns=countries)
    countries_a = df['country'].unique()
    for country in countries_a:
        #print(country) #for testing
        df_countr = df[df['country']==country]
        countr_con = df_countr['tech_countr'].unique()
        for con in countr_con:
            atob = df_countr['VALUE'][(df_countr['tech_countr']==con)&(df_countr['fuel_countr']==con)]
            if atob.empty:
                matrix.loc[country,con] = 0
            else:
                matrix.loc[country,con] = atob.iloc[0]
            btoa = df_countr['VALUE'][(df_countr['tech_countr']==con)&(df_countr['fuel_countr']==country)]
            if btoa.empty:
                matrix.loc[con,country] = 0
            else:
                matrix.loc[con,country] = btoa.iloc[0]
    return matrix
#%% Main function to execute the script
def main(scen):
    #scen = 'ref' #for testing
    df_raw = read_csv(scen)
    df_formated, countries = format_df(df_raw)
    years_list = list(df_formated['YEAR'].unique())
    years_list.sort()
    date = datetime.today().strftime('%Y-%m-%d')
    for year in years_list:
        exchange_matrix = build_matrix(df_formated, countries, year)
        exchange_matrix.to_csv('OSeMBE_cross-border-el_{}_{}_{}.txt'.format(scen, year, date),
                                sep=' ',
                                float_format='%10.0f',
                                index_label='PJ',
                                quoting=csv.QUOTE_NONE,
                                escapechar=' ')
        total = pd.Series(exchange_matrix.to_numpy().sum())
        total.to_csv('OSeMBE_total-cross-border-el_{}_{}_{}.txt'.format(scen, year, date), header=False, index=False)
#%% Create electricity exchange matrix by executing script and providing scenario name
if __name__ == '__main__':
    scenario = sys.argv[1]
    main(scenario)