import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv("E:\Semester-2\DIVA\Project\Development\sample_data.csv")
dfcountry = pd.read_csv('countryMap.txt',sep='\t')

df = df.merge(dfcountry,how='inner',left_on=['country_code'],right_on=['2let'])

new = df.groupby(['Countrylet', '3let']).size().reset_index(name= 'size')


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    dcc.Graph(
    figure = go.Figure(
        data =  [go.Choropleth(
            locations = new['3let'],
            z = new['size'],
            text = new['Countrylet'],
            colorscale = 'Viridis',
            autocolorscale = False,
            reversescale = True,

            marker = go.choropleth.Marker(
                line = go.choropleth.marker.Line(
                    color = 'rgb(180,180,180)',
                    width = 0.7
                )),
            colorbar = go.choropleth.ColorBar(
                tickprefix = '#',
                title = 'Number of Downloads',
                thickness= 10),
            )],
        layout = go.Layout(
            title = go.layout.Title(
                text = '# Package Downloads'
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
                showarrow = False
            )]
            )
        
    
    ), id='graph-with-slider'

))


if __name__ == '__main__':
    app.run_server(debug=True)


