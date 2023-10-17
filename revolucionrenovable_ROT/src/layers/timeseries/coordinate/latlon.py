from dash.dependencies import Input, Output, State
from dash import dcc, html
# import pandas as pd
import dash_leaflet as dl


class LatLon:

    def __init__(self):
        self.marker_lat = 34#43.4822# 5.6155
        self.marker_lon = -120#-95.508728#-73.8132
        self.latitude = self.marker_lat
        self.longitude = self.marker_lon
        self.layout = self.setup_layout()

    def setup_layout(self):
        style_name = {'text-align': 'center', 'font-size': '1.5em', 'line-height': '200%'}
        input_style = {'width': '50%', 'text-align': 'center', 'display': 'inline-block', 'margin-top': '20px'}

        api_key = 'dffda0ad506f7453673ccc469b55235a'
        tile_url = f"https://tile.openweathermap.org/map/precipitation_new/{{z}}/{{x}}/{{y}}.png?appid={api_key}"
        wind_layer = dl.TileLayer(url=tile_url, attribution='Map data © OpenWeatherMap')

        map_component = dl.Map(
            id='map',
            center=[self.marker_lat, self.marker_lon],
            zoom=5,
            style={'width': '100%', 'height': '550px'},
            children=[
                dl.TileLayer(),
                wind_layer,

                dl.Marker(
                    position=[self.marker_lat, self.marker_lon],
                    draggable=True,
                    id='marker',
                    children=dl.Tooltip('Drag me!')
                )
            ]
        )

        layout = html.Div([
            html.Details([
                html.Summary('Location', style=style_name),
                html.Div([
                    html.Div([
                        html.Label('Latitude: ', style={'font-size': '1.3em', 'margin-left': '230px'}),
                        dcc.Input(id='lat', type='number', value=self.latitude, style={
                            'width': '130px',
                            'text-align': 'center',
                            'font-size': '1.1em',
                        }),
                    ], style=input_style),

                    html.Div([
                        html.Label('Longitude: ', style={'font-size': '1.3em'}),
                        dcc.Input(id='lon', type='number', value=self.longitude, style={
                            'width': '130px',
                            'text-align': 'center',
                            'font-size': '1.1em',
                            'margin-right': '200px'
                        }),
                    ], style=input_style),
                ], style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center',
                          'justify-content': 'center', 'margin-bottom': '20px'}),

                html.Div([map_component])
            ], open=True, style={'margin-top': '20px', 'text-align': 'center', 'border': '1.5px solid lightgray'}),

        ], style={'padding': '10px'})

        return layout

    def setup_callbacks(self, app):
        @app.callback(
            Output('marker', 'position'),
            [Input('lat', 'value'),
             Input('lon', 'value')])
        def update_marker(lat, lon):
            return [lat, lon]

        @app.callback(
            [Output('lat', 'value'),
             Output('lon', 'value'),
             Output('map', 'center')],
            [Input('marker', 'position')],
            [State('lat', 'value'),
             State('lon', 'value')])
        def update_inputs(marker_position, latitude, longitude):
            if marker_position:
                latitude, longitude = marker_position
                return round(latitude, 4), round(longitude, 4), marker_position
            else:
                return latitude, longitude, [self.marker_lat, self.marker_lon]
