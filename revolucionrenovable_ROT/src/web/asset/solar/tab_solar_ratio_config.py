from dash import dcc, html
from dash.dependencies import Input, Output, State

class ChiquiSolarRatioConf:
    def __init__(self):
        self.panel_name = 'jinko500'
        self.solar_ratio_fix = 1.25
        self.solar_ratio_lb_min = 1
        self.solar_ratio_ub_max = 1.5
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
            'margin-right': '0px',
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
                        html.Summary('DC/AC Ratio', style=style_name_summary),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Checklist(
                                            id='solar_ratio_mode',
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
                                    [html.Div(
                                        [html.Label('Ratio: ', style=style_box_name),
                                         dcc.Input(id='solar_ratio_fix', value=self.solar_ratio_fix, type='number', style=style_box_value,), ],
                                              id='fix-ratio-div',
                                              style={'display': 'none'}
                                              ),
                                        html.Div(
                                            [html.Label('Ratio Upper Bound : ', style=style_box_name),
                                          dcc.Input(id='solar_ratio_ub_max', value=self.solar_ratio_ub_max, type='number', style=style_box_value,), ],
                                         id='opt-ub-ratio-div',
                                         style={'display': 'none'}
                                        ),
                                        html.Div(
                                            [html.Label('Ratio Lower Bound : ', style=style_box_name),
                                             dcc.Input(id='solar_ratio_lb_min', value=self.solar_ratio_lb_min, type='number',
                                                       style=style_box_value, ), ],
                                            id='opt-lb-ratio-div',
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
            Output('fix-ratio-div', 'style'),
            Output('opt-ub-ratio-div', 'style'),
            Output('opt-lb-ratio-div', 'style'),
            Input('solar_ratio_mode', 'value')
        )
        def toggle_inputs(solar_ratio_mode):
            if 'range' in solar_ratio_mode:
                return {'display': 'none'}, {'display': 'block'}, {'display': 'block'}
            elif 'fix' in solar_ratio_mode:
                return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
            else:
                return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

        @app.callback(
            Output('solar_ratio_mode', 'value'),
            Input('solar_ratio_mode', 'value')
        )
        def update_checklist_value(value):
            if len(value) > 1:
                value = value[-1:]
            return value