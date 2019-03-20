#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:18:33 2019

@author: Hauke Henke
"""

import pandas as pd
import numpy as np
import datetime
import sys

# Print Python and Pandas version

print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)

#%% Definition of to be used file and naming details -- to be changed later

ddFileName = "OSeMBE_V1_C0T0E0_data.txt"
ddFileInfo = ddFileName.split("_")
pathway = ddFileInfo[2]
date = datetime.date.today().strftime("%Y-%m-%d")

#%% Import data input file

inputData = pd.read_table(ddFileName)

for i in inputData:
    inputData = inputData[i].str.split(" ", expand = True)

#%% Determine Technologies in model    
technologies = inputData.iloc[10]
technologies = technologies.drop([0,1,2], axis=0)
technologies = technologies[:-1]
technologies = technologies.reset_index(drop = True)

#%% Determine countries in model

allCountries = technologies.str[:2]
allCountries = pd.Series(allCountries.unique())
#%% Determine years of interest

yearsOfInterest = inputData.iloc[9]
yearsOfInterest = yearsOfInterest[3:39]
yearsOfInterest = yearsOfInterest.reset_index(drop = True)

#%% parameter wanted in excel file

paraToExtract = ["AnnualEmissionLimit", "AvailabilityFactor", "CapitalCost", "DiscountRate", "EmissionActivityRatio", "FixedCost", "InputActivityRatio", "OperationalLife", "OutputActivityRatio", "ResidualCapacity", "SpecifiedAnnualDemand", "TotalAnnualMaxCapacityInvestment", "TotalTechnologyAnnualActivityLowerLimit", "TotalTechnologyAnnualActivityUpperLimit", "VariableCost"]
ThreeDParam = ["AnnualEmissionLimit", "AvailabilityFactor", "CapitalCost", "FixedCost", "ResidualCapacity", "SpecifiedAnnualDemand", "TotalAnnualMaxCapacityInvestment", "TotalTechnologyAnnualActivityLowerLimit", "TotalTechnologyAnnualActivityUpperLimit"]
#%%Identifying the first row of every parameter in the data file
startOfParam = inputData[inputData[0].str.contains("param")]
startOfParam = startOfParam.index.tolist()

#Creating a list of all parameter in data file
allParam = []
for param in startOfParam:
    allParam.append(str(inputData.iloc[param,1]))

#creating a list containing dictionaries for every paramter
allParamDic = {}
for p in allParam:
    allParamDic[p] = {}

#Filling the parameter dictionaries with the corresponding data from the inputData
for param in range(len(allParam)):
    if param<len(allParam)-1:
        allParamDic[allParam[param]] = inputData.iloc[startOfParam[param]:startOfParam[param+1]-1]
    else:
        allParamDic[allParam[param]] = inputData.iloc[startOfParam[param]:-3]

#%% Modifying the dfs of the parameter of interest
columnHeader = ['0']
for i in yearsOfInterest:
    columnHeader.append(i)
for d in ThreeDParam:
    allParamDic[d] = allParamDic[d].iloc[:,0:37]
    allParamDic[d].columns = columnHeader
    allParamDic[d] = allParamDic[d].drop(allParamDic[d].index[[0,1,2]])
    allParamDic[d] = allParamDic[d].reset_index(drop = True)
#%%
paramDic = {}
for p in paraToExtract:
    paramDic[p] = {}
    
test = {'eins', 'zwei'}
for param in range(len(paraToExtract)):
    paramDic[paraToExtract[param]] = inputData.iloc[startOfParam[param]:startOfParam[param+1]-1]
#for para in startOfParam:
    