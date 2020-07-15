# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#Import of needed packages
import plotly as py
import plotly.figure_factory as ff
import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html

import numpy as np

#%% generate table to ilustrate
data = [['', 'Emma', 'Isabella', 'Ava', 'Olivia', 'Sophia', 'row-sum'],
        ['Emma', 16, 3, 28, 0, 18, 65],
        ['Isabella', 18, 0, 12, 5, 29, 64],
        ['Ava', 9, 11, 17, 27, 0, 64],
        ['Olivia', 19, 0, 31, 11, 12, 73],
        ['Sophia', 23, 17, 10, 0, 34, 84]]

table = ff.create_table(data, index=True)

#%% 

matrix = np.array([[16,  3, 28,  0, 18],
                 [18,  0, 12,  5, 29],
                 [ 9, 11, 17, 27,  0],
                 [19,  0, 31, 11, 12],
                 [23, 17, 10,  0, 34]], dtype=int)

def check_data(data_matrix):
    L, M=data_matrix.shape
    if L!=M:
        raise ValueError('Data array must have (n, n) shape')
    return L

L = check_data(matrix)

#%% Dash app
app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=table)
])

#%% Call Dash app

app.run_server(debug=True, use_reloader=False) #Turn off reloader if inside Jupyter