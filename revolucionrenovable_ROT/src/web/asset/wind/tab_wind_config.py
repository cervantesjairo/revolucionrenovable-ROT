from dash import dcc, html
from dash.dependencies import Input, Output, State


class WindConf:
    def __init__(self):
        self.wind_turbine_name = 'jinko500'
        self.wind_size_fix = 100
        self.wind_size_lb_min = 10
        self.wind_size_ub_max = 500
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
                        html.Summary('Wind Size Config', style=style_name_summary),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Checklist(
                                            id='wind_size_mode',
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
                                        html.Div([html.Label('Size [kW]: ', style=style_box_name),
                                               dcc.Input(id='wind_size_fix', value=self.wind_size_fix,
                                                         type='number', style=style_box_value,), ],
                                              id='fix-wind_size_mode-div',
                                              style={'display': 'none'}
                                                 ),
                                        html.Div(
                                         [html.Label('Upper Bound [kW]: ', style=style_box_name),
                                          dcc.Input(id='wind_size_ub_max', value=self.wind_size_ub_max, type='number', style=style_box_value,), ],
                                         id='opt-wind_size_mode-ub-div',
                                         style={'display': 'none'}
                                        ),
                                        html.Div(
                                         [html.Label('Lower Bound [kW]: ', style=style_box_name),
                                          dcc.Input(id='wind_size_lb_min', value=self.wind_size_lb_min, type='number', style=style_box_value,), ],
                                         id='opt-wind_size_mode-lb-div',
                                         style={'display': 'none'}
                                        ),
                                     ]
                                )
                            ]
                        )
                    ], open=False, style={'margin-top': '20px', 'border': '1.5px solid lightgray'}
                )
            ], style={'padding': '10px'}
        )
        return layout

    def setup_callbacks(self, app):
        @app.callback(
            Output('fix-wind_size_mode-div', 'style'),
            Output('opt-wind_size_mode-ub-div', 'style'),
            Output('opt-wind_size_mode-lb-div', 'style'),
            Input('wind_size_mode', 'value')
        )
        def toggle_inputs(wind_size_mode):
            if 'range' in wind_size_mode:
                return {'display': 'none'}, {'display': 'block'}, {'display': 'block'}
            elif 'fix' in wind_size_mode:
                return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
            else:
                return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

        @app.callback(
            Output('wind_size_mode', 'value'),
            Input('wind_size_mode', 'value')
        )
        def update_checklist_value(value):
            if len(value) > 1:
                value = value[-1:]
            return value
