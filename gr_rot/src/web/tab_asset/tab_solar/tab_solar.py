from dash import html
from gr_rot.src.layers.renewable.solar.param.capex import SolarCapex
from gr_rot.src.layers.renewable.solar.param.opex import SolarOpex
from gr_rot.src.layers.renewable.solar.param.elect_solar import SolarElec
from gr_rot.src.layers.renewable.solar.param.elect_inv import InvElec
from gr_rot.src.layers.renewable.solar.param.poi import SolarPOI
from gr_rot.src.layers.renewable.solar.mode.solar_inv_config import SolarInvConf
from gr_rot.src.layers.renewable.solar.mode.solar_ratio_config import SolarRatioConf
# from web.information.simulation_type import ChiquiSimulation


class TabSolar(SolarCapex, SolarOpex, SolarElec, InvElec, SolarPOI, SolarInvConf, SolarRatioConf):

    def __init__(self):
        # # self.tab_solar_inv_conf.callbacks()
        self.layout = self.setup_layout()

    def setup_layout(self):

        layout = \
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(children=[SolarPOI().layout]),
                            html.Div(children=[SolarInvConf().layout]),
                            html.Div(children=[SolarRatioConf().layout]),
                        ], style={'width': '25%', 'float': 'left'}
                    ),
                    html.Div(

                        children=[
                            html.Div(children=[SolarCapex().layout]),
                            html.Div(children=[SolarOpex().layout]),
                            html.Div(children=[]),

                        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top'}
                    ),
                    html.Div(
                        children=[
                            html.Div(children=[SolarElec().layout]),
                            html.Div(children=[InvElec().layout]),
                        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top'}
                    )



                ]
            )

        return layout
