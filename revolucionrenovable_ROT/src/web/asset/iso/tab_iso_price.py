from dash import dcc, html
from dash.dependencies import Input, Output, State


class ChiquiCaisoPrice:
    def __init__(self):
        # self.panel_name = 'jinko500'
        self.layout = self.setup_layout()

    def setup_layout(self):
        ui_iso_price_variables = [
            {'label': 'DA_NP15', 'value': 'TH_NP15_GEN-APND'},
            {'label': 'DA_SP15', 'value': ''},
            {'label': 'DA_ZP26', 'value': ''},
            {'label': 'RT_NP15', 'value': ''},
            {'label': 'RT_SP15', 'value': ''},
            {'label': 'RT_ZP26', 'value': ''},
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
                        html.Summary('CAISO Prices', style=style_name_summary),
                        html.Div(
                            [
                                        html.Br(),
                                        html.H3('Locational Marginal Price (LMP) [$/MWh]', style={'text-align': 'center', 'fontSize': '1.25em',
                                                                    'line-height': '200%'}),
                                        dcc.Dropdown(
                                            id='iso_price_dropdown_var',
                                            options=ui_iso_price_variables,
                                            value=['TH_NP15_GEN-APND'],
                                            multi=True,
                                            placeholder='Select One or Multiple Options'
                                        ),

                            ]
                        )
                    ], open=False, style={'margin-top': '20px', 'border': '1.5px solid lightgray'}
                )
            ], style={'padding': '10px'}
        )
        return layout
