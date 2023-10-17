from dash import html
from common.timeseries.date.range import ChiquiDateRange
from common.timeseries.coordinate.latlon import ChiquiLatLon
from common.economics.financial import ChiquiCashFlow
from web.information.simulation_type import ChiquiSimulation

class TabInf(ChiquiSimulation, ChiquiCashFlow, ChiquiDateRange, ChiquiLatLon):
    def __init__(self):
        self.tab_sim_type = ChiquiSimulation()
        self.tab_plan_interest = ChiquiCashFlow()
        self.tab_date_range = ChiquiDateRange()
        self.tab_lat_lot = ChiquiLatLon()
        self.layout = self.setup_layout()

    def setup_layout(self):
        layout = \
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(children=[self.tab_sim_type.layout]),
                            html.Div(children=[self.tab_date_range.layout]),
                            html.Div(children=[self.tab_plan_interest.layout]),

                        ], style={'width': '25%', 'float': 'left'}
                    ),
                    html.Div(
                        children=[
                            html.Div(children=[self.tab_lat_lot.layout]),
                        ], style={'width': '75%', 'float': 'right'}
                    )
                ]
            )

        return layout