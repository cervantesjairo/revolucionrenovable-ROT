from dash import dcc, html


class WindCapex:

    def __init__(self):
        self.wind_cost = 1500
        self.wind_cost_inter = 0
        self.layout = self.setup_layout()

    def setup_layout(self):
        style_name_summary = {
            'text-align': 'center',
            'font-size': '1.5em',
            'line-height': '200%',
        }

        style_label = {
            'display': 'inline-block',
            'margin-right': '5px',
            'text-align': 'right',
            'width': '210px',
            'font-size': '1.3em',
        }

        style_input = {
            'display': 'inline-block',
            'margin-left': '0px',
            'margin-bottom': '10px',
            'width': '90px',
            'text-align': 'center',
            'font-size': '1.1em',
        }

        layout = \
            html.Div(
                [
                    html.Details(
                        [
                            html.Summary('Capital Expenditure', style=style_name_summary),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Label('Wind Cost [$/kW]: ', style=style_label),
                                            dcc.Input(id='wind_cost', value=self.wind_cost, type='number', style=style_input)
                                        ], style={'display': 'flex'}),

                                    html.Div(
                                        [
                                            html.Label('Wind Interconnection Cost [$/kWac]: ', style=style_label),
                                            dcc.Input(id='wind_cost_inter', value=self.wind_cost_inter, type='number', style=style_input)
                                        ], style={'display': 'flex'}),


                                ], style={'padding': '10px'})

                        ], open=False, style={'margin-top': '20px', 'border': '1px solid lightgray'})
                ], style={'padding': '10px'})

        return layout
