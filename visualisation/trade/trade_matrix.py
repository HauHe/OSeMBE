# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 11:06:25 2020

@author: haukeh
"""

#Import of required packages
import os
import pandas as pd
import read_pkl
import csv

#%%
def get_file_names():
    pkl_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith('.pkl'):
                pkl_files.append(file)
    return pkl_files

def get_raw_df(file):
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
    df = df[(df['year']==year)&(df['pathway']==path)]
    countries = df['fuel_countr'].unique()
    matrix = pd.DataFrame(0, index=countries, columns=countries)
    countries_a = df['country'].unique()
    for country in countries_a:
        df_countr = df[df['country']==country]
        countr_con = df_countr['tech_countr'].unique()
        for con in countr_con:
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
path_list = list(df_raw['pathway'].unique())
# for path in df_raw['pathway'].unique():
#     print(path)
# path_sel = input('Please select one of the above listed scenarios by typing its name: ')
years_list = list(df_raw['year'].unique())
# for year in df_raw['year'].unique():
#     print(year)
# year_sel= input('Please select one of the above listed years to generate the electricitr exchange matrix for:')

for path in path_list:
    for year in years_list:
        exchange_matrix = build_matrix(df_raw, path, year)
        exchange_matrix.to_csv('OSeMBE_cross-border-el_{}_{}_{}.txt'.format(path, year, pd.to_datetime('today').strftime("%Y-%m-%d")),
                               sep=' ',
                               float_format='%10.0f',
                               index_label='PJ',
                               quoting=csv.QUOTE_NONE,
                               escapechar=' ')