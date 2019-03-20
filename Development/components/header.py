import dash_html_components as html
import dash_core_components as dcc

def Header():
    return html.Div([
                html.Div([
                    html.Img(src= "https://cdn.freebiesupply.com/logos/large/2x/python-3-logo-png-transparent.png", height='40')
                        ] #, style = {'width' : '10%'}
                        ),
                html.Div([html.H1('Python Package Analyser',  style ={ 'textAlign':'center', 'color' : 'white'})
                        ], style = {'backgroundColor':'#00c6b9', 'paddingTop': '2rem', 'paddingBottom': '2rem'
                         #, 'marginLeft': '10', 'width':'80%'
                        })
    ])


