import dash
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output

from components.header import Header


app = dash.Dash(__name__)
server = app.server

#### TAB1 ######
##################################
main = html.Div('main')


#### TAB2 ######
##################################

historical = html.Div('historical')


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
# detail in depth what the callback below is doing
# # # # # # # # #
# @app.callback(dash.dependencies.Output('page-content', 'children'),
#               [dash.dependencies.Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/' or pathname == '/main':
#         return main
#     elif pathname == '/historical':
#         return historical
#     elif pathname == '/trends':
#         return trends
#     elif pathname == '/ref':
#         return ref
#     elif pathname == '/aboutus':
#         return aboutus
#     else:
#         return noPage

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