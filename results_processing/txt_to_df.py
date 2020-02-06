# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 11:22:10 2020

@author: haukeh
"""

import pandas as pd
import numpy as np
import os

sol_txts = []
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith('.txt'):
            sol_txts.append(file)

for file in sol_txts:
    raw_data = file.split('_')
    metadata = {}
    metadata['model'] = raw_data[0]
    metadata['pathway'] = raw_data[3]
    metadata['date'] = '2019-07-29'
    metadata['data-version'] = 'DataV2'
    metadata['input-output'] = 'Output'
    
    data = pd.read_csv(file, names=['Year'])
