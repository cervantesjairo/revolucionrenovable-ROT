import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
### TABS
from gr_rot.src.web.tab_information.info import Inf
from gr_rot.src.web.tab_asset.asset import Asset
from gr_rot.src.web.tab_result.run import Run

from config import setup_callbacks

# Crear la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

style = {
    'backgroundColor': '#4a86e8',
    'color': 'white',
    'borderRadius': '24px 24px 24px 24px',
    'fontSize': '18px',
    'height': '55px',
    'display': 'flex',
    'justify-content': 'center',
    'align-items': 'center'
}

selected_style = {
    'backgroundColor': '#222e50',
    'color': 'white',
    'borderRadius': '24px 24px 24px 24px',
    'fontWeight': 'bold',
    'fontSize': '20px',
    'height': '55px',
    'display': 'flex',
    'justify-content': 'center',
    'align-items': 'center'
}

# Definir el diseño de la aplicación
app.layout = html.Div(
    [
        dcc.Tabs(
            [
                dcc.Tab(label='Information', children=Inf().layout, style=style, selected_style=selected_style),
                dcc.Tab(label='Asset', children=Asset().layout, style=style, selected_style=selected_style),
                dcc.Tab(label='Result', children=Run().layout, style=style, selected_style=selected_style),
            ], vertical=False,
        )
    ]
)

# Configurar los callbacks
setup_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
