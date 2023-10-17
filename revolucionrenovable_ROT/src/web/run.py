import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from revolucionrenovable_ROT.src.web.information.tab_information import TabInf
from revolucionrenovable_ROT.src.web.information.simulation_type import Simulation
from revolucionrenovable_ROT.src.web.asset.tab_asset import TabAsset
from revolucionrenovable_ROT.src.web.asset.solar.tab_solar_inv_config import SolarInvConf
from revolucionrenovable_ROT.src.web.asset.solar.tab_solar_ratio_config import SolarRatioConf
from revolucionrenovable_ROT.src.web.asset.storage.tab_battery_power_config import BatteryPowerConf
from revolucionrenovable_ROT.src.web.asset.storage.tab_battery_cap_config import BatteryCapConf
from revolucionrenovable_ROT.src.web.asset.storage.tab_battery_cycle_config import BatteryCycleConf
from revolucionrenovable_ROT.src.web.asset.storage.tab_battery_dod_config import BatteryDoDConf
from revolucionrenovable_ROT.src.web.asset.wind.tab_wind_config import WindConf

from revolucionrenovable_ROT.src.web.result.tab_result import TabResult
from revolucionrenovable_ROT.src.layers.timeseries.coordinate.latlon import LatLon
from revolucionrenovable_ROT.src.layers.timeseries.datetime.range import DateTimeRange
from revolucionrenovable_ROT.src.layers.eng_economy.cashflow import CashFlow


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#app = dash.Dash(__name__)

tab_info = TabInf()
tab_simulation_type = Simulation()
tab_result = TabResult()
tab_asset = TabAsset()
tab_solar_inv_config = SolarInvConf()
tab_solar_ratio_config = SolarRatioConf()
tab_battery_power_config = BatteryPowerConf()
tab_battery_cap_config = BatteryCapConf()
tab_battery_cycle_config = BatteryCycleConf()
tab_battery_dod_config = BatteryDoDConf()
tab_wind_config = WindConf()

tab_lat_lon = LatLon()
tab_date_range = DateTimeRange()
tab_cash_flow = CashFlow()

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
                    dcc.Tab(label='Information', children=tab_info.layout, style=style, selected_style=selected_style),
                    dcc.Tab(label='Asset', children=tab_asset.layout, style=style, selected_style=selected_style),
                    dcc.Tab(label='Result', children=tab_result.layout, style=style, selected_style=selected_style),
                ], vertical=False,
            )
        ]
    )


tab_result.setup_callbacks(app, tab_asset)
tab_lat_lon.setup_callbacks(app)
tab_solar_ratio_config.setup_callbacks(app)
tab_solar_inv_config.setup_callbacks(app)
tab_battery_power_config.setup_callbacks(app)
tab_battery_cap_config.setup_callbacks(app)
tab_battery_cycle_config.setup_callbacks(app)
tab_battery_dod_config.setup_callbacks(app)
tab_wind_config.setup_callbacks(app)
tab_simulation_type.setup_layout()
tab_date_range.setup_layout()

if __name__ == '__main__':
    app.run_server(debug=True)