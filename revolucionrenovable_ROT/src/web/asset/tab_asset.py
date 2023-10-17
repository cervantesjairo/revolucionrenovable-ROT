from dash import dcc, html
from revolucionrenovable_ROT.src.web.asset.solar.tab_solar import TabSolar
from revolucionrenovable_ROT.src.web.asset.storage.tab_battery import TabBattery
from revolucionrenovable_ROT.src.web.asset.wind.tab_wind import TabWind
from revolucionrenovable_ROT.src.web.asset.iso.tab_iso import TabISO


class TabAsset:
    def __init__(self):
        self.tab_solar = TabSolar()
        self.tab_battery = TabBattery()
        self.tab_wind = TabWind()
        self.tab_iso = TabISO()
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
                        dcc.Tab(label='Solar', children=[self.tab_solar.layout], style=style, selected_style=selected_style),
                        dcc.Tab(label='Wind', children=[self.tab_wind.layout], style=style,
                                selected_style=selected_style),
                        dcc.Tab(label='Storage', children=[self.tab_battery.layout], style=style, selected_style=selected_style),
                        dcc.Tab(label='ISO', children=[self.tab_iso.layout], style=style, selected_style=selected_style),
                        # dcc.Tab(label='Grid', children=[], style=style, selected_style=selected_style)
                     ], vertical=False,
                )
                ]
            )

        return layout
