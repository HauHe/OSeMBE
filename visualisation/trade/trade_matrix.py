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
    return df
#%% main

pkl_list = get_file_names()
if len(pkl_list)>1:
    for file in pkl_list:
        print(file)
    pkl_file = input('Please select one of the above listed pkl files to read in by typing its name: ')
else:
    pkl_file = pkl_list[0]
df_raw = get_raw_df(pkl_file)