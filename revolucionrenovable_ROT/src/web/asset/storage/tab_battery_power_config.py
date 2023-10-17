from dash import dcc, html
from dash.dependencies import Input, Output, State

class ChiquiBatteryPowerConf:
    def __init__(self):
        self.battery_name = 'Name'
        self.battery_power_fix = 100
        self.battery_power_lb_min = 0
        self.battery_power_ub_max = 500
        self.layout = self.setup_layout()

    def setup_layout(self):
        style_name_summary = {
            'text-align': 'center',
            'font-size': '1.5em',
            'line-height': '200%',
        }
        style_checklist = {'text-align': 'center',
                           'font-size': '1.25em',
                           'line-height': '200%',
                           'display': 'flex',
                           'flex-direction': 'row',
                           'justify-content': 'space-around',
                           'margin-bottom': '10px'}

        style_box_name = {
            'width': '200px',
            'margin-right': '5px',
            'text-align': 'right',
            'font-size': '1.3em',
            'display': 'inline-block',
        }
        style_box_value = {'display': 'inline-block',
                           'margin': '0px',
                           'margin-bottom': '10px',
                           'width': '100px',
                           'text-align': 'center',
                           'font-size': '1.1em'}

        layout = html.Div(
            [
                html.Details(
                    [
                        html.Summary('Battery Power Config', style=style_name_summary),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Checklist(
                                            id='battery_power_mode',
                                            options=[
                                                {'label': 'Fix', 'value': 'fix'},
                                                {'label': 'Range', 'value': 'range'}
                                            ],
                                            value=['fix'],
                                            style=style_checklist
                                        )
                                    ],
                                ),
                                html.Div(
                                    [
                                        html.Div([html.Label('Power Size [kW]: ', style=style_box_name),
                                               dcc.Input(id='battery_power_fix', value=self.battery_power_fix,
                                                         type='number', style=style_box_value,), ],
                                              id='fix-power-div',
                                              style={'display': 'none'}
                                                 ),
                                        html.Div(
                                         [html.Label('Upper Bound [kW]: ', style=style_box_name),
                                          dcc.Input(id='battery_power_ub_max', value=self.battery_power_ub_max, type='number', style=style_box_value,), ],
                                         id='opt-bat-ub-div',
                                         style={'display': 'none'}
                                        ),
                                        html.Div(
                                         [html.Label('Lower Bound [kW]: ', style=style_box_name),
                                          dcc.Input(id='battery_power_lb_min', value=self.battery_power_lb_min, type='number', style=style_box_value,), ],
                                         id='opt-bat-lb-div',
                                         style={'display': 'none'}
                                        ),
                                     ]
                                )
                            ]
                        )
                    ], open=True, style={'margin-top': '20px', 'border': '1.5px solid lightgray'}
                )
            ], style={'padding': '10px'}
        )
        return layout

    def setup_callbacks(self, app):
        @app.callback(
            Output('fix-power-div', 'style'),
            Output('opt-bat-lb-div', 'style'),
            Output('opt-bat-ub-div', 'style'),
            Input('battery_power_mode', 'value')
        )
        def toggle_inputs(battery_power_mode):
            if 'range' in battery_power_mode:
                return {'display': 'none'}, {'display': 'block'}, {'display': 'block'}
            elif 'fix' in battery_power_mode:
                return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
            else:
                return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

        @app.callback(
            Output('battery_power_mode', 'value'),
            Input('battery_power_mode', 'value')
        )
        def update_checklist_value(value):
            if len(value) > 1:
                value = value[-1:]
            return value