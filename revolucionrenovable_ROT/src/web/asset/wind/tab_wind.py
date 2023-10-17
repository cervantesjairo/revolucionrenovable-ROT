from dash import html
from revolucionrenovable_ROT.src.layers.renewable.wind.capex import WindCapex
from revolucionrenovable_ROT.src.layers.renewable.wind.opex import WindOpex
from revolucionrenovable_ROT.src.layers.renewable.wind.turbine import WindTurb
from revolucionrenovable_ROT.src.layers.renewable.wind.poi import WindPOI
from revolucionrenovable_ROT.src.web.asset.wind.tab_wind_config import WindConf


class TabWind:
    def __init__(self):
        # self.tab_solar_inv_conf.callbacks()
        self.layout = self.setup_layout()

    def setup_layout(self):

        layout = \
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(children=[WindPOI().layout]),
                            html.Div(children=[WindConf().layout]),
                        ], style={'width': '25%', 'float': 'left'}
                    ),
                    html.Div(

                        children=[
                            html.Div(children=[WindCapex().layout]),
                            html.Div(children=[WindOpex().layout]),
                            html.Div(children=[]),

                        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top'}
                    ),
                    html.Div(
                        children=[
                            html.Div(children=[WindTurb().layout]),
                            html.Div(children=[]),
                        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top'}
                    )



                ]
            )

        return layout
