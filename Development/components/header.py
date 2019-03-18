import dash_html_components as html
import dash_core_components as dcc

def Header():
    return html.Div([
        get_logo(),
        get_header(),
        html.Br([])
        # get_menu()
    ])

def get_logo():
    logo = html.Div([

        html.Div([
            html.Img(src='E:\Semester-2\DIVA\Project\Development\logo.png', height='40', width='160')
        ], className="ten columns padded")

    ], className="row gs-header")
    return logo


def get_header():
    header = html.Div([

        html.Div([
            html.H1(
                'Python Package Analyser',  style ={ 'textAlign':'center', 'color' : 'white'})
        ], style = {'backgroundColor':'#00c6b9'},className="twelve columns padded")

    ], className="row gs-header gs-text-header")
    return header


# def get_menu():
#     menu = html.Div([

#         dcc.Link('Live Data   ', href='/main', className="tab first"),

#         dcc.Link('Historical Data   ', href='/historical', className="tab"),

#         dcc.Link('Interesting Trends   ', href='/trends', className="tab"),

#         dcc.Link('References   ', href='/ref', className="tab"),

#         dcc.Link('About Us   ', href='/aboutus', className="tab")

#     ], className="row ")
#     return menu