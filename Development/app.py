import dash
import dash_auth
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output
import plotly.graph_objs as go
from components.header import Header

import time as t
import ast
import pandas as pd
import squarify

from datetime import datetime as dt
    
###################################
########Loading the data
###################################

data = pd.read_csv("data/sample_data.csv")
data['module'] = data['file'].apply(lambda x : ast.literal_eval(x)['project'])
data['timestamp'] = pd.to_datetime(data.timestamp)
dfcountry = pd.read_csv('countryMap.txt',sep='\t')
data = data.merge(dfcountry,how='inner',left_on=['country_code'],right_on=['2let'])

###################################
#######Authorisation
###################################
VALID_USERNAME_PASSWORD_PAIRS = [
    ['hello', 'world']
]

app = dash.Dash(__name__)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)


mapbox_access_token = 'pk.eyJ1IjoiYWxpc2hvYmVpcmkiLCJhIjoiY2ozYnM3YTUxMDAxeDMzcGNjbmZyMmplZiJ9.ZjmQ0C2MNs1AzEBC_Syadg'
server = app.server
app.config.suppress_callback_exceptions = True

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

#### TAB1 ######
##################################
main =  html.Div([
        html.Div([html.Br(),
            html.Div([
            html.Div(id = 'count_download', 
                style = {'width' : '29%', 'height': '90','backgroundColor' : '#00ACC1', 'marginLeft' : '2%' ,
                'boxShadow': '3px 3px 3px 3px #d1d1d1'}, className = 'column'),

            html.Div(id = 'rate_download', 
                style = {'width' : '29%',  'height': '90','backgroundColor' : '#00ACC1',
                'boxShadow': '3px 3px 3px 3px #d1d1d1'}, className = 'column'),

            html.Div(id = 'uniq_package'
                , style = {'width' : '29%', 'height': '90','backgroundColor' : '#00ACC1',
                'boxShadow': '3px 3px 3px 3px #d1d1d1'}, className = 'column'),
            ], id = '3 boxes')
            ], style = {'height' : '140px'}),
            
        html.Div([html.Div([html.Div(html.H5("Number of Downloads ", style = {'color': 'white', 'marginTop': '0px', 'marginLeft': '10px'})
                            , style = {'backgroundColor' : '#225ea8'}),
                
                            html.Div(dcc.Graph(id = 'world_map'))],
                            style = {'width': '45%', 'marginLeft':'3%', #'border': '1px solid #9b9b9b',  
                                    'boxShadow': '3px 3px 3px 3px #d1d1d1' }, className = 'column'),
                html.Div([html.Div(html.H5("Download Rate", style = {'color': 'white', 'marginTop': '0px', 'marginLeft': '10px'})
                    , style = {'backgroundColor' : '#225ea8'}),
                
                        html.Div(dcc.Graph(id = 'world_map_rate'))],
                        style = {'width': '45%', 'marginLeft':'3%', #'border': '1px solid #9b9b9b',  
                                'boxShadow': '3px 3px 3px 3px #d1d1d1' }, className = 'column')
        
        ], className = 'row'),
        html.Br(),
        #html.Hr(),       

        html.Div([html.Div([html.Div(html.H5("Download Rate (pkgs/sec)", style = {'color': 'white', 'marginTop': '0px', 'marginLeft': '10px'})
                            , style = {'backgroundColor' : '#225ea8'}),
                            html.Div(dcc.Graph(id = 'pkg_rate'))]
                , style = {'width': '45%', 'marginLeft':'3%', #'border': '1px solid #9b9b9b',  
                                    'boxShadow': '3px 3px 3px 3px #d1d1d1' }, className = 'column'),
                
                 html.Div([html.Div(html.H5("Top 10 Packages (#/sec)", style = {'color': 'white', 'marginTop': '0px', 'marginLeft': '10px'})
                            , style = {'backgroundColor' : '#225ea8'}),
                            html.Div(dcc.Graph(id = 'treemaps'))] 
                ,style = {'width': '45%', 'marginLeft':'3%', #'border': '1px solid #9b9b9b',  
                                'boxShadow': '3px 3px 3px 3px #d1d1d1' }, className = 'column')
        ], className = 'row')         
            
], id="mainDiv", style = {"backgroundColor":'#f2f2f2', "paddingBottom":'7%'})



##################################
#### TAB2 ######
##################################

###Reading the data for TAB2
#hist_data = pd.read_csv("E:/Semester-2/DIVA/Project/Development/data/summ.csv")
hist_data = pd.read_csv("E:/Semester-2/DIVA/Project/Development/data/data_g4.csv")
sankey_data = pd.read_csv("E:/Semester-2/DIVA/Project/Development/data/sankey_data.csv")
hist_data['Date'] = hist_data['Date'].astype('datetime64[ns]')

historical = html.Div([
    #html.Br(),
    html.Div([
        html.Br(),
        html.Br(),
        html.Div(
            [html.P('Select the Date Range:'),
            dcc.DatePickerRange(
            id='date_pick',
            min_date_allowed=dt(2018, 4, 15),
            max_date_allowed=dt(2019, 3, 14),
            #initial_visible_month=dt(2019, 2, 20),
            start_date = dt(2019,1,1),
            end_date = dt(2019,1,30)
            #end_date=dt(2019, 3, 24)
            )], style = {'width' : '30%', 'marginLeft' : '20%'}, className = 'column'        
        ), 
        html.Div([html.P('Select the Packages:', style = {'paddingBottom' : '8px' }),
            dcc.Dropdown(
                id = 'modules_dd',
                options=[{'label': 'All', 'value': 'All'}]+ [{'label': i, 'value': i} for i in hist_data.project.unique()],
                value=['All'],
                multi=True,
                searchable = True
            )], style = {'width' : '30%', 'marginLeft' : '5%', 'display': 'inline-block'}, className = 'column'        
        )
    ] , className = 'row'
    ),
    html.Br(),
    html.Div([
        html.Div(dcc.Graph(id = 'tab2_map'), style = {'width': '60%', # 'border': '1px solid #9b9b9b',  
                                    'boxShadow': '3px 3px 3px 3px #d1d1d1' }, className = 'column'),

        html.Div(dcc.Graph(id = 'top5_bar_plot'), style = {'width': '35%', # 'border': '1px solid #9b9b9b',  
                                    'boxShadow': '3px 3px 3px 3px #d1d1d1' }, className = 'column')
    
    ], style = {'margin': '3%'}, className = 'row'),

    html.Br(),
    
    html.Div(
        dcc.Graph(id = 'scatterplot', style ={'marginLeft': '25%', 'width' : '50%', 'boxShadow': '3px 3px 3px 3px #d1d1d1' } )
    )
    # html.Div(dcc.Graph(id = 'scatterplot'))
    
],className = 'Hist-Tab', style = {"backgroundColor":'#f2f2f2', "paddingBottom":'7%'})


##################################
## TAB3 - Trends
##################################

trends = html.Div([
        html.Br(),
        html.Br(),
        html.Div([
        html.Div([
            html.P('Select the Metric:', style = {'paddingBottom' : '8px' }),
            dcc.RadioItems(id = 'radio', 
                options=[
                    {'label': 'Actual', 'value': 'ACT'},
                    {'label': '10 Day Moving Average', 'value': '10D'},
                    {'label': '20 Day Moving Average', 'value': '20D'},
                    {'label': '30 Day Moving Average', 'value': '30D'}
                ], value = 'ACT'
            )],style = {'width' : '25%', 'marginLeft' : '20%', 'display': 'inline-block'}, className = 'columns'),
        html.Div([
            html.P('Select the Packages:', style = {'paddingBottom' : '8px' }),
            dcc.Dropdown(
                id = 'modules_trend',
                options=[{'label': 'All', 'value': 'All'}]+ [{'label': i, 'value': i} for i in hist_data.project.unique()],
                value=['All'],
                multi=True,
                searchable = True
            )], style = {'width' : '30%', 'marginLeft' : '5%', 'display': 'inline-block'}, className = 'column'        
        ), ], className= 'row'),
        html.Br(),
        html.Br(),
        html.Div(
            dcc.Graph(id = 'trend_line', style = {'width': '80%', 'marginLeft': '10%', #'border': '1px solid #9b9b9b',  
                                    'boxShadow': '3px 3px 3px 3px #d1d1d1' }), className = 'row')
        
        ],className = 'trendTab', style = {"backgroundColor":'#f2f2f2', "paddingBottom":'7%'})



##################################
## No Page Error
##################################
noPage = html.Div([  # 404

    html.P(["404 Page not found"])

    ], className="no-page")


tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    #'fontWeight': 'bold'
}

tab_selected_style = {
    #'borderTop': '1px solid #d6d6d6',
    #'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

app.layout = html.Div([
    Header(),
    
    dcc.Tabs(id="tabs-styled-with-inline", value='main', children=[
        dcc.Tab(label='Live Data', value='main', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Country Level', value='historical', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Package Trends', value='trends', style=tab_style, selected_style=tab_selected_style),
#        dcc.Tab(label='Others', value='others', style=tab_style, selected_style=tab_selected_style),
        #dcc.Tab(label='Team', value='aboutus', style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles),
    html.Div(id='tabs-content-inline')
], style = {'width': '90%','marginLeft':'5%', 'boxShadow': '3px 3px 3px 3px #d1d1d1'})

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
    elif tab == 'others':
        return noPage
    else:
        return noPage

############################################################################################################
################################### TAB1 #################
############################################################################################################

#Initiation for live data
start_time = pd.Timestamp('2019-03-25 09:00:00')
time = start_time
time2 = start_time
time3 = start_time
time4 = start_time
time5 = start_time
time6 = start_time
time7 = start_time
downloads = 0

colorscale_map = [[0.0, 'rgb(247,252,240)'], [1/10000000, 'rgb(224,243,219)'], [1/10000, 'rgb(204,235,197)'],
                             [1/1000, 'rgb(168,221,181)'], [1/100, 'rgb(123,204,196)'], [1/25, 'rgb(78,179,211)'],
                             [1/10, 'rgb(43,140,190)'],[1/3, 'rgb(8,104,172)'], [1, 'rgb(8,64,129)'],
                             [1, 'rgb(49,54,149)']]

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
    return [html.H3(str(downloads), style = {'color': 'white', 'textAlign': 'center', 'marginBottom': '0' }),
                    html.P("Number of Downloads", style = {'textAlign': 'center', 'color' : 'white'})
                    ]

#Initiation for live data
#start_time = pd.Timestamp('2019-02-25 00:12:00')
#time2 = start_time

@app.callback(Output('rate_download', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics2(n):
    global time2
    old_time = time2
    new_time = time2 + pd.Timedelta(seconds = 1)
    temp_data = data[(data['timestamp'] > old_time) & (data['timestamp'] <= new_time)]
    rate = temp_data.shape[0]
    time2 = new_time
    return [html.H3(str(rate), style = {'color': 'white', 'textAlign': 'center', 'marginBottom': '0' }),
                    html.P("Rate of Download (pkgs/sec)", style = {'textAlign': 'center', 'color' : 'white'})
                    ]

#Initiation for live data
#start_time = pd.Timestamp('2019-02-25 00:12:00')
#time3 = start_time
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
    return [html.H3(str(len(packages)), style = {'color': 'white', 'textAlign': 'center', 'marginBottom': '0' }),
                    html.P("No of Unique Modules Downloaded", style = {'textAlign': 'center', 'color' : 'white'})
                    ]

#Initiation for live data
#start_time = pd.Timestamp('2019-02-25 00:12:00')
#time4 = start_time
column_data = data.columns
temp_df = pd.DataFrame(columns= column_data)
@app.callback(Output('world_map', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_map(n):
    global time4
    global temp_df
    old_time = time4
    new_time = time4 + pd.Timedelta(seconds = 1)
    temp_data = data[(data['timestamp'] > old_time) & (data['timestamp'] <= new_time)]
    temp_df = temp_df.append(temp_data)
    time4 = new_time
    new = temp_df.groupby(['Countrylet', '3let']).size().reset_index(name= 'size')
    return {'data' :  [go.Choropleth(
                locations = new['3let'],
                z = new['size'],
                text = new['Countrylet'],
                # colorscale = [[0.0, 'rgb(165,0,38)'], [1/10000000, 'rgb(215,48,39)'], [1/10000, 'rgb(244,109,67)'],
                #             [1/1000, 'rgb(253,174,97)'], [1/100, 'rgb(254,224,144)'], [1/25, 'rgb(224,243,248)'],
                #             [1/10, 'rgb(171,217,233)'],[1/5, 'rgb(116,173,209)'], [1/2, 'rgb(69,117,180)'],
                #             [1, 'rgb(49,54,149)']],
                colorscale = colorscale_map,
                autocolorscale = False,
                reversescale = False,
                
                marker = go.choropleth.Marker(
                    line = go.choropleth.marker.Line(
                        color = 'rgb(180,180,180)',
                        width = 0.7
                        
                    )),
                colorbar = go.choropleth.ColorBar(
                    tickprefix = '#',
                    title = 'Downloads',
                    thickness= 10,
                    len = 0.6
                    ),
                )],
            'layout' : go.Layout(
                height = 350,
                uirevision= 'temp',
                margin =go.layout.Margin(
                            l=10,
                            r=0,
                            b=0,
                            t=0,
                            pad=4
                            )
            
                ,
                geo = go.layout.Geo(
                    showframe = False,
                    showcoastlines = False,
                    showcountries = True,
                    projection = go.layout.geo.Projection(
                        type = 'equirectangular'
                    )
                ),
                annotations = [go.layout.Annotation(
                    x = 0.55,
                    y = 0.1,
                    xref = 'paper',
                    yref = 'paper',
                    text = 'Number of Downloads',
                    showarrow = False
                )]
                )
            
        
            }
    
#Initiation for live data
#start_time = pd.Timestamp('2019-02-25 00:12:00')
#time5 = start_time
@app.callback(Output('world_map_rate', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_map2(n):
    global time5
    old_time = time5
    new_time = time5 + pd.Timedelta(seconds = 1)
    temp_data = data[(data['timestamp'] > old_time) & (data['timestamp'] <= new_time)]
    time5 = new_time
    new = temp_data.groupby(['Countrylet', '3let']).size().reset_index(name= 'size')
    return {'data' :  [go.Choropleth(
                locations = new['3let'],
                z = new['size'],
                text = new['Countrylet'],
                colorscale = colorscale_map,
                autocolorscale = False,
                reversescale = False,
                
                marker = go.choropleth.Marker(
                    line = go.choropleth.marker.Line(
                        color = 'rgb(180,180,180)',
                        width = 0.7
                    )),
                colorbar = go.choropleth.ColorBar(
                    ticksuffix= '#/sec',
                    title = 'Rate',
                    thickness= 10,
                    len= 0.6),
                )],
            'layout' : go.Layout(
                height = 350,
                uirevision= 'temp',
                margin =go.layout.Margin(
                            l=10,
                            r=0,
                            b=0,
                            t=0,
                            pad=4
                            ),
                geo = go.layout.Geo(
                    showframe = False,
                    showcoastlines = False,
                    showcountries = True,
                    projection = go.layout.geo.Projection(
                        type = 'equirectangular'
                    )
                ),
                annotations = [go.layout.Annotation(
                    x = 0.55,
                    y = 0.1,
                    xref = 'paper',
                    yref = 'paper',
                    text = 'Download Rate (pkgs/sec)',
                    showarrow = False
                )]
                )
            
        
            }


#Initiation for live data
#start_time = pd.Timestamp('2019-02-25 00:12:00')
#time6 = start_time
trend = [0] * 200
@app.callback(Output('pkg_rate', 'figure'), [Input('interval-component', 'n_intervals')])
def gen_package_rate(n):
    global time6
    global trend
    old_time = time6
    new_time = time6 + pd.Timedelta(seconds = 1)
    temp_data = data[(data['timestamp'] > old_time) & (data['timestamp'] <= new_time)]
    trend.append(temp_data.shape[0])
    time6 = new_time

    trace = go.Scatter(
        y=trend[-200:],
        line=go.scatter.Line(
            color='#42C4F7'
        ),
        #hoverinfo='skip',
        mode='lines'
    )

    layout = go.Layout(
        height=350,
        xaxis=dict(
            range=[0, 200],
            showgrid=False,
            showline=False,
            zeroline=False,
            fixedrange=True,
            tickvals=[0, 50, 100, 150, 200],
            ticktext=['200', '150', '100', '50', '0'],
            title='Time Elapsed (sec)'
        ),
        yaxis=dict(
            range=[0,2500],
            showline=False,
            fixedrange=False,
            zeroline=False
            #nticks=max(6, round(trend[-1]/10))
        ),
        uirevision= 'temp',
        margin =go.layout.Margin(
                            l=50,
                            r=40,
                            b=50,
                            t=80,
                            pad=10
                            )
    )

    return go.Figure(data=[trace], layout=layout)


#Initiation for live data
#start_time = pd.Timestamp('2019-02-25 00:12:00')

@app.callback(Output('treemaps', 'figure'), [Input('interval-component', 'n_intervals')])
def gen_tree_maps(n):
    global time7
    old_time = time7
    new_time = time7 + pd.Timedelta(seconds = 1)
    tree_data = data[(data['timestamp'] > old_time) & (data['timestamp'] <= new_time)]
    top_packages = dict(tree_data['module'].value_counts()[0:10])
    time7 = new_time
    x = 0.
    y = 0.
    width = 100.
    height = 100.

    values = list(top_packages.values())
    names = list(top_packages.keys())

    normed = squarify.normalize_sizes(values, width, height)
    rects = squarify.squarify(normed, x, y, width, height)

    # Choose colors from http://colorbrewer2.org/ under "Export"
    # color_brewer = ['rgb(158,1,66)','rgb(213,62,79)','rgb(244,109,67)',
    #                 'rgb(253,174,97)','rgb(254,224,139)','rgb(230,245,152)',
    #                 'rgb(171,221,164)','rgb(102,194,165)','rgb(50,136,189)','rgb(94,79,162)']
    color_brewer = ['#40c2d1','#53c8d6','#66ceda','#79d4df','#8cdae3','#a0e1e8','#b3e7ed','#c6edf1','#d9f3f6','#ecf9fa']

    shapes = []
    annotations = []
    counter = 0

    for r in rects:
        shapes.append( 
            dict(
                type = 'rect', 
                x0 = r['x'], 
                y0 = r['y'], 
                x1 = r['x']+r['dx'], 
                y1 = r['y']+r['dy'],
                line = dict( width = 2 ),
                fillcolor = color_brewer[counter]
            ) 
        )
        annotations.append(
            dict(
                x = r['x']+(r['dx']/2),
                y = r['y']+(r['dy']/2),
                text = names[counter],
                showarrow = False
            )
        )
        counter = counter + 1
        if counter >= len(color_brewer):
            counter = 0

    # For hover text
    trace0 = go.Scatter(
        x = [ r['x']+(r['dx']/2) for r in rects ], 
        y = [ r['y']+(r['dy']/2) for r in rects ],
        text = [ str(v) for v in values ], 
        mode = 'text'
        
    )
            
    layout = dict(
        height=350, 
        #width=700,
        xaxis=dict(showgrid=False,zeroline=False),
        yaxis=dict(showgrid=False,zeroline=False),
        shapes=shapes,
        annotations=annotations,
        hovermode='closest',
        uirevision= 'temp',
        margin =go.layout.Margin(
                            l=150,
                            r=150,
                            b=35,
                            t=50,
                            pad=10
                            ),
    )

    # With hovertext
    figure = dict(data=[trace0], layout=layout)
    return figure



############################################################################################################
################################### TAB2 #################
############################################################################################################

module_all = list(hist_data.project.unique())


# Helper functions
def filter_data(df, modules, date_start, date_end):
    start_date = dt.strptime(date_start, '%Y-%m-%d')
    end_date = dt.strptime(date_end, '%Y-%m-%d')
    if 'All' in modules:
        modules = module_all
    dff = df[(df['project'].isin(modules)) & (df['Date'] >= start_date) &  (df['Date'] <= end_date)]
    return dff

colorscale_map = [[0.0, 'rgb(247,252,240)'], [1/10000000, 'rgb(224,243,219)'], [1/10000, 'rgb(204,235,197)'],
                             [1/1000, 'rgb(168,221,181)'], [1/100, 'rgb(123,204,196)'], [1/25, 'rgb(78,179,211)'],
                             [1/10, 'rgb(43,140,190)'],[1/3, 'rgb(8,104,172)'], [1, 'rgb(8,64,129)'],
                             [1, 'rgb(49,54,149)']]
# ['rgb(247,252,240)','rgb(224,243,219)','rgb(204,235,197)','rgb(168,221,181)','rgb(123,204,196)','rgb(78,179,211)','rgb(43,140,190)','rgb(8,104,172)','rgb(8,64,129)']

# Selectors -> main graph
@app.callback(Output('tab2_map', 'figure'),
              [Input('modules_dd', 'value'),
               Input('date_pick', 'start_date'),
               Input('date_pick', 'end_date')])
              #[State('lock_selector', 'values'),
              #State('main_graph', 'relayoutData')])

def make_main_figure(modules_dd, start_date, end_date): #, year_slider,
                     #selector, main_graph_layout):
    global df_map

    df_map = filter_data(hist_data, modules_dd, start_date, end_date)

    new = df_map.groupby(['Countrylet', '3let'])['num_downloads'].sum().reset_index(name= 'size')

    data =  [go.Choropleth(
            locations = new['3let'],
            z = new['size'],
            text = new['Countrylet'],
            # colorscale = [[0,'rgb(255,255,217)'],[1e-10, 'rgb(237,248,177)'],[1e-9 ,'rgb(199,233,180)'],[ 1e-8,'rgb(127,205,187)']
                        # ,[1e-7,'rgb(65,182,196)'],[1e-6, 'rgb(29,145,192)'],[1e-5,'rgb(34,94,168)'],[ 1,'rgb(12,44,132)']],
            colorscale = colorscale_map,
            autocolorscale = False,
            reversescale = False,
            
            marker = go.choropleth.Marker(
                line = go.choropleth.marker.Line(
                    color = 'rgb(180,180,180)',
                    width = 0.7
                )),
            colorbar = go.choropleth.ColorBar(
                tickprefix = '#',
                title = 'Downloads',
                thickness= 10,
                len= 0.6),
            )]
    layout = go.Layout(
            height = 450,
            margin =go.layout.Margin(
                        l=10,
                        r=0,
                        b=5,
                        t=50,
                        pad=4
                        ),
            
            geo = go.layout.Geo(
                showframe = False,
                showcoastlines = False,
                showcountries = True,
                projection = go.layout.geo.Projection(
                    type = 'equirectangular'
                )
            ),
            title = go.layout.Title(
                text = 'Total Downloads across Countries'
            ),
            uirevision= 'temp',
            xaxis = go.layout.XAxis(fixedrange= False),
            yaxis = go.layout.YAxis(fixedrange= False),
            annotations = [go.layout.Annotation(
                x = 0.55,
                y = 0.1,
                xref = 'paper',
                yref = 'paper',
                text = 'Download Rate (pkgs/sec)',
                showarrow = False
            )]
            )
    figure = dict(data=data, layout=layout)
    return figure


@app.callback(Output('top5_bar_plot', 'figure'),
              [Input('tab2_map', 'hoverData')])
def top5PackByCountry(country):
    data_g4 = df_map.groupby(['country_code','project'])['num_downloads'].sum().reset_index()
    # extract 2let country code
    country = country['points'][0]['text']
    tmp_country = dfcountry[dfcountry['Countrylet']==country]
    country = tmp_country['2let'].values[0]

    title = "Top Package Downloads - " + str(country)
    ####################
    tmp_df = data_g4[data_g4['country_code']==country]
    tmp_df = tmp_df.sort_values(by=['num_downloads'], ascending=False)
    X = tmp_df['project'].head(5)
    Y = tmp_df['num_downloads'].head(5)
    trace0 = go.Bar(
        x = list(X),
        y = list(Y),
        marker=dict(
            color= ['rgb(8,81,156)', 'rgb(49,130,189)','rgb(107,174,214)','rgb(189,215,231)','rgb(239,243,255)']),
    )

    data = [trace0]
    layout = go.Layout(
        title= title,
        height = 450,
        margin =go.layout.Margin(
                        l=50,
                        r=50,
                        b=30,
                        t=50,
                        pad=4
                        )
    )

    fig = dict(data = data, layout = layout)
    return fig

@app.callback(Output('scatterplot', 'figure'),
              [Input('modules_dd', 'value'),
               Input('date_pick', 'start_date'),
               Input('date_pick', 'end_date')])
def scatterplot(modules_dd, start_date, end_date):
    if 'All' in modules_dd:
        modules_dd = module_all
    current_module = modules_dd[0:2]
    df_scatter = filter_data(hist_data, current_module, start_date, end_date)
    df_temp = df_scatter[df_scatter['project'].isin(current_module)]
    df_temp = df_temp.groupby(['Countrylet', 'project'])['num_downloads'].sum().reset_index(name= 'size')
    df_temp = df_temp.pivot(index = 'Countrylet', columns= 'project', values= 'size')
    df_temp['Country'] = df_temp.index
    df_temp.fillna(0)
    #print(df_temp)
    data = [go.Scatter(
                    x=df_temp[df_temp['Country'] == i][current_module[0]],
                    y=df_temp[df_temp['Country'] == i][current_module[1]],
                    text=df_temp[df_temp['Country'] == i]['Country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 10,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df_temp.Country.unique()

    ]

    
    layout = go.Layout(
        title= "Comparison of 2 Packages across Countries",
        height = 450,
        xaxis={'title': "Downloads " + current_module[0]},
        yaxis={'title': "Downloads " + current_module[1]},
        hovermode='closest',
        margin =go.layout.Margin(
                        l=50,
                        r=50,
                        b=30,
                        t=80,
                        pad=4
                        )
    )
    fig = dict(data = data, layout = layout)
    return fig
    




############################################################################################################
################################### TAB3 #################
############################################################################################################


trend_data = pd.read_csv("data/trend.csv")
trend_data['day']= pd.to_datetime(trend_data.day)
module_all_trend = trend_data['pack_name'].unique()
color_col = ['rgb(158,1,66)','rgb(213,62,79)','rgb(244,109,67)','rgb(253,174,97)','rgb(254,224,139)',
'rgb(230,245,152)','rgb(171,221,164)','rgb(102,194,165)','rgb(50,136,189)','rgb(94,79,162)']
# Selectors -> main graph
@app.callback(Output('trend_line', 'figure'),
              [Input('modules_trend', 'value'),
              Input('radio', 'value')])
               #Input('slider_hour', 'value'),
               #Input('systems_dd', 'value')])
              #[State('lock_selector', 'values'),
              #State('main_graph', 'relayoutData')])

def trend_figure(modules_trend, radio):
    if 'All' in modules_trend:
        modules_trend =  module_all_trend


    if radio == 'ACT':
        y = 'num_downloads'
    elif radio == '10D':
        y = 'avg10'
    elif radio == '20D':
        y= 'avg20'
    elif radio == '30D':
        y = 'avg30'

    data = []
    for i in range(len(modules_trend)):
        trace = go.Scatter(
        x=trend_data['day'][trend_data['pack_name'] == modules_trend[i]],
        y=trend_data[y][trend_data['pack_name'] == modules_trend[i]] ,
        name = modules_trend[i],
        #line = dict(color = color_col[i % 10]),
        line = dict(color = color_col[i % 10]),
        opacity = 0.8)
        data.append(trace)

    
    layout = dict(
        title='Trend Analyses of Packages',
        height = 500,
            margin =go.layout.Margin(
                        l=50,
                        r=20,
                        b=30,
                        t=50,
                        pad=10
                        ),
        scrollZoom = True,   
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                            label='1m',
                            step='month',
                            stepmode='backward'),
                    dict(count=6,
                            label='6m',
                            step='month',
                            stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible = True
            ),
            type='date'
        )
    )

    fig = dict(data=data, layout=layout)
    return fig
    

if __name__ == '__main__':
    
    app.run_server(debug=True)