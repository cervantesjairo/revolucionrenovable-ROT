from dash import html
from revolucionrenovable_ROT.src.layers.iso.caiso.param.iso_price import IsoPrice
from revolucionrenovable_ROT.src.layers.iso.caiso.param.iso_demand import IsoDemand


class TabISO:
    def __init__(self):
        self.tab_caiso_price = IsoPrice()
        self.tab_caiso_demand = IsoDemand()
        # self.tab_solar_inv_conf.callbacks()
        self.layout = self.setup_layout()

    def setup_layout(self):

        layout = \
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(children=[self.tab_caiso_price.layout]),
                        ], style={'width': '50%', 'float': 'left'}
                    ),
                    html.Div(

                        children=[
                            html.Div(children=[self.tab_caiso_demand.layout]),

                        ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}
                    ),


                ]
            )

        return layout
