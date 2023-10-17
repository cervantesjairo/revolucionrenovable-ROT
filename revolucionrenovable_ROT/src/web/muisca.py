import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from web.information.tab_information import TabInf
from web.information.simulation_type import ChiquiSimulation
from web.asset.tab_asset import TabAsset
from web.asset.solar.tab_solar_inv_config import ChiquiSolarInvConf
from web.asset.solar.tab_solar_ratio_config import ChiquiSolarRatioConf
from web.asset.storage.tab_battery_power_config import ChiquiBatteryPowerConf
from web.asset.storage.tab_battery_cap_config import ChiquiBatteryCapConf
from web.asset.storage.tab_battery_cycle_config import ChiquiBatteryCycleConf
from web.asset.storage.tab_battery_dod_config import ChiquiBatteryDoDConf
from web.asset.wind.tab_wind_config import ChiquiWindConf


from web.result.tab_result import TabResult
from common.timeseries.date.range import ChiquiDateRange
from common.timeseries.coordinate.latlon import ChiquiLatLon
from common.economics.financial import ChiquiCashFlow

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#app = dash.Dash(__name__)

tab_info = TabInf()
tab_simulation_type = ChiquiSimulation()
tab_result = TabResult()
tab_asset = TabAsset()
tab_solar_inv_config = ChiquiSolarInvConf()
tab_solar_ratio_config = ChiquiSolarRatioConf()
tab_battery_power_config = ChiquiBatteryPowerConf()
tab_battery_cap_config = ChiquiBatteryCapConf()
tab_battery_cycle_config = ChiquiBatteryCycleConf()
tab_battery_dod_config = ChiquiBatteryDoDConf()
tab_wind_config = ChiquiWindConf()

tab_lat_lon = ChiquiLatLon()
tab_date_range = ChiquiDateRange()
tab_cash_flow = ChiquiCashFlow()

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