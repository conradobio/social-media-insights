import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H4('Insta', className='display-4'),
        html.Hr(),
        html.P(
            "Selecione a página desejada", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink('Dashboard', href='/', active='exact'),
                dbc.NavLink('Configuração', href='/configuracao', active='exact'),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE
)

content = html.Div(id='page-content', style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id='url'), sidebar, content])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == '/':
        return html.P('Essa é a página principal!')
    elif pathname == '/configuracao':
        return html.P('Essa é a página de configurações')
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

if __name__ == "__main__":
    app.run_server(debug=True)