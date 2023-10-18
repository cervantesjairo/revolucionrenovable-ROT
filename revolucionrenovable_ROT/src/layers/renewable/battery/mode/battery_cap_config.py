from dash import dcc, html
from dash.dependencies import Input, Output, State


class BatteryCapConf:
    def __init__(self):
        self.battery_duration_fix = 4
        self.battery_duration_ub_max = 8
        self.battery_duration_lb_min = 0
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
                        html.Summary('Battery Duration Config', style=style_name_summary),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Checklist(
                                            id='battery_duration_mode',
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
                                        html.Div([html.Label('Duration [h]: ', style=style_box_name),
                                               dcc.Input(id='battery_duration_fix', value=self.battery_duration_fix,
                                                         type='number', style=style_box_value,), ],
                                              id='fix-duration-div',
                                              style={'display': 'none'}
                                                 ),
                                        html.Div(
                                         [html.Label('Upper Bound [h]: ', style=style_box_name),
                                          dcc.Input(id='battery_duration_ub_max', value=self.battery_duration_ub_max, type='number', style=style_box_value,), ],
                                         id='opt-bat-dur-ub-div',
                                         style={'display': 'none'}
                                        ),
                                        html.Div(
                                         [html.Label('Lower Bound [h]: ', style=style_box_name),
                                          dcc.Input(id='battery_duration_lb_min', value=self.battery_duration_lb_min, type='number', style=style_box_value,), ],
                                         id='opt-bat-dur-lb-div',
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
            Output('fix-duration-div', 'style'),
            Output('opt-bat-dur-ub-div', 'style'),
            Output('opt-bat-dur-lb-div', 'style'),
            Input('battery_duration_mode', 'value')
        )
        def toggle_inputs(battery_duration_mode):
            if 'range' in battery_duration_mode:
                return {'display': 'none'}, {'display': 'block'}, {'display': 'block'}
            elif 'fix' in battery_duration_mode:
                return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
            else:
                return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

        @app.callback(
            Output('battery_duration_mode', 'value'),
            Input('battery_duration_mode', 'value')
        )
        def update_checklist_value(value):
            if len(value) > 1:
                value = value[-1:]
            return value
