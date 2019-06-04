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

#%% Get input from comand prompt/batch run
Input = sys.argv[1:]
#Input = ['OSeMBE_V1_C0T0E1_data.txt', 0, 0, 1]
print(Input)
ddFileName = Input[0]
RECapCoScen = Input[1]
RECapCoScen = int(RECapCoScen)
TransmissionScen = Input[2]
TransmissionScen = int(TransmissionScen)
EmissionScen = Input[3]
EmissionScen = int(EmissionScen)
name_details_dd_file = ddFileName.split('_')
pathway = name_details_dd_file[2] 
date = datetime.date.today().strftime("%Y-%m-%d") 
pathway = 'C%iT%iE%s' % (RECapCoScen, TransmissionScen, EmissionScen)
model = 'OSeMBE' 
framework = 'FrameworkNA' 
version = 'Data'+name_details_dd_file[1] 
inputoutput = 'Input'
#%% Definition of to be used file and naming details -- to be changed later

#ddFileName = "OSeMBE_V1_C0T0E0_data.txt"
#ddFileInfo = ddFileName.split("_")
#pathway = ddFileInfo[2]
#date = datetime.date.today().strftime("%Y-%m-%d")
#model = 'OSeMBE'
#framework = 'FrameworkNA'
#version = 'Data'+ddFileInfo[1]
#inputoutput = 'Input'
#%% Import data input file

#inputData = pd.read_table(ddFileName)
inputData = pd.read_csv(ddFileName, sep='\t')

for i in inputData:
    inputData = inputData[i].str.split(" ", expand = True)
    
#%% Create df for SETs
sets = inputData.iloc[:12]

#%% Determine Technologies in model    
technologies = sets[sets[1]=='TECHNOLOGY'].squeeze()
technologies = technologies.drop([0,1,2], axis=0)
technologies = technologies[:-1]
technologies = technologies.reset_index(drop = True)

#%% Determine countries in model

allCountries = technologies.str[:2]
allCountries = pd.Series(allCountries.unique())
allSheetsForXsl = pd.Series('EU+CH+NO')
allSheetsForXsl = allSheetsForXsl.append(allCountries, ignore_index = True)

#%% Determine years of interest

yearsOfInterest = sets[sets[1]=='YEAR'].squeeze()
yearsOfInterest = yearsOfInterest[3:39]
yearsOfInterest = yearsOfInterest.reset_index(drop = True)

#%% parameter wanted in excel file
availableTech = ['BF00I00','BF00X00','BFHPFH1','BM00I00','BM00X00','BMCCPH1','BMCHPH3','BMSTPH3','CO00I00','CO00X00','COCHPH3','COSTPH1','COSTPH3','EL00TD0','ELDKPH1','ELFRPH1','ELLUPH1','ELNLPH1','ELNOPH1','ELPLPH1','ELSEPH1','ELXXPH1','GO00X00','GOCVPH2','HF00I00','HFCCPH2','HFCHPH3','HFGCPH3','HFGCPN3','HFHPFH1','HFHPPH2','HFSTPH2','HFSTPH3','HYDMPH0','HYDMPH1','HYDMPH2','HYDMPH3','HYDSPH2','HYDSPH3','NG00I00','NG00X00','NGCCPH2','NGCHPH3','NGCHPN3','NGFCFH1','NGGCPH2','NGGCPN2','NGHPFH1','NGHPPH2','NGSTPH2','NUG2PH3','NUG3PH3','OCWVPH1','OI00I00','OI00X00','OIRFPH0','SODIFH1','SOUTPH2','UR00I00','WIOFPH3','WIOFPN2','WIOFPN3','WIONPH3','WIONPN3','WS00X00','WSCHPH2','WSSTPH1']
availableTechNames = ['Bio fuel Import','Bio fuel Generation','Bio fuel ICE Heat and Power unit','Biomass Import','Biomass Extraction','Biomass Combined Cycle','Biomass Combined Heat and Power','Biomass Steam Turbine','Coal Import','Coal Extraction','Coal Combined Heat and Power','Coal Steam Turbine small','Coal Steam Turbine large','Domestic Transmission and Distribution','Trans-border transmission with neighbour 1','Trans-border transmission with neighbour 2','Trans-border transmission with neighbour 3','Trans-border transmission with neighbour 4','Trans-border transmission with neighbour 5','Trans-border transmission with neighbour 6','Trans-border transmission with neighbour 7','Trans-border transmission with neighbour 8','Geothermal Extraction','Geothermal Conventional','HFO Import','HFO Combined Cycle','HFO Combined Heat and Power','HFO Gas Turbine old','HFO Gas Turbine new','HFO ICE Heat and Power unit small','HFO ICE Heat and Power Unit large','HFO Steam Turbine small','HFO Steam Turbine large','Hydro Run of river','Hydro Dam <10MW','Hydro Dam 10-100MW','Hydro Dam >100MW','Hydro Pumped Storage 10-100MW','Hydro Pumped Storage >100MW','Natural Gas Import','Natural Gas Extraction','Natural Gas Combined Cycle','Natural Gas Combined Heat and Power old','Natural Gas Combined Heat and Power new','Natural Gas Fuel Cell','Natural Gas Gas Turbine old','Natural Gas Gas Turbine new','Natural Gas ICE Heat and Power unit small','Natural Gas ICE Heat and Power Unit large','Natural Gas Steam Turbine','Nuclear Generation 2','Nuclear Generation 3','Ocean Wave','Oil Import','Oil Extraction','Oil Refinery','Solar Distributed solar PV <=0.1MW','Solar Utility solar PV >0.1MW','Uranium Import','Wind Offshore Current','Wind Offshore Near-term','Wind Offshore Long-term','Wind Onshore Current','Wind Onshore Near-term','Waste Extraction','Waste Combined Heat and Power','Waste Steam Turbine']
demands = ['Electricity']
emissions = ['CO2']
none = ['none']
nanSeries = pd.Series([np.nan])
paraToExtract = ["AnnualEmissionLimit", "AvailabilityFactor", "CapitalCost", "DiscountRate", "EmissionActivityRatio", "FixedCost", "InputActivityRatio", "OperationalLife", "OutputActivityRatio", "ResidualCapacity", "SpecifiedAnnualDemand", "TotalAnnualMaxCapacityInvestment", "TotalTechnologyAnnualActivityLowerLimit", "TotalTechnologyAnnualActivityUpperLimit", "VariableCost"]
paraForExSheets = {"AnnualEmissionLimit":'kton', "AvailabilityFactor":'none', "CapitalCost":'M$/GW', "DiscountRate":'none', 'Efficiency':'none',"EmissionActivityRatio":'kt/PJ', "FixedCost":'M$/GW', "OperationalLife":'yr', "ResidualCapacity":'GW', "SpecifiedAnnualDemand":'PJ', "TotalAnnualMaxCapacityInvestment":'GW', "TotalTechnologyAnnualActivityLowerLimit":'PJ', "TotalTechnologyAnnualActivityUpperLimit":'PJ', "VariableCost":'M$/PJ'}
ThreeDParam = ["AnnualEmissionLimit", "AvailabilityFactor", "CapitalCost", "FixedCost", "ResidualCapacity", "SpecifiedAnnualDemand", "TotalAnnualMaxCapacityInvestment", "TotalTechnologyAnnualActivityLowerLimit", "TotalTechnologyAnnualActivityUpperLimit"]
FourDParam = ['VariableCost']
FiveDParam = ["EmissionActivityRatio","InputActivityRatio","OutputActivityRatio"]
nonTechSpecParam = ["AnnualEmissionLimit", "DiscountRate", "SpecifiedAnnualDemand"]
paramToSum = ["ResidualCapacity", "SpecifiedAnnualDemand", "TotalTechnologyAnnualActivityLowerLimit"]
paramNonEu = ["AvailabilityFactor", "CapitalCost", "EmissionActivityRatio", "FixedCost", 'Efficiency', "OperationalLife", "TotalAnnualMaxCapacityInvestment","TotalTechnologyAnnualActivityUpperLimit", "VariableCost"]
paramToXsl = pd.Series(["AnnualEmissionLimit", "AvailabilityFactor", "CapitalCost", "DiscountRate", "Efficiency", "EmissionActivityRatio", "FixedCost", "OperationalLife", "ResidualCapacity", "SpecifiedAnnualDemand", "TotalAnnualMaxCapacityInvestment", "TotalTechnologyAnnualActivityLowerLimit", "TotalTechnologyAnnualActivityUpperLimit", "VariableCost"])
techSpecParam = ["AvailabilityFactor", "CapitalCost", "Efficiency", "EmissionActivityRatio", "FixedCost", "OperationalLife", "ResidualCapacity", "SpecifiedAnnualDemand", "TotalAnnualMaxCapacityInvestment", "TotalTechnologyAnnualActivityLowerLimit", "TotalTechnologyAnnualActivityUpperLimit", "VariableCost"]
ThreeDtechSpec = ["AvailabilityFactor","CapitalCost", "FixedCost", "ResidualCapacity", "TotalAnnualMaxCapacityInvestment", "TotalTechnologyAnnualActivityLowerLimit", "TotalTechnologyAnnualActivityUpperLimit"]
generalValidParam = ['AnnualEmissionLimit', 'DiscountRate']
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

#%% Modifying the dfs of the parameter of interest with 3 dimensions
columnHeader = ['0']
for i in yearsOfInterest:
    columnHeader.append(i)
for d in ThreeDParam:
    allParamDic[d] = allParamDic[d].iloc[:,0:37]
    allParamDic[d].columns = columnHeader
    allParamDic[d] = allParamDic[d].drop(allParamDic[d].index[[0,1,2]])
    allParamDic[d] = allParamDic[d].reset_index(drop = True)
    allParamDic[d]["countryTech"] = allParamDic[d]["0"].apply(lambda x: x[:2])
    allParamDic[d]["techTech"] = allParamDic[d]["0"].apply(lambda x: x[2:])
#%% Modifying the dfs of the parameter of interest with 4 dimensions (Variable Cost)
for d in FourDParam:
    allParamDic[d] = allParamDic[d].iloc[:,0:37]
    allParamDic[d].columns = columnHeader
    allParamDic[d] = allParamDic[d].drop(allParamDic[d].index[[0]])
    allParamDic[d] = allParamDic[d][allParamDic[d]["0"] != '2015']
    df = allParamDic[d].iloc[0::2, :]
    df = df.iloc[:,:1]
    df = df['0'].str.split(',',n=-1,expand = True)
    df = df.iloc[:,1:2]
    df = df.reset_index(drop = True)
    df.columns = ['technology']
    allParamDic[d] = allParamDic[d].iloc[1::2,1:]
    allParamDic[d] = allParamDic[d].reset_index(drop = True)
    allParamDic[d] = allParamDic[d].join(df)
    allParamDic[d]['countryTech'] = allParamDic[d]["technology"].apply(lambda x: x[:2])
    allParamDic[d]['techTech'] = allParamDic[d]["technology"].apply(lambda x: x[2:])
#%% Modifying the dfs of the parameter of interest with 5 dimensions
for d in FiveDParam:
    allParamDic[d] = allParamDic[d].iloc[:,0:37]
    allParamDic[d].columns = columnHeader
    allParamDic[d] = allParamDic[d].drop(allParamDic[d].index[[0]])
    allParamDic[d] = allParamDic[d][allParamDic[d]["0"] != '2015']
    df = allParamDic[d].iloc[0::2, :]
    df = df.iloc[:,:1]
    df = df['0'].str.split(',',n=-1,expand = True)
    df = df.iloc[:,1:3]
    df = df.reset_index(drop = True)
    df.columns = ['technology', 'commodity']
    allParamDic[d] = allParamDic[d].iloc[1::2,1:]
    allParamDic[d] = allParamDic[d].reset_index(drop = True)
    allParamDic[d] = allParamDic[d].join(df)
    allParamDic[d]['countryTech'] = allParamDic[d]["technology"].apply(lambda x: x[:2])
    allParamDic[d]['techTech'] = allParamDic[d]["technology"].apply(lambda x: x[2:])
    allParamDic[d]['countryComm'] = allParamDic[d]["commodity"].apply(lambda x: x[:2])
#%% Creating a df with the CapacityToActivityUnit
cToA = allParamDic['CapacityToActivityUnit']
cToA = cToA.iloc[1:]
cToA = cToA.T
cToA.iloc[:,1] = cToA.iloc[:,1].shift(-1)
cToA = cToA.iloc[:-4]
cToA['country'] = cToA.iloc[:,0].apply(lambda x: x[:2])
cToA['tech'] = cToA.iloc[:,0].apply(lambda x: x[2:])
cToA = cToA[cToA['country']=='DE']
cToA = cToA.reset_index(drop = True)
cToA = cToA.append({3534: 1,'tech':np.nan}, ignore_index=True)
powerGenTech = cToA[cToA.iloc[:,1]=='31.536']
#%% Create dictionary with dictionaries for each modelled country
fileDic = {}
for c in allCountries:
    fileDic[c] = {}

#%% Function to create dfs for country and technology specific parameter
def CreateParamDf(Country, Parameter):
    global availableTech
    global availableTechNames
    outDf = pd.DataFrame()
    sourceDf = allParamDic[Parameter][allParamDic[Parameter]['countryTech']==Country]    
    if sourceDf.empty == False:
        for t in availableTech:
            count = 0
            count = sourceDf['techTech'].str.contains(t).sum()
            if count > 0:
                outDf = outDf.append(sourceDf[sourceDf['techTech']==t])
            else:
                outDf = outDf.append(pd.Series([np.nan]), ignore_index = True)
        outDf = outDf.drop([0], axis=1)
        outDf = outDf.drop(["0"], axis=1)
        outDf = outDf.drop(["countryTech"], axis=1)
        outDf.index = availableTechNames
        outDf.insert(loc=0,column='Unit',value=np.nan)
        outDf['Unit'] = paraForExSheets[Parameter]
        if Parameter == 'VariableCost':
            for t in outDf['powerGenTech']:
                outDf.loc[outDf['techTech']==t,'Unit']='M$/GWh'
        outDf = outDf.drop(["techTech"], axis=1)
    return outDf
#%% Filter the VariableCost
def CreateVarCoDf(Country):
    global availableTech
    global availableTechNames
    outDf = pd.DataFrame()
    variCost = allParamDic['VariableCost'][allParamDic['VariableCost']['countryTech']==Country]
    for t in availableTech:
        count = 0
        count = variCost['techTech'].str.contains(t).sum()
        if count > 0:
            outDf = outDf.append(variCost[variCost['techTech']==t])
        else:
            outDf = outDf.append(pd.Series([np.nan]), ignore_index = True)
    outDf = outDf.drop([0], axis=1)
    outDf = outDf.loc[:,'2015':'2050']
    outDf.index = availableTechNames
    outDf.insert(loc=0,column='Unit',value=np.nan)
    outDf['Unit'] = paraForExSheets['VariableCost']
    return outDf
#%% Calculate the technolgy efficiencies
def CreateEfficDf(Country):
    global availableTech
    global availableTechNames
    outDf = pd.DataFrame()
    inputActivities = allParamDic['InputActivityRatio'][(allParamDic['InputActivityRatio']['countryTech']==Country) & (allParamDic['InputActivityRatio']['countryComm']==Country)]
    outputActivities = allParamDic['OutputActivityRatio'][(allParamDic['OutputActivityRatio']['countryTech']==Country) & (allParamDic['OutputActivityRatio']['countryComm']==Country)]
    for t in availableTech:
        inCount = 0
        outCount = 0
        inCount= inputActivities['techTech'].str.contains(t).sum()
        outCount = outputActivities['techTech'].str.contains(t).sum()
        if inCount > 0 and outCount > 0:
            inA = inputActivities[inputActivities['techTech']==t]
            inA = inA.loc[:,'2015':'2050']
            inA = inA.astype(float)
            outA = outputActivities[outputActivities['techTech']==t]
            outA = outA.loc[:,'2015':'2050']
            outA = outA.astype(float)
            outDf = outDf.append(outA.div(inA.sum()).reset_index(drop=True))
        elif outCount > 0:
            outA = outputActivities[outputActivities['techTech']==t]
            outA = outA.loc[:,'2015':'2050']
            outA = outA.astype(float)
            outDf = outDf.append(outA)
        else:
            outDf = outDf.append(pd.Series([np.nan]), ignore_index = True)
    outDf = outDf.drop([0], axis=1)
    outDf.index = availableTechNames
    outDf.insert(loc=0,column='Unit',value=np.nan)
    outDf['Unit'] = paraForExSheets['Efficiency']
    return outDf
#%% Filter the EmissionActivityRatios
def CreateEmiDf(Country):
    global availableTech
    global availableTechNames
    outDf = pd.DataFrame()
    emiActRat = allParamDic['EmissionActivityRatio'][(allParamDic['EmissionActivityRatio']['countryTech']==Country) & (allParamDic['EmissionActivityRatio']['countryComm']=='CO')]
    for t in availableTech:
        count = 0
        count = emiActRat['techTech'].str.contains(t).sum()
        if count > 0:
            outDf = outDf.append(emiActRat[emiActRat['techTech']==t])
        else:
            outDf = outDf.append(pd.Series([np.nan]), ignore_index = True)
    outDf = outDf.loc[:,'2015':'2050']
    outDf.index = availableTechNames
    outDf.insert(loc=0,column='Unit',value=np.nan)
    outDf['Unit'] = paraForExSheets['EmissionActivityRatio']
    return outDf
#%% Extract the OperationalLife
def OpeLifDf(Country):
    global availableTech
    global availableTechNames
    outDf = pd.DataFrame()
    allLifeTimes = pd.DataFrame()
    rawCountryLifeTimes =pd.DataFrame()
    opeLif = allParamDic['OperationalLife']
    allTech = opeLif.iloc[1,:1631]
    opeLif = opeLif.iloc[2,1:1632]
    opeLif = opeLif.reset_index(drop = True)
    allLifeTimes = allLifeTimes.append(opeLif)
    allLifeTimes = allLifeTimes.append(allTech)
    allLifeTimes = allLifeTimes.transpose()
    allLifeTimes.columns = ['LifeTime','Technology']
    allLifeTimes.loc[1630,'Technology'] = 'UKWSSTPH1'
    allLifeTimes['countryTech'] = allLifeTimes["Technology"].apply(lambda x: x[:2])
    allLifeTimes['techTech'] = allLifeTimes["Technology"].apply(lambda x: x[2:])
    countryLifeTimes = allLifeTimes[allLifeTimes["countryTech"]==Country]
    for t in availableTech:
        count = 0
        count = countryLifeTimes['techTech'].str.contains(t).sum()
        if count > 0:
            rawCountryLifeTimes = rawCountryLifeTimes.append(countryLifeTimes[countryLifeTimes['techTech']==t])
        else:
            rawCountryLifeTimes = rawCountryLifeTimes.append(pd.Series([np.nan]), ignore_index = True)
    for y in yearsOfInterest:
        outDf[y] = rawCountryLifeTimes['LifeTime']
    outDf.index = availableTechNames
    outDf.insert(loc=0,column='Unit',value=np.nan)
    outDf['Unit'] = paraForExSheets['OperationalLife']
    return outDf
#%% filling the country dictionaries with the country and technology specific parameter data
for c in allCountries:
    for p in ThreeDtechSpec:
        fileDic[c][p] = CreateParamDf(c,p)
#%% Adding the efficiencies to the country dictionaries
for c in allCountries:
    fileDic[c]['Efficiency'] = CreateEfficDf(c)
#%% Adding the EmissionActivityRatios to the country dictionaries
for c in allCountries:
    fileDic[c]['EmissionActivityRatio'] = CreateEmiDf(c)
#%% Adding the VariableCosts to the country dictionaries
for c in allCountries:
    fileDic[c]['VariableCost'] = CreateVarCoDf(c)
#%% Adding the SpecifiedAnnualDemand to the country dictionaries
for c in allCountries:
    fileDic[c]['SpecifiedAnnualDemand'] = allParamDic['SpecifiedAnnualDemand'][allParamDic['SpecifiedAnnualDemand']['countryTech']==c]
    fileDic[c]['SpecifiedAnnualDemand'] = fileDic[c]['SpecifiedAnnualDemand'].loc[:,'2015':'2050']
    fileDic[c]['SpecifiedAnnualDemand'].index = demands
    fileDic[c]['SpecifiedAnnualDemand'].insert(loc=0,column='Unit',value=np.nan)
    fileDic[c]['SpecifiedAnnualDemand']['Unit'] = paraForExSheets['SpecifiedAnnualDemand']
#%% Add (empty) dfs for AnnualEmissionLimit to country dictionaries
for c in allCountries:
    fileDic[c]['AnnualEmissionLimit'] = pd.DataFrame()
#%% Add the AnnualEmissionLimit to the EU+CH+NO dictionary
fileDic['EU+CH+NO'] = {}
fileDic['EU+CH+NO']['AnnualEmissionLimit'] = allParamDic['AnnualEmissionLimit'][allParamDic['AnnualEmissionLimit']['countryTech']=='CO']
fileDic['EU+CH+NO']['AnnualEmissionLimit'] = fileDic['EU+CH+NO']['AnnualEmissionLimit'].loc[:,'2015':'2050']
fileDic['EU+CH+NO']['AnnualEmissionLimit'].index = emissions
fileDic['EU+CH+NO']['AnnualEmissionLimit'].insert(loc=0,column='Unit',value=np.nan)
fileDic['EU+CH+NO']['AnnualEmissionLimit']['Unit'] = paraForExSheets['AnnualEmissionLimit']
#%% Adding the OperationalLife to the country dictionaries
for c in allCountries:
    fileDic[c]['OperationalLife'] = OpeLifDf(c)
#%% Add (empty) dfs for DiscountRate to the country dictionaries
for c in allCountries:
    fileDic[c]['DiscountRate'] = pd.DataFrame(np.nan, index=['none'], columns=['unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050'])
#%% Add (empty) dfs for AnnualEmissionLimit to the country dictionaries
for c in allCountries:
    fileDic[c]['AnnualEmissionLimit'] = pd.DataFrame(np.nan, index=['none'], columns=['unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050'])
#%% Add the DiscountRate to the EU+CH+NO dictionary
df = allParamDic['DiscountRate'].iloc[1,1]
outDf = pd.DataFrame()
for y in yearsOfInterest:
    outDf.loc[1,y] = df
dRs = ['DiscountRate']
outDf.index = dRs
outDf.insert(loc=0,column='Unit',value=np.nan)
outDf['Unit'] = paraForExSheets['DiscountRate']
fileDic['EU+CH+NO']['DiscountRate'] = outDf
#%% Add (empty) Dataframes to EU dictionary for parameter that are not relevant/sumable
for p in paramNonEu:
    fileDic['EU+CH+NO'][p] = pd.DataFrame()
#%% Sum of country parameter dataframes for EU dictionaries
for p in paramToSum:
    outDf = pd.DataFrame()
    for c in allCountries:
        df = fileDic[c][p]
        if df.empty == False:
            df[yearsOfInterest] = df[yearsOfInterest].apply(pd.to_numeric, errors='coerce')
            if outDf.empty == False:
                outDf[yearsOfInterest] = outDf[yearsOfInterest].add(df[yearsOfInterest], fill_value=0)
            else:
                outDf = df.copy()
    fileDic['EU+CH+NO'][p] = outDf
#%% Adding index to empty dataframes
for c in allSheetsForXsl:
    for p in techSpecParam:
        if fileDic[c][p].empty == True:
            df = pd.DataFrame(np.nan, index=availableTechNames, columns=['unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050'])
            fileDic[c][p] = df
    if fileDic[c]['AnnualEmissionLimit'].empty == True:
        df = pd.DataFrame(np.nan, index=['CO2'], columns=['unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050'])
        fileDic[c][p] = df
    if fileDic[c]['DiscountRate'].empty == True:
        df = pd.DataFrame(np.nan, index=['DiscountRate'], columns=['unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050'])
        fileDic[c][p] = df
#%% Adding information for database to country dataframes
for c in allCountries:
    ID = 1
    for p in paramToXsl:
        if len(fileDic[c][p]) < 2:
            if p != 'SpecifiedAnnualDemand':
                fileDic[c][p].loc['none','id'] = ID
                fileDic[c][p].loc['none','category'] = p
                fileDic[c][p].loc['none','aggregation'] = 'f'
                ID +=1
            else:
                fileDic[c][p].loc['Electricity','id'] = ID
                fileDic[c][p].loc['Electricity','category'] = p
                fileDic[c][p].loc['Electricity','aggregation'] = 'f'
                ID += 1
        else:
            for i in availableTechNames:
                    fileDic[c][p].loc[i,'id'] = ID
                    fileDic[c][p].loc[i,'category'] = p
                    fileDic[c][p].loc[i,'aggregation'] = 'f'
                    ID +=1
#%% Adding information for database to EU dataframe
ID = 1
for p in paramToXsl: 
    if len(fileDic['EU+CH+NO'][p]) < 2:
        if p != 'SpecifiedAnnualDemand':
            fileDic['EU+CH+NO'][p]['id'] = ID
            fileDic['EU+CH+NO'][p]['category'] = p
            fileDic['EU+CH+NO'][p]['aggregation'] = 'f'
            ID +=1
        else:
            fileDic['EU+CH+NO'][p]['id'] = ID
            fileDic['EU+CH+NO'][p]['category'] = p
            fileDic['EU+CH+NO'][p]['aggregation'] = 't'
            ID +=1
    else:
        for t in availableTechNames:
            fileDic['EU+CH+NO'][p].loc[t,'id'] = ID
            fileDic['EU+CH+NO'][p].loc[t,'category'] = p
            fileDic['EU+CH+NO'][p].loc[t,'aggregation'] = 't'
            ID +=1
#%% Dataframe for Tables Sheet
df = pd.Series(['List of tables',''])
df = df.append(paramToXsl)
tables = df
#%% xlsx file name

xlsxName = date
xlsxName += str('_'+pathway+'_'+model+'_'+framework+'_'+version+'_'+inputoutput+'.xlsx')
#%%
writer = pd.ExcelWriter(xlsxName, engine='xlsxwriter')
col_headers = pd.DataFrame(['unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050','ID','Category','Aggregation']).T

tables.to_excel(writer, sheet_name='Tables', header=False, index=False)

for c in allSheetsForXsl:
    firstrow = 8

    for p in paramToXsl:
        fileDic[c][p].to_excel(writer, sheet_name=c, startrow=firstrow, header=False )
        worksheet = writer.sheets[c]    
        worksheet.write_string((firstrow-1), 0, p)
        firstrow += len(fileDic[c][p].index)+1

    worksheet.write_string(0, 0,'Scenario')
    worksheet.write_string(1, 0,'Date')
    worksheet.write_string(2, 0,'Model')
    worksheet.write_string(0, 1,pathway)
    worksheet.write_string(1, 1, date)
    worksheet.write_string(2, 1, model)
    worksheet.write_string(5, 0, c)
    worksheet.write_string(3, 38, 'For database')
    col_headers.to_excel(writer, sheet_name=c, startrow=5, startcol=1, header=False, index=False)
    
writer.save()