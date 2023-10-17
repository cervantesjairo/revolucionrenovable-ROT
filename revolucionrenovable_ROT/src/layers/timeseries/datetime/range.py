from dash import dcc, html
from datetime import datetime


class DateTimeRange:
    def __init__(self):
        self.start_date = datetime(2021, 1, 1)
        self.end_date = datetime(2021, 1, 10)
        self.layout = self.setup_layout()

    def setup_layout(self):
        style_name_summary = {
            'text-align': 'center',
            'font-size': '1.5em',
            'line-height': '200%',
        }

        layout = \
            html.Div(
                [
                    html.Details(
                        [
                            html.Summary('Date Range', style=style_name_summary),
                            html.Div(
                                [
                                    dcc.DatePickerRange(
                                        id='date_range',
                                        start_date=self.start_date,
                                        end_date=self.end_date,
                                        style={
                                            'margin': '5px',
                                            'text-align': 'center',
                                            'font-size': '1.2em',
                                        }
                                    )

                                ], style={'float': 'center'})

                        ], open=False, style={'margin-top': '20px', 'text-align': 'center', 'border': '1px solid lightgray'})
                ], style={'padding': '10px'})

        return layout
