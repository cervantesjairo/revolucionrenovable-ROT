import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

### MODES
from gr_rot.src.layers.renewable.solar.mode.solar_inv_config import SolarInvConf
from gr_rot.src.layers.renewable.solar.mode.solar_ratio_config import SolarRatioConf
from gr_rot.src.layers.renewable.battery.mode.battery_power_config import BatteryPowerConf
from gr_rot.src.layers.renewable.battery.mode.battery_cap_config import BatteryCapConf
from gr_rot.src.layers.renewable.battery.mode.battery_cycle_config import BatteryCycleConf
from gr_rot.src.layers.renewable.battery.mode.battery_dod_config import BatteryDoDConf
from gr_rot.src.layers.renewable.wind.mode.wind_config import WindConf
from gr_rot.src.layers.timeseries.mode.latlon import LatLon

### TABS
from gr_rot.src.web.tab_information.info import Inf
from gr_rot.src.web.tab_asset.asset import Asset
from gr_rot.src.web.tab_result.run import Run


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


style = \
    {
    'backgroundColor': '#4a86e8',
    'color': 'white',
    'borderRadius': '24px 24px 24px 24px',
    'fontSize': '18px',
    'height': '55px',
    'display': 'flex',
    'justify-content': 'center',
    'align-items': 'center'
    }

selected_style = \
    {
        'backgroundColor': '#222e50',#'#2a5db0',
        'color': 'white',
        'borderRadius': '24px 24px 24px 24px',
        'fontWeight': 'bold',
        'fontSize': '20px',
        'height': '55px',
        'display': 'flex',
        'justify-content': 'center',
        'align-items': 'center'}

app.layout = \
    html.Div(
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


Run().setup_callbacks(app)
WindConf().setup_callbacks(app)
LatLon().setup_callbacks(app)
SolarInvConf().setup_callbacks(app)
SolarRatioConf().setup_callbacks(app)
BatteryPowerConf().setup_callbacks(app)
BatteryCapConf().setup_callbacks(app)
BatteryCycleConf().setup_callbacks(app)
BatteryDoDConf().setup_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
