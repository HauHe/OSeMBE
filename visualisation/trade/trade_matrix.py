# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 11:06:25 2020

@author: haukeh
"""

#Import of required packages
import os
import pandas as pd
import read_pkl

#%%
def get_file_names():
    pkl_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith('.pkl'):
                pkl_files.append(file)
    return pkl_files

def get_raw_df(file):
    # file = 'OSeMBE_ProductionByTechnologyAnnual_DataV3R1_2020-03-24.pkl'
    df = read_pkl.read_pickle_file(file)
    df['fuel'] = df['info_1'].apply(lambda x: x[2:4])    
    df = df[df['fuel']=='EL']
    df['tech_countr'] = df['info_1'].apply(lambda x : x[4:6])
    df = df[df['tech_countr']!='00']
    df = df[(df['year']=='2015')
            |(df['year']=='2020')
            |(df['year']=='2030')
            |(df['year']=='2040')
            |(df['year']=='2050')]
    df['country'] = df['info_1'].apply(lambda x: x[:2])
    df['fuel_countr'] = df['info_2'].apply(lambda x: x[:2])
    df['fuel_fuel'] = df['info_2'].apply(lambda x: x[2:])
    df = df[df['fuel_fuel']=='E1']
    return df

def build_matrix(df, path, year):
    # df = df_raw #for development, hashout after  or delete
    # path = path_sel #for development, hashout after  or delete
    # year = year_sel #for development, hashout after  or delete
    
    df = df[(df['year']==year)&(df['pathway']==path)]
    countries = df['fuel_countr'].unique()
    matrix = pd.DataFrame(0, index=countries, columns=countries)
    countries_a = df['country'].unique()
    for country in countries_a:
        # country = 'AT' #for development, hashout after  or delete
        df_countr = df[df['country']==country]
        countr_con = df_countr['tech_countr'].unique()
        for con in countr_con:
            # con = 'CZ' #for development, hashout after  or delete
            atob = df_countr['value'][(df_countr['tech_countr']==con)&(df_countr['fuel_countr']==con)]
            matrix.loc[country,con] = atob.iloc[0]
            btoa = df_countr['value'][(df_countr['tech_countr']==con)&(df_countr['fuel_countr']==country)]
            matrix.loc[con,country] = btoa.iloc[0]
    return matrix
#%% main

pkl_list = get_file_names()
if len(pkl_list)>1:
    for file in pkl_list:
        print(file)
    pkl_file = input('Please select one of the above listed pkl files to read in by typing its name: ')
else:
    pkl_file = pkl_list[0]
df_raw = get_raw_df(pkl_file)
for path in df_raw['pathway'].unique():
    print(path)
path_sel = input('Please select one of the above listed scenarios by typing its name: ')
for year in df_raw['year'].unique():
    print(year)
year_sel= input('Please select one of the above listed years to generate the electricitr exchange matrix for:')

exchange_matrix = build_matrix(df_raw, path_sel, year_sel)