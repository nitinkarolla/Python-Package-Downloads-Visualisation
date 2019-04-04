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

data = pd.read_csv("sample_data.csv")
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
                style = {'width' : '29%', 'height': '90','backgroundColor' : '#5108af', 'marginLeft' : '2%' ,
                'boxShadow': '3px 3px 3px 3px #d1d1d1'}, className = 'column'),

            html.Div(id = 'rate_download', 
                style = {'width' : '29%',  'height': '90','backgroundColor' : '#0bbf4d',
                'boxShadow': '3px 3px 3px 3px #d1d1d1'}, className = 'column'),

            html.Div(id = 'uniq_package'
                , style = {'width' : '29%', 'height': '90','backgroundColor' : '#edc423',
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
hist_data = pd.read_csv("E:/Semester-2/DIVA/Project/Development/data/summ.csv")


historical = html.Div([
    #html.Br(),
    html.Div([
        html.Br(),
        html.Br(),
        html.Div(
            [html.P('Select the Date Range:'),
            dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=dt(2019, 1, 1),
            max_date_allowed=dt(2019, 3, 24),
            initial_visible_month=dt(2019, 3, 20)
            #end_date=dt(2019, 3, 24)
            )], style = {'width' : '25%', 'marginLeft' : '8%'}, className = 'column'        
        ), 
        html.Div([html.P('Select the Packages:', style = {'paddingBottom' : '8px' }),
            dcc.Dropdown(
                id = 'modules_dd',
                options=[{'label': 'All', 'value': 'All'}]+ [{'label': i, 'value': i} for i in hist_data.Module.unique()],
                value=['All'],
                multi=True,
                searchable = True
            )], style = {'width' : '25%', 'marginLeft' : '2%', 'display': 'inline-block'}, className = 'column'        
        ),
        html.Div([html.P('Select the Systems:', style = {'paddingBottom' : '8px' }),
            dcc.Dropdown(
                id = 'systems_dd',
                options=[{'label': 'All', 'value': 'All'}]+ [{'label': i, 'value': i} for i in hist_data.System.unique()],
                value=['All'],
                multi=True,
                searchable = True
            )], style = {'width' : '25%', 'marginLeft' : '5%', 'display': 'inline-block'}, className = 'column'        
        )
    ] , className = 'row'
    ),
    html.Br(),
    html.Div([
        html.P("Select the hour of the day:"),
        html.Div(dcc.Slider(id='slider_hour',
            marks={i: '{}'.format (str(i)+ ': 00') for i in range(24)},
            min = -1,
            max=23,
            value=-1,
            step=1,
            updatemode='drag' )         
        , className = 'column')],
    className = 'row', style = {'marginLeft': '8%', 'width': '75%'}),
    html.Br(),
    html.Div([
        html.Div(dcc.Graph(id = 'tab2_map'), style = {'width': '55%', # 'border': '1px solid #9b9b9b',  
                                    'boxShadow': '3px 3px 3px 3px #d1d1d1' }, className = 'column'),

        html.Div(dcc.Graph(id = 'cate_plot'), style = {'width': '40%', # 'border': '1px solid #9b9b9b',  
                                    'boxShadow': '3px 3px 3px 3px #d1d1d1' }, className = 'column')
    
    ], style = {'margin': '3%'}, className = 'row'),

    html.Div(dcc.Graph(id = 'trend_line'), style = {'width': '60%', 'marginLeft': '20%', #'border': '1px solid #9b9b9b',  
                                    'boxShadow': '3px 3px 3px 3px #d1d1d1' })
    
],className = 'Hist-Tab', style = {"backgroundColor":'#f2f2f2', "paddingBottom":'7%'})


##################################
#### TAB3 ######
##################################
trends = html.Div('trends')







##################################
#### TAB4 ######
##################################
ref = html.Div('references')







##################################
#### TAB5 ######
##################################
aboutus = html.Div('about us')




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
        dcc.Tab(label='Historical Data', value='historical', style=tab_style, selected_style=tab_selected_style),
        #dcc.Tab(label='Interesting Trends', value='trends', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='References', value='ref', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Team', value='aboutus', style=tab_style, selected_style=tab_selected_style),
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
    elif tab == 'ref':
        return ref
    elif tab == 'aboutus':
        return aboutus
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
                colorscale = [[0.0, 'rgb(165,0,38)'], [1/10000000, 'rgb(215,48,39)'], [1/10000, 'rgb(244,109,67)'],
                            [1/1000, 'rgb(253,174,97)'], [1/100, 'rgb(254,224,144)'], [1/25, 'rgb(224,243,248)'],
                            [1/10, 'rgb(171,217,233)'],[1/5, 'rgb(116,173,209)'], [1/2, 'rgb(69,117,180)'],
                            [1, 'rgb(49,54,149)']],
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
                colorscale = 'Rainbow',
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
    color_brewer = ['rgb(158,1,66)','rgb(213,62,79)','rgb(244,109,67)',
                    'rgb(253,174,97)','rgb(254,224,139)','rgb(230,245,152)',
                    'rgb(171,221,164)','rgb(102,194,165)','rgb(50,136,189)','rgb(94,79,162)']
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

module_all = list(hist_data.Module.unique())
hour_all = list(hist_data.Hour.unique())
system_all = list(hist_data.System.unique())

# Helper functions
def filter_data(df, modules, system, hour):
    if 'All' in modules:
        modules = module_all
    if 'All' in system:
        system = system_all
    if hour == -1:
        dff = df[df['System'].isin(system)
                & df['Module'].isin(modules)
                ]
    else :
        dff = df[df['Module'].isin(modules)
                 & df['System'].isin(system) &
                 (df['Hour'] == hour)
                ]
    return dff


# Selectors -> main graph
@app.callback(Output('tab2_map', 'figure'),
              [Input('modules_dd', 'value'),
               Input('slider_hour', 'value'),
               Input('systems_dd', 'value')])
              #[State('lock_selector', 'values'),
              #State('main_graph', 'relayoutData')])

def make_main_figure(modules_dd, slider_hour, systems_dd): #, year_slider,
                     #selector, main_graph_layout):

    dff = filter_data(hist_data, modules_dd, systems_dd, slider_hour)

    new = dff.groupby(['Countrylet', '3let'])['Downloads'].sum().reset_index(name= 'size')

    data =  [go.Choropleth(
            locations = new['3let'],
            z = new['size'],
            text = new['Countrylet'],
            colorscale = [[0,'rgb(255,255,217)'],[1e-10, 'rgb(237,248,177)'],[1e-9 ,'rgb(199,233,180)'],[ 1e-8,'rgb(127,205,187)']
                        ,[1e-7,'rgb(65,182,196)'],[1e-6, 'rgb(29,145,192)'],[1e-5,'rgb(34,94,168)'],[ 1,'rgb(12,44,132)']],
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
            height = 350,
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

trend_data = pd.read_csv("trend.csv")

color_col = ['rgb(158,1,66)','rgb(213,62,79)','rgb(244,109,67)','rgb(253,174,97)','rgb(254,224,139)',
'rgb(230,245,152)','rgb(171,221,164)','rgb(102,194,165)','rgb(50,136,189)','rgb(94,79,162)']
# Selectors -> main graph
@app.callback(Output('trend_line', 'figure'),
              [Input('modules_dd', 'value')])
               #Input('slider_hour', 'value'),
               #Input('systems_dd', 'value')])
              #[State('lock_selector', 'values'),
              #State('main_graph', 'relayoutData')])

def trend_figure(modules_dd):
    if 'All' in modules_dd:
        modules_dd =  module_all   
    data = []
    for i in range(len(modules_dd)):
        trace = go.Scatter(
        x=trend_data['date'][trend_data['module'] == modules_dd[i]],
        y=trend_data['count'][trend_data['module'] == modules_dd[i]] ,
        name = modules_dd[i],
        #line = dict(color = color_col[i % 10]),
        line = dict(color = color_col[i % 10]),
        opacity = 0.8)
        data.append(trace)

    
    layout = dict(
        title='Trend Analyses of Packages',
        height = 350,
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

@app.callback(Output('cate_plot', 'figure'),
              [Input('slider_hour', 'value')])
def generate_parallel_cord_plots(slider_hour):

    new = filter_data(hist_data, 'All', 'All', slider_hour)

    grouped = new.groupby(['Version', 'CPU', 'System'])['Downloads'].sum().reset_index(name='Sum')

    data = [go.Parcats(
    dimensions=[
        {'label': 'System',
         'values': list(grouped['System'])},
        {'label': 'CPU',
         'values': list(grouped['CPU'])},
        {'label': 'Version',
         'values': list(grouped['Version'])}],
    counts= list(grouped['Sum']),
    line = {'shape' : 'hspline',
            'color': '#1a9850'}
            #'colorscale': 'Rainbow'},
    
    )]

    layout = go.Layout(
                height = 350,
                uirevision= 'temp',
                title = 'Distribution of System/CPU/Version',
                margin =go.layout.Margin(
                            l=15,
                            r=15,
                            b=35,
                            t=80,
                            pad=10
                            ))
    fig = dict(data = data, layout = layout)
    return fig

if __name__ == '__main__':
    
    app.run_server(debug=True)