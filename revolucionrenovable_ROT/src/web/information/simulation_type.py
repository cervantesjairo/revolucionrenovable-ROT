from dash import dcc, html


class Simulation:

    def __init__(self):
        # TODO: Simulation for service and define the type of the dispatch economico or diseno optimization.
        self.asset_mode = 'wind_and_solar_and_battery' #'wind_and_solar' #'battery'
        self.poi_asset = 150
        self.watts = 'kW'
        self.layout = self.setup_layout()

    def setup_layout(self):
        style_name_summary = {
            'text-align': 'center',
            'font-size': '1.5em',
            'line-height': '200%',
        }

        style_label = {
            'display': 'inline-block',
            'margin-right': '10px',
            'text-align': 'right',
            'width': '200px',
            'font-size': '1.3em',
        }

        style_input = {
            'display': 'inline-block',
            'margin-left': '10px',
            'width': '200px',
            'text-align': 'center',
            'font-size': '1.2em',
        }
        style_box = {'padding': '0px', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
        style_m_bottom = {'margin-bottom': '60px'}
        style_name = {'text-align': 'center', 'font-size': '1.25em', 'line-height': '200%', 'width': '300px',}

        layout = html.Div(
            [
                html.Details(
                    [
                        html.Summary('Simulation', style=style_name_summary),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Label('Asset', style=style_name),
                                        dcc.Dropdown(
                                            id='info_asset_mode',
                                            options=[
                                                {'label': 'Wind', 'value': 'wind'},
                                                {'label': 'Solar', 'value': 'solar'},
                                                {'label': 'Battery', 'value': 'battery'},
                                                {'label': 'Wind-Solar', 'value': 'wind_and_solar'},
                                                {'label': 'Wind-Battery', 'value': 'wind_and_battery'},
                                                {'label': 'Solar-Battery', 'value': 'solar_and_battery'},
                                                # {'label': 'Solar and dcBattery', 'value': 'solar_and_dc_battery'},
                                                # {'label': 'Wind + Solar and Battery', 'value': 'wind_solar_and_battery'},
                                                # {'label': 'Wind + Solar and dcBattery', 'value': 'wind_solar_and_dc_battery'},
                                                # {'label': 'Solar + Wind and Battery', 'value': 'solar_wind_and_battery'},
                                                {'label': 'Wind-Solar-Battery', 'value': 'wind_and_solar_and_battery'},

                                            ],
                                            value=self.asset_mode,
                                            style=style_m_bottom
                                        ),
                                    ],
                                    style={'display': 'inline-block'}
                                ),
                            ],
                            style=style_box
                        ),

                        html.Div(
                            [
                                html.Label('POI [kW] :', style=style_label),
                                dcc.Input(id='info_asset_poi', value=self.poi_asset, type='number',
                                          style=style_input)
                            ],

                            style={'display': 'flex'}
                        ),
                    ],
                    open=False,
                    style={'margin-top': '20px', 'border': '1.5px solid lightgray'}
                ),
            ],
            style={'padding': '10px'}
        )

        return layout


