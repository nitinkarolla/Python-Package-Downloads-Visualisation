import dash_html_components as html
import dash_core_components as dcc

def Header():
    return html.Div([
                html.Div([
                    html.Img(src= "https://cdn.freebiesupply.com/logos/large/2x/python-3-logo-png-transparent.png", height='60')
                        ] #, style = {'width' : '10%'}
                        ),
                dcc.Interval(
                id='interval-component',
                interval=1*1400, # in milliseconds
                n_intervals=0
            )   #,
                # html.Div([html.H1('Python Package Analyser',  style ={ 'textAlign':'center', 'color' : 'white', 'marginBottom': '0'})
                #         ], style = {'backgroundColor':'#d73027', 'paddingTop' : '2px', 'paddingBottom' : '2px'
                #          #, 'marginLeft': '10', 'width':'80%'
                #         })
    ])


