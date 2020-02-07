# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 11:22:10 2020

@author: haukeh
"""

import pandas as pd
import numpy as np
import os

def get_file_names():
    sol_txts = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith('.txt'):
                sol_txts.append(file)
    return sol_txts

def get_results(file):
    data = pd.read_csv(file, names=['Year'])
    return data

def metadata_dic(file):
    raw_data = file.split('_')
    metadata = {}
    metadata['model'] = raw_data[0]
    metadata['pathway'] = raw_data[3]
    metadata['date'] = '2019-07-29'
    metadata['data-version'] = 'DataV2'
    metadata['input-output'] = 'Output'
    return metadata

def results_to_dfs(metadata, data):
    results_dic = {}
    data = pd.DataFrame(data.Year.str.split('\t', 2).tolist(), columns = ['Parameter', 'Region', 'rest'])
    data = data.drop(['Region'], axis=1)
    parameters = data['Parameter'].unique()
    for parameter in parameters:
        results_dic[parameter] = data[data['Parameter']==parameter]
        df = results_dic[parameter]
        df = df['rest'].str.split('\t', expand=True)
        results_dic[parameter] = df
    return results_dic

sol_txts = get_file_names()

for file in sol_txts:
    metadata = metadata_dic(file)
    data = get_results(file)