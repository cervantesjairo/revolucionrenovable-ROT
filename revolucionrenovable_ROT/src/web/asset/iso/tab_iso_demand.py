from dash import dcc, html
from dash.dependencies import Input, Output, State


class IsoDemand:
    def __init__(self):
        self.iso_demand_size_factor = 1
        self.layout = self.setup_layout()

    def setup_layout(self):
        ui_iso_demand_variables = [
            {'label': 'ACTUAL', 'value': 'demand_actual'},
        ]


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
                        html.Summary('CAISO Demand', style=style_name_summary),
                        html.Div(
                            [
                                html.Br(),
                                html.H3('Transmission Access Charges (TAC) Load [MW]',
                                        style={'text-align': 'center', 'fontSize': '1.25em', 'line-height': '200%'}),
                                dcc.Dropdown(
                                    id='iso_demand_dropdown_var',
                                    options=ui_iso_demand_variables,
                                    multi=True,
                                    placeholder='Selecciona una o varias opciones'
                                ),
                            ]
                        )
                    ],
                    open=False,
                    style={'margin-top': '20px', 'border': '1.5px solid lightgray'}
                ),
                html.Div(
                    [
                        html.Br(),  # Adding a line break
                        html.Label('Load Size Sample [MW]:', style={'fontSize': '1em'}),  # Adding a label for the input
                        dcc.Input(
                            id='iso_demand_size_factor',
                            value=self.iso_demand_size_factor,
                            type='number',  # Set the input type to number
                            placeholder='Enter load size'
                        ),
                    ],
                    style={'margin-top': '20px', 'border': '1.5px solid lightgray', 'padding': '10px'}
                ),
            ],
            style={'padding': '10px'}
        )

        return layout
