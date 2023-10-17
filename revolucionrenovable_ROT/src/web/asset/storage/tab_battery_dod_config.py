from dash import dcc, html
from dash.dependencies import Input, Output, State

class ChiquiBatteryDoDConf:
    def __init__(self):
        self.battery_dod_lb_min = 0
        self.battery_dod_ub_max = 100
        self.layout = self.setup_layout()

    def setup_layout(self):
        style_name_summary = {
            'text-align': 'center',
            'font-size': '1.5em',
            'line-height': '200%',
        }
        style_checklist = {
            'text-align': 'center',
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
                        html.Summary('Depth of Discharge Config', style=style_name_summary),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Checklist(
                                            id='battery_dod_mode',
                                            options=[
                                                {'label': 'Unrestricted', 'value': 'unrestricted'},
                                                {'label': 'Range', 'value': 'range'}
                                            ],
                                            value=['unrestricted'],
                                            style=style_checklist
                                        )
                                    ],
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                         [html.Label('Min DoD [%] : ', style=style_box_name),
                                          dcc.Input(id='battery_dod_lb_min', value=self.battery_dod_lb_min, type='number', style=style_box_value,), ],
                                         id='range-bat-dod-min-div',
                                         style={'display': 'none'}
                                        ),
                                        html.Div(
                                         [html.Label('Max DoD [%] : ', style=style_box_name),
                                          dcc.Input(id='battery_dod_ub_max', value=self.battery_dod_ub_max, type='number', style=style_box_value,), ],
                                         id='range-bat-dod-max-div',
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
            Output('range-bat-dod-min-div', 'style'),
            Output('range-bat-dod-max-div', 'style'),
            Input('battery_dod_mode', 'value')
        )
        def toggle_inputs(battery_dod_mode):
            if 'range' in battery_dod_mode:
                return {'display': 'block'}, {'display': 'block'}
            else:
                return {'display': 'none'}, {'display': 'none'}

        @app.callback(
            Output('battery_dod_mode', 'value'),
            Input('battery_dod_mode', 'value')
        )
        def update_checklist_value(value):
            if len(value) > 1:
                value = value[-1:]
            return value
