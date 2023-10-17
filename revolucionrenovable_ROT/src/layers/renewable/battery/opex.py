from dash import dcc, html


class BatteryOpex:

    def __init__(self):
        self.battery_cost_fix = 0.0025
        self.battery_cost_variable = 10
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
                            html.Summary('O&M Expenditure', style=style_name_summary),
                            html.Div(
                                [

                                    html.Div(
                                        [
                                            html.Label('Fix [$/kW-yr]: ', style=style_label),
                                            dcc.Input(id='battery_cost_variable', value=self.battery_cost_variable, type='number', style=style_input)
                                        ], style={'display': 'flex'}),

                                    html.Div(
                                        [
                                            html.Label('Variable [$/kWh]: ', style=style_label),
                                            dcc.Input(id='battery_cost_fix', value=self.battery_cost_fix, type='number',
                                                      style=style_input)
                                        ], style={'display': 'flex'}),

                                ], style={'padding': '10px'})

                        ], open=False, style={'margin-top': '20px', 'border': '1px solid lightgray'})
                ], style={'padding': '10px'})

        return layout
