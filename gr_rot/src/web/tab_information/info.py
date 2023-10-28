from dash import html
from gr_rot.src.layers.simulation.param.simulation_type import Simulation
from gr_rot.src.layers.timeseries.mode.latlon import LatLon
from gr_rot.src.layers.timeseries.param.datetime_range import DateTimeRange
from gr_rot.src.layers.eng_economy.cashflow import CashFlow


class Inf(Simulation, CashFlow, DateTimeRange, LatLon):
    def __init__(self):
        self.layout = self.setup_layout()

    def setup_layout(self):
        layout = \
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(children=[Simulation().layout]),
                            html.Div(children=[DateTimeRange().layout]),
                            html.Div(children=[CashFlow().layout]),

                        ], style={'width': '25%', 'float': 'left'}
                    ),
                    html.Div(
                        children=[
                            html.Div(children=[LatLon().layout]),
                        ], style={'width': '75%', 'float': 'right'}
                    )
                ]
            )

        return layout
