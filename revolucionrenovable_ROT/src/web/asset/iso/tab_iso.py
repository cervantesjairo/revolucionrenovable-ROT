from dash import html
from web.asset.iso.tab_iso_price import ChiquiCaisoPrice
from web.asset.iso.tab_iso_demand import ChiquiCaisoDemand



class TabISO:
    def __init__(self):
        self.tab_caiso_price = ChiquiCaisoPrice()
        self.tab_caiso_demand = ChiquiCaisoDemand()
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