from dash import dcc, html


class SolarCapex:

    def __init__(self):
        self.solar_cost_panel = 300
        self.solar_cost_inverter = 215
        self.solar_cost_bos = 260
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
                                            html.Label('Panel Cost [$/kWdc]: ', style=style_label),
                                            dcc.Input(id='solar_cost_panel', value=self.solar_cost_panel, type='number', style=style_input)
                                        ], style={'display': 'flex'}),

                                    html.Div(
                                        [
                                            html.Label('Inverter Cost [$/kWac]: ', style=style_label),
                                            dcc.Input(id='solar_cost_inverter', value=self.solar_cost_inverter, type='number', style=style_input)
                                        ], style={'display': 'flex'}),

                                    html.Div(
                                        [
                                            html.Label('Other BoS [$/kWdc]: ', style=style_label),
                                            dcc.Input(id='solar_cost_bos', value=self.solar_cost_bos, type='number', style=style_input)
                                        ], style={'display': 'flex'}),

                                ], style={'padding': '10px'})

                        ], open=False, style={'margin-top': '20px', 'border': '1px solid lightgray'})
                ], style={'padding': '10px'})

        return layout
