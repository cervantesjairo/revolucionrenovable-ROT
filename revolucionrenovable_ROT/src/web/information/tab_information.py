from dash import html
from revolucionrenovable_ROT.src.web.information.simulation_type import Simulation
from revolucionrenovable_ROT.src.layers.timeseries.coordinate.latlon import LatLon
from revolucionrenovable_ROT.src.layers.timeseries.datetime.range import DateTimeRange
from revolucionrenovable_ROT.src.layers.eng_economy.cashflow import CashFlow


class TabInf(Simulation, CashFlow, DateTimeRange, LatLon):
    def __init__(self):
        # self.tab_sim_type = ChiquiSimulation()
        # self.tab_plan_interest = ChiquiCashFlow()
        # self.tab_date_range = ChiquiDateRange()
        # self.tab_lat_lot = ChiquiLatLon()
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
