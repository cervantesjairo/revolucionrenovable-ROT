from dash import html
from revolucionrenovable_ROT.src.layers.renewable.battery.capex import BatteryCapex
from revolucionrenovable_ROT.src.layers.renewable.battery.opex import BatteryOpex
from revolucionrenovable_ROT.src.layers.renewable.battery.rte import BatteryRTE
from revolucionrenovable_ROT.src.layers.renewable.battery.poi import BatteryPOI
from revolucionrenovable_ROT.src.web.asset.storage.tab_battery_power_config import BatteryPowerConf
from revolucionrenovable_ROT.src.web.asset.storage.tab_battery_cap_config import BatteryCapConf
from revolucionrenovable_ROT.src.web.asset.storage.tab_battery_cycle_config import BatteryCycleConf
from revolucionrenovable_ROT.src.web.asset.storage.tab_battery_dod_config import BatteryDoDConf

# from web.information.simulation_type import ChiquiSimulation

class TabBattery:
    def __init__(self):
        # self.tab_battery_poi = ChiquiBatteryPOI()
        # self.tab_battery_power_conf = ChiquiBatteryPowerConf()
        # self.tab_battery_cap_conf = ChiquiBatteryCapConf()
        # self.tab_battery_capex = ChiquiBatteryCapex()
        # self.tab_battery_opex = ChiquiBatteryOpex()
        # self.tab_battery_rte = ChiquiBatteryRTE()
        # self.tab_battery_cycle_config = ChiquiBatteryCycleConf()
        # self.tab_battery_dod_config = ChiquiBatteryDoDConf()
        self.layout = self.setup_layout()

    def setup_layout(self):
        layout = \
            html.Div(
                children=[
                    html.Div(

                        children=[
                            html.Div(children=[BatteryPOI().layout]),
                            html.Div(children=[BatteryPowerConf().layout]),
                            html.Div(children=[BatteryCapConf().layout]),
                        ],
                        style={'width': '25%', 'float': 'left'}
                    ),

                    html.Div(
                        children=[
                            html.Div(children=[BatteryCapex().layout]),
                            html.Div(children=[BatteryOpex().layout]),
                            html.Div(children=[]),
                        ],
                        style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top'}
                    ),

                    html.Div(
                        children=[
                            html.Div(children=[BatteryRTE().layout]),
                        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top'}
                    ),

                    html.Div(
                        children=[
                            html.Div(children=[BatteryCycleConf().layout]),
                            html.Div(children=[BatteryDoDConf().layout]),
                        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top'}
                    ),
                ]
            )

        return layout
