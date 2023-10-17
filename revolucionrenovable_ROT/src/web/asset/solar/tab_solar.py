from dash import html
from common.renewable.solar.capex import ChiquiSolarCapex
from common.renewable.solar.opex import ChiquiSolarOpex
from common.renewable.solar.elect_solar import ChiquiSolarElec
from common.renewable.solar.elect_inv import ChiquiInvElec
from common.renewable.solar.poi import ChiquiSolarPOI
from web.asset.solar.tab_solar_inv_config import ChiquiSolarInvConf
from web.asset.solar.tab_solar_ratio_config import ChiquiSolarRatioConf
from web.information.simulation_type import ChiquiSimulation

class TabSolar:
    def __init__(self):
        self.tab_solar_poi = ChiquiSolarPOI()
        self.tab_solar_capex = ChiquiSolarCapex()
        self.tab_solar_opex = ChiquiSolarOpex()
        self.tab_solar_elec = ChiquiSolarElec()
        self.tab_solar_inv_elec = ChiquiInvElec()
        self.tab_solar_inv_conf = ChiquiSolarInvConf()
        self.tab_solar_ratio_conf = ChiquiSolarRatioConf()
        # self.tab_solar_inv_conf.callbacks()
        self.layout = self.setup_layout()

    def setup_layout(self):

        layout = \
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(children=[self.tab_solar_poi.layout]),
                            html.Div(children=[self.tab_solar_inv_conf.layout]),
                            html.Div(children=[self.tab_solar_ratio_conf.layout]),
                        ], style={'width': '25%', 'float': 'left'}
                    ),
                    html.Div(

                        children=[
                            html.Div(children=[self.tab_solar_capex.layout]),
                            html.Div(children=[self.tab_solar_opex.layout]),
                            html.Div(children=[]),

                        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top'}
                    ),
                    html.Div(
                        children=[
                            html.Div(children=[self.tab_solar_elec.layout]),
                            html.Div(children=[self.tab_solar_inv_elec.layout]),
                        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top'}
                    )



                ]
            )

        return layout