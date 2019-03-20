import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output

import ast
import pandas as pd
import time as t

#Loading the data
data = pd.read_csv("E:\Semester-2\DIVA\Project\Development\sample_data.csv")
data['module'] = data['file'].apply(lambda x : ast.literal_eval(x)['project'])
data['timestamp'] = pd.to_datetime(data.timestamp)

#Initiation for live data
start_time = pd.Timestamp('2019-02-25 00:12:00')
time = start_time
downloads = 0
packages = []

# pip install pyorbital
from pyorbital.orbital import Orbital
satellite = Orbital('TERRA')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('TERRA Satellite Live Feed'),
        html.Div(id='live-download'),
        html.Div(id='live-download1'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])
)


@app.callback(Output('live-download', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Longitude: {0:.2f}'.format(lon), style=style),
        #html.Span('Latitude: {0:.2f}'.format(lat), style=style),
        #html.Span('Altitude: {0:0.2f}'.format(alt), style=style)
    ]

@app.callback(Output('live-download1', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    global time
    global downloads
    global packages
    old_time = time
    new_time = time + pd.Timedelta(seconds = 2)
    temp_data = data[(data['timestamp'] > old_time) & (data['timestamp'] <= new_time)]
    downloads += temp_data.shape[0]
    rate = temp_data.shape[0]/2
    packages.extend(list(set(temp_data['module'])))
    packages = list(set(packages))
    #print('Unique Packages :', len(packages))
    #print("Downloads : ", downloads)
    #print("Rate : ", rate)
    time = new_time

    style = {'padding': '5px', 'fontSize': '16px'}

    return [
        html.Span(downloads, style=style)
    ]


if __name__ == '__main__':
    app.run_server(debug=True)