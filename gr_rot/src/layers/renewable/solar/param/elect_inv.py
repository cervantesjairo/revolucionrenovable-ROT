from dash import dcc, html


class InvElec:

    def __init__(self):
        self.solar_inv_eff = 95
        self.solar_inv_pre_loss = 2
        self.solar_inv_post_loss = 5
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
                            html.Summary('Inverter Characteristics', style=style_name_summary),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Label('Efficiency: ', style=style_label),
                                            dcc.Input(id='solar_inv_eff', value=self.solar_inv_eff, type='number', style=style_input)
                                        ], style={'display': 'flex'}),

                                    html.Div(
                                        [
                                            html.Label('Pre Inverter Loss [%]: ', style=style_label),
                                            dcc.Input(id='solar_inv_pre_loss', value=self.solar_inv_pre_loss, type='number', style=style_input)
                                        ], style={'display': 'flex'}),

                                    html.Div(
                                        [
                                            html.Label('Post Inverter Loss[%]: ', style=style_label),
                                            dcc.Input(id='solar_inv_post_loss', value=self.solar_inv_post_loss, type='number', style=style_input)
                                        ], style={'display': 'flex'}),

                                ], style={'padding': '10px'})

                        ], open=False, style={'margin-top': '20px', 'border': '1px solid lightgray'})
                ], style={'padding': '10px'})

        return layout
