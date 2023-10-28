from dash import dcc, html
from gr_rot.src.web.tab_asset.tab_solar.tab_solar import TabSolar
from gr_rot.src.web.tab_asset.tab_storage.tab_battery import TabBattery
from gr_rot.src.web.tab_asset.tab_wind.tab_wind import TabWind
from gr_rot.src.web.tab_asset.tab_iso.iso import TabISO


class Asset:
    def __init__(self):
        self.layout = self.setup_layout()

    def setup_layout(self):
        style = \
            {
                'border': '2px solid black',
                'backgroundColor': 'transparent',
                'color': 'black',
                'borderRadius': '24px 24px 24px 24px',
                'fontSize': '18px',
                'height': '55px',
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center'
            }

        selected_style = \
            {
                'backgroundColor': '#c0c0c0',
                'color': 'black',
                'border': '2px solid black',
                'borderRadius': '24px 24px 24px 24px',
                'fontWeight': 'bold',
                'fontSize': '20px',
                'height': '55px',
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center'}

        layout = \
            html.Div(
                [dcc.Tabs(
                    [
                        dcc.Tab(label='Solar', children=[TabSolar().layout], style=style, selected_style=selected_style),
                        dcc.Tab(label='Wind', children=[TabWind().layout], style=style, selected_style=selected_style),
                        dcc.Tab(label='Storage', children=[TabBattery().layout], style=style, selected_style=selected_style),
                        dcc.Tab(label='ISO', children=[TabISO().layout], style=style, selected_style=selected_style),
                        # dcc.Tab(label='Grid', children=[], style=style, selected_style=selected_style)
                     ], vertical=False,
                )
                ]
            )

        return layout
