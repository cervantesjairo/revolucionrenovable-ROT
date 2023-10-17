from dash import dcc, html


class SolarElec:

    def __init__(self):
        self.solar_panel_area = 1.92
        self.solar_panel_eff = 20
        self.solar_panel_degradation = 3
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
                            html.Summary('Panel Characteristics', style=style_name_summary),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Label('Area [m2]: ', style=style_label),
                                            dcc.Input(id='solar_panel_area', value=self.solar_panel_area, type='number', style=style_input)
                                        ], style={'display': 'flex'}),

                                    html.Div(
                                        [
                                            html.Label('Efficiency [%]: ', style=style_label),
                                            dcc.Input(id='solar_panel_eff', value=self.solar_panel_eff, type='number', style=style_input)
                                        ], style={'display': 'flex'}),

                                    html.Div(
                                        [
                                            html.Label('Degradation [%]: ', style=style_label),
                                            dcc.Input(id='solar_panel_degradation', value=self.solar_panel_degradation, type='number', style=style_input)
                                        ], style={'display': 'flex'}),

                                ], style={'padding': '10px'})

                        ], open=False, style={'margin-top': '20px', 'border': '1px solid lightgray'})
                ], style={'padding': '10px'})

        return layout
