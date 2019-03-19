import plotly.graph_objs as go
import plotly.plotly as py
import pandas as pd
import plotly 

plotly.tools.set_credentials_file(username='nrk60', api_key='33dDfH0GlJaksOCZaRzR')

df = pd.read_csv("E:\Semester-2\DIVA\Project\Development\sample_data.csv")

counts = pd.DataFrame(df['country_code'].value_counts())

data = [go.Choropleth(
    locations = counts.index,
    z = counts['country_code'],
    text = counts.index,
    colorscale = [
        [0, "rgb(5, 10, 172)"],
        [0.35, "rgb(40, 60, 190)"],
        [0.5, "rgb(70, 100, 245)"],
        [0.6, "rgb(90, 120, 245)"],
        [0.7, "rgb(106, 137, 247)"],
        [1, "rgb(220, 220, 220)"]
    ],
    autocolorscale = False,
    reversescale = True,
    marker = go.choropleth.Marker(
        line = go.choropleth.marker.Line(
            color = 'rgb(180,180,180)',
            width = 0.5
        )),
    colorbar = go.choropleth.ColorBar(
        tickprefix = '$',
        title = 'GDP<br>Billions US$'),
)]

layout = go.Layout(
    title = go.layout.Title(
        text = '2014 Global GDP'
    ),
    geo = go.layout.Geo(
        showframe = False,
        showcoastlines = False,
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

fig = go.Figure(data = data, layout = layout)
py.iplot(fig, filename = 'd3-world-map')