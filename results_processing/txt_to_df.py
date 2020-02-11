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
        print(parameter)
        # parameter='RateOfActivity' # for testing
        results_dic[parameter] = data[data['Parameter']==parameter]
        df = results_dic[parameter]
        data_expanded = df['rest'].str.split('\t', expand=True)
        data_col = list(data_expanded)
        df = df.drop(['rest'], axis=1)
        for i in data_col:
            df[i] = data_expanded[i]
        df = df.replace('?',np.nan)
        df = df.apply(lambda x: pd.to_numeric(x,errors='ignore'))
        df_info = df.dtypes.value_counts()
        n_txt_col = sum(df_info[1:])
        if n_txt_col==2:
            df.columns = ['Parameter','info_1', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050', '2051', '2052', '2053', '2054', '2055', '2056', '2057', '2058', '2059', '2060']
            df = df.melt(id_vars=['Parameter','info_1'],
                         var_name="year",
                         value_name="value")
        if n_txt_col==3:
            df.columns = ['Parameter','info_1', 'info_2', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050', '2051', '2052', '2053', '2054', '2055', '2056', '2057', '2058', '2059', '2060']
            df = df.melt(id_vars=['Parameter','info_1', 'info_2'],
                         var_name="year",
                         value_name="value")
        if n_txt_col==4:
            df.columns = ['Parameter','info_1', 'info_2', 'info_3', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050', '2051', '2052', '2053', '2054', '2055', '2056', '2057', '2058', '2059', '2060']
            df = df.melt(id_vars=['Parameter','info_1', 'info_2', 'info_3'],
                         var_name="year",
                         value_name="value")
        results_dic[parameter] = df
    return results_dic

sol_txts = get_file_names()

for file in sol_txts:
    metadata = metadata_dic(file)
    data = get_results(file)
    dic_results_df = results_to_dfs(metadata, data)