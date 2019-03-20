import dash
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output

from components.header import Header

import time as t
import ast
import pandas as pd


#Loading the data
data = pd.read_csv("E:/Semester-2/DIVA/Project/Development/sample_data.csv")
data['module'] = data['file'].apply(lambda x : ast.literal_eval(x)['project'])
data['timestamp'] = pd.to_datetime(data.timestamp)

app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True

#### TAB1 ######
##################################
main =  html.Div([html.Br(),
            html.Div(id = 'count_download', 
                style = {'width' : '29%', 'height': '90','backgroundColor' : '#5108af', 'marginLeft' : '2%'}, className = 'column'),

            html.Div(id = 'rate_download', 
                style = {'width' : '29%',  'height': '90','backgroundColor' : '#0bbf4d'}, className = 'column'),

            html.Div(id = 'uniq_package'
                , style = {'width' : '29%', 'height': '90','backgroundColor' : '#edc423'}, className = 'column'),
            
            dcc.Interval(
                id='interval-component',
                interval=1*1000, # in milliseconds
                n_intervals=0
            )
], className = 'MainTab')













#### TAB2 ######
##################################

historical = html.Div('historical',
    className = 'Hist-Tab')


#### TAB3 ######
##################################
trends = html.Div('trends')



#### TAB4 ######
##################################
ref = html.Div('references')



#### TAB5 ######
##################################
aboutus = html.Div('about us')



## No Page Error
noPage = html.Div([  # 404

    html.P(["404 Page not found"])

    ], className="no-page")


# app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     html.Div(id='page-content')
# ])

tabs_styles = {
    'height': '44px'
}
tab_style = {
    #'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    #'fontWeight': 'bold'
}

tab_selected_style = {
    #'borderTop': '1px solid #d6d6d6',
    #'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#ffb014',
    'color': 'white',
    'padding': '6px'
}

app.layout = html.Div([
    Header(),
    
    dcc.Tabs(id="tabs-styled-with-inline", value='main', children=[
        dcc.Tab(label='Live Data', value='main', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Historical Data', value='historical', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Interesting Trends', value='trends', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='References', value='ref', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='About Us', value='aboutus', style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles),
    html.Div(id='tabs-content-inline')
])

# Update page
# # # # # # # # #


@app.callback(Output('tabs-content-inline', 'children'),
              [Input('tabs-styled-with-inline', 'value')])
def render_content(tab):
    if tab == 'main':
        return main
    elif tab == 'historical':
        return historical
    elif tab == 'trends':
        return trends
    elif tab == 'ref':
        return ref
    elif tab == 'aboutus':
        return aboutus
    else:
        return noPage

###########################
########### TAB1 #################
###########################

#Initiation for live data
start_time = pd.Timestamp('2019-02-25 00:12:00')
time = start_time
downloads = 0

@app.callback(Output('count_download', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    global time
    global downloads
    old_time = time
    new_time = time + pd.Timedelta(seconds = 1)
    temp_data = data[(data['timestamp'] > old_time) & (data['timestamp'] <= new_time)]
    downloads += temp_data.shape[0]
    time = new_time
    return [html.H4(str(downloads), style = {'color': 'white', 'textAlign': 'center' }),
                    html.P("Number of Downloads", style = {'textAlign': 'center', 'color' : 'white'})
                    ]

#Initiation for live data
start_time = pd.Timestamp('2019-02-25 00:12:00')
time2 = start_time

@app.callback(Output('rate_download', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics2(n):
    global time2
    old_time = time2
    new_time = time2 + pd.Timedelta(seconds = 1)
    temp_data = data[(data['timestamp'] > old_time) & (data['timestamp'] <= new_time)]
    rate = temp_data.shape[0]
    time2 = new_time
    return [html.H4(str(rate), style = {'color': 'white', 'textAlign': 'center' }),
                    html.P("Rate of Download (pkgs/sec)", style = {'textAlign': 'center', 'color' : 'white'})
                    ]

#Initiation for live data
start_time = pd.Timestamp('2019-02-25 00:12:00')
time3 = start_time
packages = []
@app.callback(Output('uniq_package', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics3(n):
    global time3
    global packages
    old_time = time3
    new_time = time3 + pd.Timedelta(seconds = 1)
    temp_data = data[(data['timestamp'] > old_time) & (data['timestamp'] <= new_time)]
    packages.extend(list(set(temp_data['module'])))
    packages = list(set(packages))
    time3 = new_time
    return [html.H4(str(len(packages)), style = {'color': 'white', 'textAlign': 'center' }),
                    html.P("No of Unique Modules Downloaded", style = {'textAlign': 'center', 'color' : 'white'})
                    ]

# # # # # # # # #
# detail the way that external_css and external_js work and link to alternative method locally hosted
# # # # # # # # #
external_css = [# "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                # "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                # "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                # "https://codepen.io/bcd/pen/KQrXdb.css",
                # "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                 "https://codepen.io/chriddyp/pen/bWLwgP.css"
                ]

for css in external_css:
    app.css.append_css({"external_url": css})

#external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
#               "https://codepen.io/bcd/pen/YaXojL.js"]

# for js in external_js:
#     app.scripts.append_script({"external_url": js})

if __name__ == '__main__':
    
    app.run_server(debug=True)