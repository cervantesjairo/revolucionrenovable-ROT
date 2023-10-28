from dash import dcc, html


class CashFlow:

    def __init__(self):
        self.planning_horizon = 10  ### yr
        self.interest_rate = 7  ### %
        self.layout = self.setup_layout()

    def setup_layout(self):
        style_name_summary = {
            'text-align': 'center',
            'font-size': '1.5em',
            'line-height': '200%',
        }

        style_label = {
            'display': 'inline-block',
            'margin-right': '0px',
            'text-align': 'right',
            'width': '220px',
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
                            html.Summary('Financial', style=style_name_summary),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Label('Planning Horizon [yr] :', style=style_label),
                                            dcc.Input(id='planning_horizon', value=self.planning_horizon, type='number', style=style_input)
                                        ], style={'display': 'flex'}),

                                    html.Div(
                                        [
                                            html.Label('Interest Rate [%] :', style=style_label),
                                            dcc.Input(id='interest_rate', value=self.interest_rate, type='number', style=style_input)
                                        ], style={'display': 'flex'}),
                                ], style={'padding': '10px'})

                        ], open=False, style={'margin-top': '20px', 'border': '1px solid lightgray'})
                ], style={'padding': '10px'})

        return layout
