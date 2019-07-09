
import pandas as pd
import numpy as np
import datetime
import sys

# Print Python and Pandas version

print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)

#%% Get inout for manual runs
results_file = 'OSeMBE_V2.1_sol_C0T0E10_sorted.txt'

#%% Get input on run specifics of the data from command prompt
#Input = sys.argv[1:]
#print(Input)
#results_file = Input[0]

#%%Generate Metadata
name_details_results_file = results_file.split('_')
scenario = name_details_results_file[3] 
date = datetime.date.today().strftime("%Y-%m-%d") 
pathway = name_details_results_file[3]
model = 'OSeMBE' 
framework = 'FrameworkNA' 
version = 'DataV1R1' 
inputoutput = 'Output' 

#%% Definition needed results variables
variables = ['AnnualEmissions', 'AnnualTechnologyEmission', 'ProductionByTechnologyAnnual', 'TotalCapacityAnnual', 'UseByTechnologyAnnual','NewCapacity']

#%% Read the data from txt results file

data = pd.read_csv(results_file, names=['Year']) # The variable results_file needs to be defined in the batch file

# Edditing raw data dataframe 
data = pd.DataFrame(data.Year.str.split('\t', 2).tolist(), columns = ['Parameter', 'Region', 'rest'])
data = data.set_index('Parameter')
data = data.drop(['Region'], axis=1)

# Creating dictionary with one dataframe for each results variable 

variables_dict = {}
for i in variables:
    variables_dict[i] = data.loc[i]

# Filling the dataframes with the variable results

for i in variables:
    df = variables_dict[i]
    df = df['rest'].str.split('\t', expand=True)
    if i == 'AnnualEmissions':
        df.columns = ['Emission', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050', '2051', '2052', '2053', '2054', '2055', '2056', '2057', '2058', '2059', '2060']
        cols = df.columns.drop('Emission')
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
    elif i == 'AnnualTechnologyEmission':
        df.columns = ['Technology', 'Emission', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050', '2051', '2052', '2053', '2054', '2055', '2056', '2057', '2058', '2059', '2060']
        cols = df.columns.drop(['Technology','Emission'])
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
        df['TechCountry'] = df['Technology'].apply(lambda x: x[:2])
        df['TechFuel'] = df['Technology'].apply(lambda x: x[2:4])
    elif i == 'TotalCapacityAnnual':
        df.columns = ['Technology', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050', '2051', '2052', '2053', '2054', '2055', '2056', '2057', '2058', '2059', '2060']
        cols = df.columns.drop('Technology')
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
        df['TechCountry'] = df['Technology'].apply(lambda x: x[:2])
        df['TechFuel'] = df['Technology'].apply(lambda x: x[2:4])
        df['TechTech'] = df['Technology'].apply(lambda x: x[4:6])
        df['TechAge'] = df['Technology'].apply(lambda x: x[7:8])
        df['TechSize'] = df['Technology'].apply(lambda x: x[8:])
    elif i == 'NewCapacity':
        df.columns = ['Technology', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050', '2051', '2052', '2053', '2054', '2055', '2056', '2057', '2058', '2059', '2060']
        cols = df.columns.drop('Technology')
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
        df['TechCountry'] = df['Technology'].apply(lambda x: x[:2])
        df['TechFuel'] = df['Technology'].apply(lambda x: x[2:4])
        df['TechTech'] = df['Technology'].apply(lambda x: x[4:6])
        df['TechAge'] = df['Technology'].apply(lambda x: x[7:8])
        df['TechSize'] = df['Technology'].apply(lambda x: x[8:])
    else:
        df.columns = ['Technology', 'Commodity', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050', '2051', '2052', '2053', '2054', '2055', '2056', '2057', '2058', '2059', '2060']
        cols = df.columns.drop(['Technology','Commodity'])
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
        df['TechCountry'] = df['Technology'].apply(lambda x: x[:2])
        df['TechFuel'] = df['Technology'].apply(lambda x: x[2:4])
        df['TechTech'] = df['Technology'].apply(lambda x: x[4:6])
        df['TechLevel'] = df['Technology'].apply(lambda x: x[6:7])
        df['TechAge'] = df['Technology'].apply(lambda x: x[7:8])
        df['TechSize'] = df['Technology'].apply(lambda x: x[8:])
        df['ComCountry'] = df['Commodity'].apply(lambda x: x[:2])
        df['ComFuel'] = df['Commodity'].apply(lambda x: x[2:4])
    variables_dict[i] = df

#%% Creating dictionary for excel file
file_dict = {}
TableOfContent = pd.Series(['List of tables','','Final energy consumption by energy carrier sum of all sectors','Primary energy consumption','Primary energy consumption of renewables','Installed Capacities Public and Industrial Power and CHP Plants by Fuel and Technology','Electricity Production from Public and Industrial Power and CHP Plants by Fuel and Technology','Fuel Input to Public and Industrial Power and CHP Plants by Fuel and Technology','Electricity Exchange - Net Imports','Electricity Exchange - Capacities','Emissions','Biomass production','New Capacity'])
#%%
df = variables_dict['AnnualTechnologyEmission']
country_series = pd.Series(df.TechCountry.unique())
years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050']
 
#%% List of dictionaries
country_dict_list = []
for j in country_series:
    country_dict_list.append(j+'_dict')
    
for dic in country_dict_list:
    file_dict[dic] = {}
    
#%% Function to extract annual installed capacities

def InstalledCapByFandT(FuAbr, FuNam, TechAbre, TechNam, Age, Size):
    global ID
    global CCS_id
    ID += 1
    FueAndTechs = [FuNam]
    FueAndTechs.extend(TechNam)
    InstalledCap = pd.DataFrame(index=FueAndTechs, columns=['Unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050','ID','Category','Aggregation'])
    Category = ('Installed Capacities Public and Industrial Power and CHP Plants by Fuel and Technology_'+FuNam)
    for tech, nam, age, siz in zip(TechAbre,TechNam,Age,Size):
        if not (age and siz):
            AnnualTechCaps = CountryCaps.loc[(CountryCaps.TechFuel==FuAbr) & (CountryCaps.TechTech==tech)]
        else:
            AnnualTechCaps = CountryCaps.loc[(CountryCaps.TechFuel==FuAbr) & (CountryCaps.TechTech==tech) & (CountryCaps.TechAge==age) & (CountryCaps.TechSize==siz)]

        InstalledCap.set_value(InstalledCap.index, 'Unit', 'GW')
        for yr in years:
            value = AnnualTechCaps[yr].sum()
            InstalledCap.set_value(nam, yr, value)
        if nam != 'Carbon Capture and Storage':
            InstalledCap.set_value(nam, 'ID', ID)
            ID += 1
        else:
            InstalledCap.set_value(nam, 'ID', CCS_id)
            CCS_id += 1
        InstalledCap.set_value(nam, 'Category', Category)
        InstalledCap.set_value(nam, 'Aggregation', 'f')
    for yr in years:
        val = InstalledCap[yr].sum()
        InstalledCap.set_value(FuNam, yr, val)
    FuelID = ID - len(TechNam)
    InstalledCap.set_value(FuNam, 'ID', FuelID)
    InstalledCap.set_value(FuNam, 'Category', Category)
    InstalledCap.set_value(FuNam, 'Aggregation', 't')
    
    return InstalledCap
 
#%% Function to extract annual production by power plant type

def ElProdByFandT(FuAbr, FuNam, TechAbre, TechNam, Age, Size):
    global ID
    global CCS_id
    ID += 1
    FueAndTechs = [FuNam]
    FueAndTechs.extend(TechNam)
    ElProd = pd.DataFrame(index=FueAndTechs, columns=['Unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050','ID','Category','Aggregation'])
    Category = ('Electricity Production from Public and Industrial Power and CHP Plants by Fuel and Technology_'+FuNam)
    for tech, nam, age, siz in zip(TechAbre,TechNam,Age,Size):
        if not (age and siz):
            AnnualTechProd = Country.loc[(Country.TechFuel==FuAbr) & (Country.TechTech==tech)]
        else:
            AnnualTechProd = Country.loc[(Country.TechFuel==FuAbr) & (Country.TechTech==tech) & (Country.TechAge==age) & (Country.TechSize==siz)]

        ElProd.set_value(ElProd.index, 'Unit', 'PJ')
        for yr in years:
            value = AnnualTechProd[yr].sum()
            ElProd.set_value(nam, yr, value)
        if nam != 'Carbon Capture and Storage':
            ElProd.set_value(nam, 'ID', ID)
            ID += 1
        else:
            ElProd.set_value(nam, 'ID', CCS_id)
            CCS_id += 1
        ElProd.set_value(nam, 'Category', Category)
        ElProd.set_value(nam, 'Aggregation', 'f')
    for yr in years:
        val = ElProd[yr].sum()
        ElProd.set_value(FuNam, yr, val)
    FuelID = ID - len(TechNam)
    ElProd.set_value(FuNam, 'ID', FuelID)
    ElProd.set_value(FuNam, 'Category', Category)
    ElProd.set_value(FuNam, 'Aggregation', 't')
    
    return ElProd

#%% Function to calculate the annual fuel input per technology

def FuIntoTe(FuAbr, FuNam, TechAbre, TechNam, Age, Size):
    global ID
    global CCS_id
    ID += 1
    FueAndTechs = [FuNam]
    FueAndTechs.extend(TechNam)
    FuUs = pd.DataFrame(index=FueAndTechs, columns=['Unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050','ID','Category','Aggregation'])
    Category = ('Fuel Input to Public and Industrial Power and CHP Plants by Fuel and Technology_'+FuNam)
    for tech, nam, age, siz in zip(TechAbre,TechNam,Age,Size):
        if not (age and siz):
            AnnualFuUs = FuelUse.loc[(FuelUse.TechFuel==FuAbr) & (FuelUse.TechTech==tech)]
        else:
            AnnualFuUs = FuelUse.loc[(FuelUse.TechFuel==FuAbr) & (FuelUse.TechTech==tech) & (FuelUse.TechAge==age) & (FuelUse.TechSize==siz)]

        FuUs.set_value(FuUs.index, 'Unit', 'PJ')
        for yr in years:
            value = AnnualFuUs[yr].sum()
            FuUs.set_value(nam, yr, value)
        if nam != 'Carbon Capture and Storage':
            FuUs.set_value(nam, 'ID', ID)
            ID += 1
        else:
            FuUs.set_value(nam, 'ID', CCS_id)
            CCS_id += 1
        FuUs.set_value(nam, 'Category', Category)
        FuUs.set_value(nam, 'Aggregation', 'f')
    for yr in years:
        val = FuUs[yr].sum()
        FuUs.set_value(FuNam, yr, val)
    FuelID = ID - len(TechNam)
    FuUs.set_value(FuNam, 'ID', FuelID)
    FuUs.set_value(FuNam, 'Category', Category)
    FuUs.set_value(FuNam, 'Aggregation', 't')
    
    return FuUs

#%% Function to determine the Net Electricity import

def NetElImp(Countr):
    global ID
    countcon1 = pd.Series(TotalTransBorder.TechCountry.unique())
    countcon2 = pd.Series(TotalTransBorder.TechTech.unique())
    countconnect = countcon1.append(countcon2)
    countconnect = pd.Series(countconnect.unique())
    currentcount = Countr[:2]
    countconnect = countconnect.loc[countconnect!=currentcount]
    countconnect = countconnect.reset_index(drop=True)
    exind = country_series.append(pd.Series(['Total net Imports']))
    ElEx = pd.DataFrame(index=exind, columns=['Unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050','ID','Category','Aggregation'])
    Category = ('Electricity Exchange - Net Imports')
    countnr = 0
    
    for coun in country_series:
        if coun == currentcount:
            for yr in years:
                ElEx.set_value(currentcount, yr, 0)
        elif countconnect.str.contains(coun).any():
            ElImport = TotalTransBorder.loc[((TotalTransBorder.TechCountry==countconnect[countnr])|(TotalTransBorder.TechTech==countconnect[countnr])) & (TotalTransBorder.ComCountry==currentcount)]
            ElExport = TotalTransBorder.loc[((TotalTransBorder.TechCountry==countconnect[countnr])|(TotalTransBorder.TechTech==countconnect[countnr])) & (TotalTransBorder.ComCountry==countconnect[countnr])]
            for yr in years:
                net_import = ElImport[yr].sum()-ElExport[yr].sum()
                ElEx.set_value(countconnect[countnr], yr, net_import)
            countnr += 1
        else:
            for yr in years:
                ElEx.set_value(coun, yr, 0)
        
        ElEx.set_value(ElEx.index, 'Unit', 'PJ')
        ElEx.set_value(coun, 'ID', ID)
        ElEx.set_value(coun, 'Category', Category)
        ElEx.set_value(coun, 'Aggregation', 'f')
        ID += 1
    for yr in years:
        value = ElEx[yr].sum()
        ElEx.set_value('Total net Imports', yr, value)
    ElEx.set_value('Total net Imports', 'ID', ID)
    ElEx.set_value('Total net Imports', 'Category', str(Category))
    ElEx.set_value('Total net Imports', 'Aggregation', 't')
    ID += 1
         
    return ElEx

#%% Function to determine the Electricity Exchange - Capacities
    
def ElExCap(Countr):
    global ID
    countcon1 = pd.Series(TotalTransBorder.TechCountry.unique())
    countcon2 = pd.Series(TotalTransBorder.TechTech.unique())
    countconnect = countcon1.append(countcon2)
    countconnect = pd.Series(countconnect.unique())
    currentcount = Countr[:2]
    countconnect = countconnect.loc[countconnect!=currentcount]
    countconnect = countconnect.reset_index(drop=True)
    ExCa = pd.DataFrame(index=country_series, columns=['Unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050','ID','Category','Aggregation'])
    Category = ('Electricity Exchange - Capacities')
    countnr = 0
    
    for coun in country_series:
        if coun == currentcount:
            for yr in years:
                ExCa.set_value(currentcount, yr, 0)
        elif countconnect.str.contains(coun).any():
            TrBoCa = variables_dict['TotalCapacityAnnual'].loc[((variables_dict['TotalCapacityAnnual'].TechCountry==countconnect[countnr])&(variables_dict['TotalCapacityAnnual'].TechFuel=='EL')&(variables_dict['TotalCapacityAnnual'].TechTech==currentcount))|((variables_dict['TotalCapacityAnnual'].TechCountry==currentcount)&(variables_dict['TotalCapacityAnnual'].TechFuel=='EL')&(variables_dict['TotalCapacityAnnual'].TechTech==countconnect[countnr]))]
            for yr in years:
                value = TrBoCa[yr].sum()
                ExCa.set_value(countconnect[countnr], yr, value)
            countnr += 1
        else:
            for yr in years:
                ExCa.set_value(coun, yr, 0)
        
        ExCa.set_value(ExCa.index, 'Unit', 'PJ')
        ExCa.set_value(coun, 'ID', ID)
        ExCa.set_value(coun, 'Category', Category)
        ExCa.set_value(coun, 'Aggregation', 'f')
        ID += 1
         
    return ExCa

#%% Function to determine the national Emissions
    
def NatEmi(Countr):
    global ID
    countr = Countr[:2]
    NatCo2 = pd.DataFrame(index=['CO2'], columns=['Unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050','ID','Category','Aggregation'])
    NaCo2ByTech = variables_dict['AnnualTechnologyEmission'].loc[(variables_dict['AnnualTechnologyEmission'].TechCountry==countr)&(variables_dict['AnnualTechnologyEmission'].Emission=='CO2')]
    NatCo2.set_value(NatCo2.index, 'Unit', 'Mt')
    for yr in years:
        value = NaCo2ByTech[yr].sum()
        NatCo2.set_value('CO2', yr, value)
    NatCo2.set_value('CO2', 'ID', ID)
    NatCo2.set_value('CO2', 'Category', 'Emissions')
    NatCo2.set_value('CO2', 'Aggregation', 't')
    ID += 1
    
    return NatCo2

#%% Function to determine the national Biomass production
    
def NatBMpro(Countr):
    global ID
    NatBM = pd.DataFrame(index=['Other biomass potential (wood, or not spec.)'], columns=['Unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050','ID','Category','Aggregation'])
    BMprod = Country.loc[(Country.TechLevel=='X')&(Country.ComFuel=='BM')]
    NatBM.set_value(NatBM.index, 'Unit', 'PJ')
    for yr in years:
        value = BMprod[yr].sum()
        NatBM.set_value('Other biomass potential (wood, or not spec.)', yr, value)
    NatBM.set_value('Other biomass potential (wood, or not spec.)', 'ID', ID)
    NatBM.set_value('Other biomass potential (wood, or not spec.)', 'Category', 'Biomass production')
    NatBM.set_value('Other biomass potential (wood, or not spec.)', 'Aggregation', 'f')
    ID += 1
    
    return NatBM

#%% Function to determine the New Capacity installed per year
def NewCapByFandT(FuAbr, FuNam, TechAbre, TechNam, Age, Size):
    global ID
    global CCS_id
    ID += 1
    FueAndTechs = [FuNam]
    FueAndTechs.extend(TechNam)
    NewCap = pd.DataFrame(index=FueAndTechs, columns=['Unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050','ID','Category','Aggregation'])
    Category = ('New Capacity_'+FuNam)
    for tech, nam, age, siz in zip(TechAbre,TechNam,Age,Size):
        if not (age and siz):
            AnnualTechCaps = NewCaps.loc[(NewCaps.TechFuel==FuAbr) & (NewCaps.TechTech==tech)]
        else:
            AnnualTechCaps = NewCaps.loc[(NewCaps.TechFuel==FuAbr) & (NewCaps.TechTech==tech) & (NewCaps.TechAge==age) & (NewCaps.TechSize==siz)]

        NewCap.set_value(NewCap.index, 'Unit', 'GW')
        for yr in years:
            value = AnnualTechCaps[yr].sum()
            NewCap.set_value(nam, yr, value)
        if nam != 'Carbon Capture and Storage':
            NewCap.set_value(nam, 'ID', ID)
            ID += 1
        else:
            NewCap.set_value(nam, 'ID', CCS_id)
            CCS_id += 1
        NewCap.set_value(nam, 'Category', Category)
        NewCap.set_value(nam, 'Aggregation', 'f')
    for yr in years:
        val = NewCap[yr].sum()
        NewCap.set_value(FuNam, yr, val)
    FuelID = ID - len(TechNam)
    NewCap.set_value(FuNam, 'ID', FuelID)
    NewCap.set_value(FuNam, 'Category', Category)
    NewCap.set_value(FuNam, 'Aggregation', 't')
    
    return NewCap

#%% Iteration country by country (sheet by sheet)
c = 0 #country number
for count in country_dict_list:
    ID = 1    
    CCS_id = 295
#%% Final energy consumption by energy carrier sum of all sectors
    
    Table = 2
    Country = variables_dict['ProductionByTechnologyAnnual'].loc[(variables_dict['ProductionByTechnologyAnnual'].TechCountry==country_series[c]) & (variables_dict['ProductionByTechnologyAnnual'].ComCountry==country_series[c])]
    TransBorder1 = variables_dict['ProductionByTechnologyAnnual'].loc[(variables_dict['ProductionByTechnologyAnnual'].TechFuel=='EL') & (variables_dict['ProductionByTechnologyAnnual'].TechCountry==country_series[c])& (variables_dict['ProductionByTechnologyAnnual'].ComFuel=='E1')& (variables_dict['ProductionByTechnologyAnnual'].TechTech!='00')]
    TransBorder2 = variables_dict['ProductionByTechnologyAnnual'].loc[(variables_dict['ProductionByTechnologyAnnual'].TechFuel=='EL') & (variables_dict['ProductionByTechnologyAnnual'].TechTech==country_series[c])& (variables_dict['ProductionByTechnologyAnnual'].ComFuel=='E1')]
    TotalTransBorder = TransBorder1
    TotalTransBorder = TotalTransBorder.append(TransBorder2)
    CountryCaps = variables_dict['TotalCapacityAnnual'].loc[(variables_dict['TotalCapacityAnnual'].TechCountry==country_series[c])]
    NewCaps = variables_dict['NewCapacity'].loc[(variables_dict['NewCapacity'].TechCountry==country_series[c])]
    FuelUse = variables_dict['UseByTechnologyAnnual'].loc[(variables_dict['UseByTechnologyAnnual'].TechCountry==country_series[c]) & (variables_dict['UseByTechnologyAnnual'].ComCountry==country_series[c])]
    
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'] = pd.DataFrame(index=['Coal','Petroleum products','Gas','Renewables','Waste','Others (Methanol, Hydrogen, DME)','Sum'], columns=['Unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050','ID','Category','Aggregation'])
    
    #Coal
    Country_Coal = Country.loc[(Country.TechFuel=='CO') & ((Country.ComFuel=='E1') | (Country.ComFuel=='E2'))]
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value(file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].index, 'Unit', 'PJ')
    for yr in years:
        value = Country_Coal[yr].sum()
        file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Coal', yr, value)
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Coal', 'ID', ID)
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Coal', 'Category', TableOfContent[Table])
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Coal', 'Aggregation', 'f')
    ID += 1
    #Petroleum Products
    Country_Petrol = Country.loc[(Country.TechFuel=='HF') & ((Country.ComFuel=='E1') | (Country.ComFuel=='E2'))]
    for yr in years:
        value = Country_Petrol[yr].sum()
        file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Petroleum products', yr, value)
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Petroleum products', 'ID', ID)
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Petroleum products', 'Category', TableOfContent[Table])
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Petroleum products', 'Aggregation', 'f')
    ID += 1
    #Gas
    Country_Gas = Country.loc[(Country.TechFuel=='NG') & ((Country.ComFuel=='E1') | (Country.ComFuel=='E2'))]
    for yr in years:
        value = Country_Gas[yr].sum()
        file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Gas', yr, value)
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Gas', 'ID', ID)
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Gas', 'Category', TableOfContent[Table])
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Gas', 'Aggregation', 'f')
    ID += 1
    #Renewables
    Country_RE = Country.loc[((Country.TechFuel=='BF')|(Country.TechFuel=='BM')|(Country.TechFuel=='GO')|(Country.TechFuel=='HY')|(Country.TechFuel=='OC')|(Country.TechFuel=='SO')|(Country.TechFuel=='WI'))& ((Country.ComFuel=='E1') | (Country.ComFuel=='E2'))]
    for yr in years:
        value = Country_RE[yr].sum()
        file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Renewables', yr, value)
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Renewables', 'ID', ID)
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Renewables', 'Category', TableOfContent[Table])
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Renewables', 'Aggregation', 'f')
    ID += 1
    #Waste
    Country_Waste = Country.loc[(Country.TechFuel=='WS') & ((Country.ComFuel=='E1') | (Country.ComFuel=='E2'))]
    for yr in years:
        value = Country_Waste[yr].sum()
        file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Waste', yr, value)
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Waste', 'ID', ID)
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Waste', 'Category', TableOfContent[Table])
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Waste', 'Aggregation', 'f')
    ID += 1
    #Others
    Country_Other = Country.loc[(Country.TechFuel=='NU') & ((Country.ComFuel=='E1') | (Country.ComFuel=='E2'))]
    for yr in years:
        value = Country_Gas[yr].sum()
        file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Others (Methanol, Hydrogen, DME)', yr, value)
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Others (Methanol, Hydrogen, DME)', 'ID', ID)
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Others (Methanol, Hydrogen, DME)', 'Category', TableOfContent[Table])
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Others (Methanol, Hydrogen, DME)', 'Aggregation', 'f')
    ID += 1
    #Sum
    Country_Sum = Country.loc[((Country.ComFuel=='E1') | (Country.ComFuel=='E2')) & (Country.TechTech!='00')]
    for yr in years:
        value = Country_Sum[yr].sum()
        file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Sum', yr, value)
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Sum', 'ID', ID)
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Sum', 'Category', TableOfContent[Table])
    file_dict[count]['Final energy consumption by energy carrier sum of all sectors'].set_value('Sum', 'Aggregation', 't')
    ID += 1
    Table +=1
    
    #%% Primary energy consumption
    
    file_dict[count]['Primary energy consumption'] = pd.DataFrame(index=['Coal','Oil','Natural gas','Nuclear','Hydro, wind, solar, Ocean','Other renewables','Waste (non renewable)','Electricity import','Sum'], columns=['Unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050','ID','Category','Aggregation'])
    
    # Coal
    Country_Coal = Country.loc[(Country.TechFuel=='CO') & ((Country.TechLevel=='I') | (Country.TechLevel=='X'))]
    file_dict[count]['Primary energy consumption'].set_value(file_dict[count]['Primary energy consumption'].index, 'Unit', 'PJ')
    for yr in years:
        value = Country_Coal[yr].sum()
        file_dict[count]['Primary energy consumption'].set_value('Coal', yr, value)
    file_dict[count]['Primary energy consumption'].set_value('Coal', 'ID', ID)
    file_dict[count]['Primary energy consumption'].set_value('Coal', 'Category', TableOfContent[Table])
    file_dict[count]['Primary energy consumption'].set_value('Coal', 'Aggregation', 'f')
    ID += 1
    # Oil
    Country_Oil = Country.loc[((Country.TechFuel=='OI') |(Country.TechFuel=='HF')) & ((Country.TechLevel=='I') | (Country.TechLevel=='X'))]
    file_dict[count]['Primary energy consumption'].set_value(file_dict[count]['Primary energy consumption'].index, 'Unit', 'PJ')
    for yr in years:
        value = Country_Oil[yr].sum()
        file_dict[count]['Primary energy consumption'].set_value('Oil', yr, value)
    file_dict[count]['Primary energy consumption'].set_value('Oil', 'ID', ID)
    file_dict[count]['Primary energy consumption'].set_value('Oil', 'Category', TableOfContent[Table])
    file_dict[count]['Primary energy consumption'].set_value('Oil', 'Aggregation', 'f')
    ID += 1
    # Natural gas
    Country_Gas = Country.loc[(Country.TechFuel=='NG') & ((Country.TechLevel=='I') | (Country.TechLevel=='X'))]
    file_dict[count]['Primary energy consumption'].set_value(file_dict[count]['Primary energy consumption'].index, 'Unit', 'PJ')
    for yr in years:
        value = Country_Gas[yr].sum()
        file_dict[count]['Primary energy consumption'].set_value('Natural gas', yr, value)
    file_dict[count]['Primary energy consumption'].set_value('Natural gas', 'ID', ID)
    file_dict[count]['Primary energy consumption'].set_value('Natural gas', 'Category', TableOfContent[Table])
    file_dict[count]['Primary energy consumption'].set_value('Natural gas', 'Aggregation', 'f')
    ID += 1
    # Nuclear
    Country_Nuclear = Country.loc[(Country.TechFuel=='UR') & ((Country.TechLevel=='I') | (Country.TechLevel=='X'))]
    file_dict[count]['Primary energy consumption'].set_value(file_dict[count]['Primary energy consumption'].index, 'Unit', 'PJ')
    for yr in years:
        value = Country_Nuclear[yr].sum()
        file_dict[count]['Primary energy consumption'].set_value('Nuclear', yr, value)
    file_dict[count]['Primary energy consumption'].set_value('Nuclear', 'ID', ID)
    file_dict[count]['Primary energy consumption'].set_value('Nuclear', 'Category', TableOfContent[Table])
    file_dict[count]['Primary energy consumption'].set_value('Nuclear', 'Aggregation', 'f')
    ID += 1
    # Hydro, Wind, Solar, Ocean
    Country_RE = Country.loc[(Country.TechFuel=='HY') | (Country.TechFuel=='WI') | (Country.TechFuel=='SO') | (Country.TechFuel=='OC')]
    file_dict[count]['Primary energy consumption'].set_value(file_dict[count]['Primary energy consumption'].index, 'Unit', 'PJ')
    for yr in years:
        value = Country_RE[yr].sum()
        file_dict[count]['Primary energy consumption'].set_value('Hydro, wind, solar, Ocean', yr, value)
    file_dict[count]['Primary energy consumption'].set_value('Hydro, wind, solar, Ocean', 'ID', ID)
    file_dict[count]['Primary energy consumption'].set_value('Hydro, wind, solar, Ocean', 'Category', TableOfContent[Table])
    file_dict[count]['Primary energy consumption'].set_value('Hydro, wind, solar, Ocean', 'Aggregation', 'f')
    ID += 1
    # Other renewables
    Country_OtherRE = Country.loc[((Country.TechFuel=='BF') | (Country.TechFuel=='BM') | (Country.TechFuel=='GO')) & ((Country.TechLevel=='I') | (Country.TechLevel=='X'))]
    file_dict[count]['Primary energy consumption'].set_value(file_dict[count]['Primary energy consumption'].index, 'Unit', 'PJ')
    for yr in years:
        value = Country_OtherRE[yr].sum()
        file_dict[count]['Primary energy consumption'].set_value('Other renewables', yr, value)
    file_dict[count]['Primary energy consumption'].set_value('Other renewables', 'ID', ID)
    file_dict[count]['Primary energy consumption'].set_value('Other renewables', 'Category', TableOfContent[Table])
    file_dict[count]['Primary energy consumption'].set_value('Other renewables', 'Aggregation', 'f')
    ID += 1
    # Waste (non renewable)
    Country_Waste = Country.loc[(Country.TechFuel=='WS') & ((Country.TechLevel=='I') | (Country.TechLevel=='X'))]
    file_dict[count]['Primary energy consumption'].set_value(file_dict[count]['Primary energy consumption'].index, 'Unit', 'PJ')
    for yr in years:
        value = Country_Waste[yr].sum()
        file_dict[count]['Primary energy consumption'].set_value('Waste (non renewable)', yr, value)
    file_dict[count]['Primary energy consumption'].set_value('Waste (non renewable)', 'ID', ID)
    file_dict[count]['Primary energy consumption'].set_value('Waste (non renewable)', 'Category', TableOfContent[Table])
    file_dict[count]['Primary energy consumption'].set_value('Waste (non renewable)', 'Aggregation', 'f')
    ID += 1
    # Electricity import
    ElImport = TotalTransBorder.loc[(TotalTransBorder.ComCountry==country_series[c])]
    ElExport = TotalTransBorder.loc[(TotalTransBorder.ComCountry!=country_series[c])]
    for yr in years:
        net_import = ElImport[yr].sum()-ElExport[yr].sum()
        file_dict[count]['Primary energy consumption'].set_value('Electricity import', yr, net_import)
    file_dict[count]['Primary energy consumption'].set_value('Electricity import', 'ID', ID)
    file_dict[count]['Primary energy consumption'].set_value('Electricity import', 'Category', TableOfContent[Table])
    file_dict[count]['Primary energy consumption'].set_value('Electricity import', 'Aggregation', 'f')
    ID += 1
    # Sum
    Country_Sum = Country.loc[(Country.TechLevel=='I') | (Country.TechLevel=='X')]
    file_dict[count]['Primary energy consumption'].set_value(file_dict[count]['Primary energy consumption'].index, 'Unit', 'PJ')
    for yr in years:
        net_import = ElImport[yr].sum()-ElExport[yr].sum()
        value = Country_Sum[yr].sum()+file_dict[count]['Primary energy consumption'][yr]['Hydro, wind, solar, Ocean']+net_import
        file_dict[count]['Primary energy consumption'].set_value('Sum', yr, value)
    file_dict[count]['Primary energy consumption'].set_value('Sum', 'ID', ID)
    file_dict[count]['Primary energy consumption'].set_value('Sum', 'Category', TableOfContent[Table])
    file_dict[count]['Primary energy consumption'].set_value('Sum', 'Aggregation', 't')
    ID += 1
    
    Table += 1
    
#%% Primary energy consumption by renewables
    
    file_dict[count]['Primary energy consumption of renewables'] = pd.DataFrame(index=['Hydro, Ocean','Solar','Wind','Geothermal','Biomass','Biofuel','Sum'], columns=['Unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050','ID','Category','Aggregation'])
    
    # Hydro, Ocean
    Country_HyOc = Country.loc[(Country.TechFuel=='HY') | (Country.TechFuel=='OC')]
    file_dict[count]['Primary energy consumption of renewables'].set_value(file_dict[count]['Primary energy consumption of renewables'].index, 'Unit', 'PJ')
    for yr in years:
        value = Country_HyOc[yr].sum()
        file_dict[count]['Primary energy consumption of renewables'].set_value('Hydro, Ocean', yr, value)
    file_dict[count]['Primary energy consumption of renewables'].set_value('Hydro, Ocean', 'ID', ID)
    file_dict[count]['Primary energy consumption of renewables'].set_value('Hydro, Ocean', 'Category', TableOfContent[Table])
    file_dict[count]['Primary energy consumption of renewables'].set_value('Hydro, Ocean', 'Aggregation', 'f')
    ID += 1
    # Solar
    Country_HyOc = Country.loc[(Country.TechFuel=='SO')]
    file_dict[count]['Primary energy consumption of renewables'].set_value(file_dict[count]['Primary energy consumption of renewables'].index, 'Unit', 'PJ')
    for yr in years:
        value = Country_HyOc[yr].sum()
        file_dict[count]['Primary energy consumption of renewables'].set_value('Solar', yr, value)
    file_dict[count]['Primary energy consumption of renewables'].set_value('Solar', 'ID', ID)
    file_dict[count]['Primary energy consumption of renewables'].set_value('Solar', 'Category', TableOfContent[Table])
    file_dict[count]['Primary energy consumption of renewables'].set_value('Solar', 'Aggregation', 'f')
    ID += 1
    # Wind
    Country_Wind = Country.loc[(Country.TechFuel=='WI')]
    file_dict[count]['Primary energy consumption of renewables'].set_value(file_dict[count]['Primary energy consumption of renewables'].index, 'Unit', 'PJ')
    for yr in years:
        value = Country_Wind[yr].sum()
        file_dict[count]['Primary energy consumption of renewables'].set_value('Wind', yr, value)
    file_dict[count]['Primary energy consumption of renewables'].set_value('Wind', 'ID', ID)
    file_dict[count]['Primary energy consumption of renewables'].set_value('Wind', 'Category', TableOfContent[Table])
    file_dict[count]['Primary energy consumption of renewables'].set_value('Wind', 'Aggregation', 'f')
    ID += 1
    # Geothermal
    Country_Geo = Country.loc[(Country.TechFuel=='GO') & (Country.ComFuel=='GO')]
    file_dict[count]['Primary energy consumption of renewables'].set_value(file_dict[count]['Primary energy consumption of renewables'].index, 'Unit', 'PJ')
    for yr in years:
        value = Country_Geo[yr].sum()
        file_dict[count]['Primary energy consumption of renewables'].set_value('Geothermal', yr, value)
    file_dict[count]['Primary energy consumption of renewables'].set_value('Geothermal', 'ID', ID)
    file_dict[count]['Primary energy consumption of renewables'].set_value('Geothermal', 'Category', TableOfContent[Table])
    file_dict[count]['Primary energy consumption of renewables'].set_value('Geothermal', 'Aggregation', 'f')
    ID += 1
    # Biomass
    Country_BioM = Country.loc[(Country.TechFuel=='BM') & (Country.ComFuel=='BM')]
    file_dict[count]['Primary energy consumption of renewables'].set_value(file_dict[count]['Primary energy consumption of renewables'].index, 'Unit', 'PJ')
    for yr in years:
        value = Country_BioM[yr].sum()
        file_dict[count]['Primary energy consumption of renewables'].set_value('Biomass', yr, value)
    file_dict[count]['Primary energy consumption of renewables'].set_value('Biomass', 'ID', ID)
    file_dict[count]['Primary energy consumption of renewables'].set_value('Biomass', 'Category', TableOfContent[Table])
    file_dict[count]['Primary energy consumption of renewables'].set_value('Biomass', 'Aggregation', 'f')
    ID += 1
    # Biofuel
    Country_BioF = Country.loc[(Country.TechFuel=='BF')& (Country.ComFuel=='BF')]
    file_dict[count]['Primary energy consumption of renewables'].set_value(file_dict[count]['Primary energy consumption of renewables'].index, 'Unit', 'PJ')
    for yr in years:
        value = Country_BioF[yr].sum()
        file_dict[count]['Primary energy consumption of renewables'].set_value('Biofuel', yr, value)
    file_dict[count]['Primary energy consumption of renewables'].set_value('Biofuel', 'ID', ID)
    file_dict[count]['Primary energy consumption of renewables'].set_value('Biofuel', 'Category', TableOfContent[Table])
    file_dict[count]['Primary energy consumption of renewables'].set_value('Biofuel', 'Aggregation', 'f')
    ID += 1
    # Sum
    Country_Sum = Country.loc[((Country.TechFuel=='BF') & (Country.ComFuel=='BF'))|((Country.TechFuel=='BM') & (Country.ComFuel=='BM'))|((Country.TechFuel=='GO') & (Country.ComFuel=='GO'))|(Country.TechFuel=='WI')|(Country.TechFuel=='SO')|(Country.TechFuel=='OC')|(Country.TechFuel=='HY')]
    file_dict[count]['Primary energy consumption of renewables'].set_value(file_dict[count]['Primary energy consumption of renewables'].index, 'Unit', 'PJ')
    for yr in years:
        value = Country_Sum[yr].sum()
        file_dict[count]['Primary energy consumption of renewables'].set_value('Sum', yr, value)
    file_dict[count]['Primary energy consumption of renewables'].set_value('Sum', 'ID', ID)
    file_dict[count]['Primary energy consumption of renewables'].set_value('Sum', 'Category', TableOfContent[Table])
    file_dict[count]['Primary energy consumption of renewables'].set_value('Sum', 'Aggregation', 'f')
    ID += 1
    
    Table += 1
    
#%% Lists of abbreviations, names, ages, sizes
    
    ListOfFuAbr = ['CO','HF','NG','NU','WS','BM','BF','HY','WI','SO','GO','OC']
    ListOfFuNam = ['Coal','Oil','Natural gas / non renew.','Nuclear','Waste non renewable','Biomass solid','Biofuel liquid','Hydro','Wind','Solar','Geothermal','Ocean']
    
    # Coal
    CoTechAbr = ['CH','CS', 'ST','ST']
    CoTechNam = ['CHP', 'Carbon Capture and Storage', 'Steam Turbine small','Steam Turbine large']
    CoAge = ['H','N','H','H']
    CoSize = ['3','2','1','3']
    # Oil
    HfTechAbr = ['CC','CH','GC','GC','HP','HP','ST','ST']
    HfTechNam = ['Combined Cycle','CHP','Gas Turbine old','Gas Turbine new','Heat and Power Unit small','Heat and Power Unit large','Steam Turbine small','Steam Turbine large']
    HfAge = ['H','H','H','N','H','H','H','H']
    HfSize = ['2','3','3','3','1','2','2','3']
    # Natural gas / non renew.
    NgTechAbr = ['CC','CH','CH','CS','FC','GC','GC','HP','HP','ST']
    NgTechNam = ['Combined Cycle','CHP old','CHP new','Carbon Capture and Storage','Fuel cell','Gas Turbine old','Gas Turbine new','Heat and Power Unit small','Heat and Power Unit large','Steam Turbine']
    NgAge = ['H','H','N','N','H','H','N','H','H','H']
    NgSize = ['2','3','3','2','1','2','2','1','2','2']
    # Nuclear
    NuTechAbr = ['G2','G3']
    NuTechNam = ['Generation 2','Generation 3']
    NuAge = ['','']
    NuSize = ['','']
    # Waste non renewable
    WsTechAbr = ['CH','ST']
    WsTechNam = ['CHP','Steam Turbine']
    WsAge = ['H','H']
    WsSize = ['2','1']
    # Biomass solid
    BmTechAbr = ['CC','CH','CS','ST']
    BmTechNam = ['Combined Cycle','CHP','Carbon Capture and Storage','Steam Turbine']
    BmAge = ['H','H','N','H']
    BmSize = ['1','3','2','3']
    # Biofuel liquid
    BfTechAbr = ['HP']
    BfTechNam = ['Heat and Power Unit']
    BfAge = ['H']
    BfSize = ['1']
    # Hydro
    HyTechAbr = ['DM','DM','DM','DM','DS','DS']
    HyTechNam = ['Run of river','Dam <10MW','Dam 10-100MW','Dam >100MW','Pumped Storage <100MW','Pumped Storage >100MW']
    HyAge = ['H','H','H','H','H','H']
    HySize = ['0','1','2','3','2','3']
    # Wind
    WiTechAbr = ['OF','ON']
    WiTechNam = ['Offshore','Onshore']
    WiAge = ['','']
    WiSize = ['','']
    # Solar
    SoTechAbr = ['DI','UT']
    SoTechNam = ['Distributed PV','Utility PV']
    SoAge = ['H','H']
    SoSize = ['1','2']
    # Geothermal
    GoTechAbr = ['CV']
    GoTechNam = ['Conventional']
    GoAge = ['H']
    GoSize = ['2']
    # Ocean
    OcTechAbr = ['WV']
    OcTechNam = ['Wave']
    OcAge = ['H']
    OcSize = ['1']
    
    ListOfTechAbrByFu = [CoTechAbr, HfTechAbr, NgTechAbr, NuTechAbr, WsTechAbr,BmTechAbr,BfTechAbr,HyTechAbr,WiTechAbr,SoTechAbr,GoTechAbr,OcTechAbr]
    ListOfTechNamByFu = [CoTechNam, HfTechNam, NgTechNam, NuTechNam, WsTechNam,BmTechNam,BfTechNam,HyTechNam,WiTechNam,SoTechNam,GoTechNam,OcTechNam]
    ListOfTechAge = [CoAge, HfAge, NgAge, NuAge, WsAge,BmAge,BfAge,HyAge,WiAge,SoAge,GoAge,OcAge]
    ListOfTechSiz = [CoSize, HfSize, NgSize, NuSize, WsSize,BmSize,BfSize,HySize,WiSize,SoSize,GoSize,OcSize]

#%% Installed Capacities Public and Industrial Power and CHP Plants by Fuel and Technology
    
    file_dict[count]['Installed Capacities Public and Industrial Power and CHP Plants by Fuel and Technology'] = pd.DataFrame(index=[],columns=['Unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050','ID','Category','Aggregation'])    
    for fuabr,funam, techabr, technam, techage, techsize in zip(ListOfFuAbr,ListOfFuNam,ListOfTechAbrByFu,ListOfTechNamByFu,ListOfTechAge,ListOfTechSiz):
        Caps = InstalledCapByFandT(fuabr,funam,techabr,technam,techage,techsize)
        file_dict[count]['Installed Capacities Public and Industrial Power and CHP Plants by Fuel and Technology'] = file_dict[count]['Installed Capacities Public and Industrial Power and CHP Plants by Fuel and Technology'].append(Caps)
    
#%% Electricity Production from Public and Industrial Power and CHP Plants by Fuel and Technology
    
    file_dict[count]['Electricity Production from Public and Industrial Power and CHP Plants by Fuel and Technology'] = pd.DataFrame(index=[],columns=['Unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050','ID','Category','Aggregation'])
    for fuabr,funam, techabr, technam, techage, techsize in zip(ListOfFuAbr,ListOfFuNam,ListOfTechAbrByFu,ListOfTechNamByFu,ListOfTechAge,ListOfTechSiz):
        ElProd = ElProdByFandT(fuabr,funam,techabr,technam,techage,techsize)
        file_dict[count]['Electricity Production from Public and Industrial Power and CHP Plants by Fuel and Technology'] = file_dict[count]['Electricity Production from Public and Industrial Power and CHP Plants by Fuel and Technology'].append(ElProd)
   
#%% Fuel Input to Public and Industrial Power and CHP Plants by Fuel and Technology','Electricity Exchange - Net Imports
    file_dict[count]['Fuel Input to Public and Industrial Power and CHP Plants by Fuel and Technology'] = pd.DataFrame(index=[],columns=['Unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050','ID','Category','Aggregation'])
    for fuabr,funam, techabr, technam, techage, techsize in zip(ListOfFuAbr,ListOfFuNam,ListOfTechAbrByFu,ListOfTechNamByFu,ListOfTechAge,ListOfTechSiz):
        FueUse = FuIntoTe(fuabr,funam,techabr,technam,techage,techsize)
        file_dict[count]['Fuel Input to Public and Industrial Power and CHP Plants by Fuel and Technology'] = file_dict[count]['Fuel Input to Public and Industrial Power and CHP Plants by Fuel and Technology'].append(FueUse)

#%% Electricity Exchange - Net Imports
    
    file_dict[count]['Electricity Exchange - Net Imports'] = pd.DataFrame(index=[],columns=['Unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050','ID','Category','Aggregation'])    
    NeElIm = NetElImp(count)
    file_dict[count]['Electricity Exchange - Net Imports'] = file_dict[count]['Electricity Exchange - Net Imports'].append(NeElIm)
    
#%% Electricity Exchange - Capacities
    
    file_dict[count]['Electricity Exchange - Capacities'] = pd.DataFrame(index=[],columns=['Unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050','ID','Category','Aggregation'])    
    TranBorCap = ElExCap(count)
    file_dict[count]['Electricity Exchange - Capacities'] = file_dict[count]['Electricity Exchange - Capacities'].append(TranBorCap)
    
#%% Emissions
    
    file_dict[count]['Emissions'] = pd.DataFrame(index=[],columns=['Unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050','ID','Category','Aggregation'])    
    NatiEmis = NatEmi(count)
    file_dict[count]['Emissions'] = file_dict[count]['Emissions'].append(NatiEmis)
    
#%% Biomass production
    
    file_dict[count]['Biomass production'] = pd.DataFrame(index=[],columns=['Unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050','ID','Category','Aggregation'])    
    NatiBMprod = NatBMpro(count)
    file_dict[count]['Biomass production'] = file_dict[count]['Biomass production'].append(NatiBMprod)
    
#%% New Capacities
    file_dict[count]['New Capacity'] = pd.DataFrame(index=[],columns=['Unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050','ID','Category','Aggregation'])    
    for fuabr,funam, techabr, technam, techage, techsize in zip(ListOfFuAbr,ListOfFuNam,ListOfTechAbrByFu,ListOfTechNamByFu,ListOfTechAge,ListOfTechSiz):
        Caps = NewCapByFandT(fuabr,funam,techabr,technam,techage,techsize)
        file_dict[count]['New Capacity'] = file_dict[count]['New Capacity'].append(Caps)

#%% Adding CCS
    
#%%
    c += 1
    
#%% Creating "Tables" sheet/dictionary

file_dict['Tables'] = TableOfContent

#%% Creating the sheet "EU28+CH+NO"
file_dict['EU28+CH+NO'] = file_dict[country_dict_list[0]].copy()
columns = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050']
for table in TableOfContent[2:]:
    for count in country_dict_list[1:]:
        file_dict['EU28+CH+NO'][table] = file_dict['EU28+CH+NO'][table].add(file_dict[count][table], fill_value=0)
    file_dict['EU28+CH+NO'][table]['Unit'] = file_dict[country_dict_list[0]][table].loc[:,'Unit']
    file_dict['EU28+CH+NO'][table]['ID'] = file_dict[country_dict_list[0]][table].loc[:,'ID']
    file_dict['EU28+CH+NO'][table]['Category'] = file_dict[country_dict_list[0]][table].loc[:,'Category']
    file_dict['EU28+CH+NO'][table].loc[:,'Aggregation'] = 't'
file_dict['EU28+CH+NO']['Electricity Exchange - Net Imports'].loc[:,['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050']] = file_dict['EU28+CH+NO']['Electricity Exchange - Net Imports'].loc[:,['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050']] * (-1)
file_dict['EU28+CH+NO']['Electricity Exchange - Net Imports'].loc['Total net Imports',['Unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050','ID','Category','Aggregation']] = np.NaN
#%% 
xlsxName = date
xlsxName += str('_'+pathway+'_'+model+'_'+framework+'_'+version+'_'+inputoutput+'.xlsx')

#%% Write excel file

writer = pd.ExcelWriter(xlsxName, engine='xlsxwriter')
dfs = TableOfContent[2:13].reset_index(drop=True)
col_headers = pd.DataFrame(['Unit','2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050','ID','Category','Aggregation']).T

file_dict['Tables'].to_excel(writer, sheet_name='Tables', header=False, index=False)

# All countries sheet
firstrow = 8
for df in dfs:

    file_dict['EU28+CH+NO'][df].to_excel(writer, sheet_name='EU+CH+NO', startrow=firstrow, header=False )
    worksheet = writer.sheets['EU+CH+NO']   
    worksheet.write_string((firstrow-1), 0, df)
    firstrow += len(file_dict['EU28+CH+NO'][df].index)+1

worksheet.write_string(0, 0,'Scenario')
worksheet.write_string(1, 0,'Date')
worksheet.write_string(2, 0,'Model')
worksheet.write_string(0, 1,scenario)
worksheet.write_string(1, 1, date)
worksheet.write_string(2, 1, model)
worksheet.write_string(5, 0, 'EU28+CH+NO')
worksheet.write_string(3, 38, 'For database')
col_headers.to_excel(writer, sheet_name='EU+CH+NO', startrow=5, startcol=1, header=False, index=False)

# Country sheets
c = 0
for countr in country_dict_list:
    firstrow = 8

    for df in dfs:
    
        file_dict[countr][df].to_excel(writer, sheet_name=countr[:2], startrow=firstrow, header=False )
        worksheet = writer.sheets[countr[:2]]    
        worksheet.write_string((firstrow-1), 0, df)
        firstrow += len(file_dict[countr][df].index)+1
    
    worksheet.write_string(0, 0,'Scenario')
    worksheet.write_string(1, 0,'Date')
    worksheet.write_string(2, 0,'Model')
    worksheet.write_string(0, 1,scenario)
    worksheet.write_string(1, 1, date)
    worksheet.write_string(2, 1, model)
    worksheet.write_string(5, 0, countr[:2])
    worksheet.write_string(3, 38, 'For database')
    col_headers.to_excel(writer, sheet_name=countr[:2], startrow=5, startcol=1, header=False, index=False)

writer.save()
