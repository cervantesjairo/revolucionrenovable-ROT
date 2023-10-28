from dash import dcc, html
from dash.dependencies import Input, Output, State


class SolarInvConf:
    def __init__(self):
        self.panel_name = 'jinko500'
        self.solar_size_fix = 100
        self.solar_size_lb_min = 0
        self.solar_size_ub_max = 200
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
                        html.Summary('Inverter Configuration', style=style_name_summary),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Checklist(
                                            id='solar_inverter_mode',
                                            options=[
                                                {'label': 'Fix', 'value': 'fix'},
                                                {'label': 'Optimize', 'value': 'range'}
                                            ],
                                            value=['fix'],
                                            style=style_checklist
                                        )
                                    ],
                                ),
                                html.Div(
                                    [
                                        html.Div([html.Label('Size [kW]: ', style=style_box_name),
                                               dcc.Input(id='solar_size_fix', value=self.solar_size_fix,
                                                         type='number', style=style_box_value,), ],
                                              id='fix-size-div',
                                              style={'display': 'none'}
                                                 ),
                                        html.Div(
                                         [html.Label('Upper Bound [kW]: ', style=style_box_name),
                                          dcc.Input(id='solar_size_ub_max', value=self.solar_size_ub_max, type='number', style=style_box_value,), ],
                                         id='optimize-ub-div',
                                         style={'display': 'none'}
                                        ),
                                        html.Div(
                                         [html.Label('Lower Bound [kW]: ', style=style_box_name),
                                          dcc.Input(id='solar_size_lb_min', value=self.solar_size_lb_min, type='number', style=style_box_value,), ],
                                         id='optimize-lb-div',
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
            Output('fix-size-div', 'style'),
            Output('optimize-ub-div', 'style'),
            Output('optimize-lb-div', 'style'),
            Input('solar_inverter_mode', 'value')
        )
        def toggle_inputs(solar_inverter_mode):
            if 'range' in solar_inverter_mode:
                return {'display': 'none'}, {'display': 'block'}, {'display': 'block'}
            elif 'fix' in solar_inverter_mode:
                return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
            else:
                return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

        @app.callback(
            Output('solar_inverter_mode', 'value'),
            Input('solar_inverter_mode', 'value')
        )
        def update_checklist_value(value):
            if len(value) > 1:
                value = value[-1:]
            return value