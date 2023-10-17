from dash import html
from common.renewable.wind.capex import ChiquiWindCapex
from common.renewable.wind.opex import ChiquiWindOpex
from common.renewable.wind.turbine import ChiquiWindTurb
from common.renewable.wind.poi import ChiquiWindPOI
from web.asset.wind.tab_wind_config import ChiquiWindConf



class TabWind:
    def __init__(self):
        self.tab_wind_capex = ChiquiWindCapex()
        self.tab_wind_opex = ChiquiWindOpex()
        self.tab_wind_turbine = ChiquiWindTurb()
        self.tab_wind_conf = ChiquiWindConf()
        self.tab_wind_poi = ChiquiWindPOI()
        # self.tab_solar_inv_conf.callbacks()
        self.layout = self.setup_layout()

    def setup_layout(self):

        layout = \
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(children=[self.tab_wind_poi.layout]),
                            html.Div(children=[self.tab_wind_conf.layout]),
                        ], style={'width': '25%', 'float': 'left'}
                    ),
                    html.Div(

                        children=[
                            html.Div(children=[self.tab_wind_capex.layout]),
                            html.Div(children=[self.tab_wind_opex.layout]),
                            html.Div(children=[]),

                        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top'}
                    ),
                    html.Div(
                        children=[
                            html.Div(children=[self.tab_wind_turbine.layout]),
                            html.Div(children=[]),
                        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top'}
                    )



                ]
            )

        return layout