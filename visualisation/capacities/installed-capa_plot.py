# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 16:35:17 2020

@author: haukeh
"""
#%%Import of required packages
import numpy as np
import pandas as pd
import sys
import plotly.graph_objs as go
from plotly.offline import plot
#%% function to read a results csv for given scneario and parameter
def read_csv(scen, param):
    df = pd.read_csv('{}/results_csv/{}.csv'.format(scen,param))
    df['pathway'] = scen
    return df
#%%function to create a dictionary of dictionaries for each scenario containing dfs for the result parameter
def build_dic(scens, params):
    dic = {}
    for scen in scens:
        dic[scen] = {}
    for scen in scens:
        for param in params:
            dic[scen][param] = read_csv(scen, param)
    return dic
#%% function to shape df as needed for figure generation
def build_TAC_df(dic):
    df = pd.DataFrame(columns=['REGION','TECHNOLOGY','YEAR','VALUE','pathway'])
    for i in dic:
        df_work = dic[i]['TotalCapacityAnnual']
        df = df.append(df_work)    
    df['region'] = df['TECHNOLOGY'].apply(lambda x: x[:2])
    df['fuel'] = df['TECHNOLOGY'].apply(lambda x: x[2:4])
    df['tech_type'] = df['TECHNOLOGY'].apply(lambda x: x[4:6])
    df['tech_spec'] = df['TECHNOLOGY'].apply(lambda x: x[2:])
    df = df[((df['fuel']!='EL')&(df['fuel']!='OI')) & (df['tech_type']!='00')]
    df['unit'] = 'GW'
    return df
#%% function generating a dictionary with information on the model
def get_facts(df):
    facts_dic = {}
    facts_dic['pathways'] = df.loc[:,'pathway'].unique()
    facts_dic['regions'] = df.loc[:,'region'].unique()
    facts_dic['unit'] = df.loc[:, 'unit'].unique()
    facts_dic['regions'] = np.append(facts_dic['regions'],'EU28')
    return facts_dic
#%% function generating the figure
def create_fig(df_exp, country,paths,colours):
    fig = go.Figure()
    years = ['2015','2020','2030','2040','2050']
    countries = {'AT':'Austria','BE':'Belgium','BG':'Bulgaria','CH':'Switzerland','CY':'Cyrpus','CZ':'Czech Republic','DE':'Germany','DK':'Denmark','EE':'Estonia','ES':'Spain','FI':'Finland','FR':'France','GR':'Greece','HR':'Croatia','HU':'Hungary','IE':'Ireland','IT':'Italy','LT':'Lithuania','LU':'Luxembourg','LV':'Latvia','MT':'Malta','NL':'Netherlands','NO':'Norway','PL':'Poland','PT':'Portugal','RO':'Romania','SE':'Sweden','SI':'Slovenia','SK':'Slovakia','UK':'United Kingdom','EU28':'EU28'}
    fuel_short = pd.DataFrame({'fuel_name':['WI','HY','BF','CO','BM','WS','HF','NU','NG','OC','OI','GO','SO','EL'],'fuel_abr':['Wind','Hydro','Biofuel','Coal','Biomass','Waste','Oil','Nuclear','Gas','Ocean','Oil','Geo','Solar','Imports']}, columns = ['fuel_name','fuel_abr'])
    fuel_short = fuel_short.sort_values(['fuel_name'])
    df_sel_year = df_exp[(df_exp['YEAR']==int(years[0]))
                  |(df_exp['YEAR']==int(years[1]))
                  |(df_exp['YEAR']==int(years[2]))
                  |(df_exp['YEAR']==int(years[3]))
                  |(df_exp['YEAR']==int(years[4]))]
    info_dict = {}
    info_dict['Unit'] = df_sel_year.loc[:,'unit'].unique()
    info_dict['Y-Axis'] = ['{}'.format(*info_dict['Unit'])]
    dict_path = {}
    for j in paths:
        df = df_sel_year[df_sel_year['pathway']==j]
        if country == 'EU28':
            df = df[(df['region']=='AT')
                   |(df['region']=='BE')
                   |(df['region']=='BG')
                   |(df['region']=='CY')
                   |(df['region']=='CZ')
                   |(df['region']=='DE')
                   |(df['region']=='DK')
                   |(df['region']=='EE')
                   |(df['region']=='ES')
                   |(df['region']=='FI')
                   |(df['region']=='FR')
                   |(df['region']=='GR')
                   |(df['region']=='HR')
                   |(df['region']=='HU')
                   |(df['region']=='IE')
                   |(df['region']=='IT')
                   |(df['region']=='LT')
                   |(df['region']=='LU')
                   |(df['region']=='LV')
                   |(df['region']=='MT')
                   |(df['region']=='NL')
                   |(df['region']=='PL')
                   |(df['region']=='PT')
                   |(df['region']=='RO')
                   |(df['region']=='SE')
                   |(df['region']=='SI')
                   |(df['region']=='SK')
                   |(df['region']=='UK')]
            df.drop('info_1',axis=1, inplace=True)
            df.drop('region',axis=1, inplace=True)
            techs = df['tech_spec'].unique()
            df_p = pd.DataFrame(index=years, columns=techs)
            for year in years:
                for tech in techs:
                    df_p.loc[year, tech] = df.loc[(df['YEAR']==int(year))&(df['tech_spec']==tech), 'VALUE'].sum()
            df_by_com = pd.DataFrame()
            coms = fuel_short['fuel_name']
            coms = coms[(coms!='EL')&(coms!='OI')]
            for com in coms:    
                com_selec = df_p.filter(regex="\A"+com, axis=1)
                com_sum = com_selec.sum(axis=1)
                df_by_com[com] = com_sum
            dict_path[j] = df_by_com
        else:
            df = df[df['region'] == country]
            df_p = df.pivot(index='YEAR', columns='tech_spec',  values='VALUE')
            techs = list(df_p)
            df_by_com = pd.DataFrame()
            coms = fuel_short['fuel_name']
            coms = coms[(coms!='EL')&(coms!='OI')]
            for com in coms:    
                com_selec = df_p.filter(regex="\A"+com, axis=1)
                com_sum = com_selec.sum(axis=1)
                df_by_com[com] = com_sum
            dict_path[j] = df_by_com
    df_blend = pd.DataFrame(columns=coms)
    path_ind =[]
    year_ind =[]
    for year in years:
        i = 0
        for j in paths:                
            df_blend = df_blend.append(dict_path[j].loc[int(year)])
            path_ind.append(paths[i].upper())
            year_ind.append(year)
            i += 1
    df_blend = df_blend.set_index([pd.Index(path_ind, name='paths')],append=True)
    for i in coms:
        temp = fuel_short.loc[fuel_short['fuel_name']==i,'fuel_abr']
        fuel_code = temp.iloc[0]
        fig.add_trace(go.Bar(
            y = df_blend.loc[:,i],
            x = [year_ind,path_ind],
            name=fuel_code,
            # hoverinfo='x+y',
            hovertemplate=
            'Capacity: %{y}GW',
            marker_color=colours[fuel_code]
            ))
    fig.update_layout(
        barmode='stack',
        plot_bgcolor='rgba(0,0,0,0)',
        title={
            'text':'Installed power generation capacities in {}'.format(countries[country]),
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis = {'type': 'multicategory'},
        yaxis = dict(title='Installed power capacity [{}]'.format(info_dict['Y-Axis'][0])),
        font_family = "Arial",
        font_color = "black"
        )
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='Black')
    return fig, df_p
#%% Dictionary of dictionaries with colour schemes
colour_schemes = dict(
    dES_colours = dict(
        Coal = 'rgb(0, 0, 0)',
        Oil = 'rgb(121, 43, 41)',
        Gas = 'rgb(86, 108, 140)',
        Nuclear = 'rgb(186, 28, 175)',
        Waste = 'rgb(138, 171, 71)',
        Biomass = 'rgb(172, 199, 119)',
        Biofuel = 'rgb(79, 98, 40)',
        Hydro = 'rgb(0, 139, 188)',
        Wind = 'rgb(143, 119, 173)',
        Solar = 'rgb(230, 175, 0)',
        Geo = 'rgb(192, 80, 77)',
        Ocean ='rgb(22, 54, 92)',
        Imports = 'rgb(232, 133, 2)'),
    TIMES_PanEU_colours = dict(
        Coal = 'rgb(0, 0, 0)',
        Oil = 'rgb(202, 171, 169)',
        Gas = 'rgb(102, 77, 142)',
        Nuclear = 'rgb(109, 109, 109)',
        Waste = 'rgb(223, 134, 192)',
        Biomass = 'rgb(80, 112, 45)',
        Biofuel = 'rgb(178, 191, 225)',
        Hydro = 'rgb(181, 192, 224)',
        Wind = 'rgb(103, 154, 181)',
        Solar = 'rgb(210, 136, 63)',
        Geo = 'rgb(178, 191, 225)',
        Ocean ='rgb(178, 191, 225)',
        Imports = 'rgb(232, 133, 2)')
    )
#%% main function to execute the script
def main(selec_region,scens):
    params = ['TotalCapacityAnnual']
    results_dic = build_dic(scens, params)
    df_TAC = build_TAC_df(results_dic)
    facts_dic = get_facts(df_TAC)
    for region in facts_dic['regions']:
        print(region)
    # selec_region = input('Please select a country from the above listed by typing here:')
    print(list(colour_schemes.keys()))
    # selec_scheme = input('Please select one of the above listed colour schemes by writing it here and confirming by enter:')
    selec_scheme = 'dES_colours' 
    colours = colour_schemes[selec_scheme]
    figure, table = create_fig(df_TAC, selec_region,scens,colours)
    plot(figure)
#%% If executed as script
if __name__ == '__main__':
    selec_region = sys.argv[1]
    scens = sys.argv[2:]
    main(selec_region,scens)