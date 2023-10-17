from dash import html

from common.renewable.battery.capex import ChiquiBatteryCapex
from common.renewable.battery.opex import ChiquiBatteryOpex
from common.renewable.battery.rte import ChiquiBatteryRTE
from common.renewable.battery.poi import ChiquiBatteryPOI
from web.asset.storage.tab_battery_power_config import ChiquiBatteryPowerConf
from web.asset.storage.tab_battery_cap_config import ChiquiBatteryCapConf
from web.asset.storage.tab_battery_cycle_config import ChiquiBatteryCycleConf
from web.asset.storage.tab_battery_dod_config import ChiquiBatteryDoDConf

from web.information.simulation_type import ChiquiSimulation

class TabBattery:
    def __init__(self):
        self.tab_battery_poi = ChiquiBatteryPOI()
        self.tab_battery_power_conf = ChiquiBatteryPowerConf()
        self.tab_battery_cap_conf = ChiquiBatteryCapConf()
        self.tab_battery_capex = ChiquiBatteryCapex()
        self.tab_battery_opex = ChiquiBatteryOpex()
        self.tab_battery_rte = ChiquiBatteryRTE()
        self.tab_battery_cycle_config = ChiquiBatteryCycleConf()
        self.tab_battery_dod_config = ChiquiBatteryDoDConf()
        self.layout = self.setup_layout()

    def setup_layout(self):
        layout = \
            html.Div(
                children=[
                    html.Div(

                        children=[
                            html.Div(children=[self.tab_battery_poi.layout]),
                            html.Div(children=[self.tab_battery_power_conf.layout]),
                            html.Div(children=[self.tab_battery_cap_conf.layout]),
                        ],
                        style={'width': '25%', 'float': 'left'}
                    ),

                    html.Div(
                        children=[
                            html.Div(children=[self.tab_battery_capex.layout]),
                            html.Div(children=[self.tab_battery_opex.layout]),
                            html.Div(children=[]),
                        ],
                        style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top'}
                    ),

                    html.Div(
                        children=[
                            html.Div(children=[self.tab_battery_rte.layout]),
                        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top'}
                    ),

                    html.Div(
                        children=[
                            html.Div(children=[self.tab_battery_cycle_config.layout]),
                            html.Div(children=[self.tab_battery_dod_config.layout]),
                        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top'}
                    ),
                ]
            )

        return layout