from gr_comun.src.renewable.wind.msg import WindMSG as Wmsg
from dash import dcc, html


class WindTurb:

    def __init__(self):
        # Clipper C96 -> https://geosci.uchicago.edu/~moyer/GEOS24705/Readings/Liberty_Brochure_2009_LR.pdf
        self.wind_turbine_rated_power = 2500    # kW
        self.wind_turbine_rotor_diameter = 96   # m
        self.wind_turbine_hub_height = 80       # m
        self.wind_turbine_v_cut_in = 3.5        # m/s
        self.wind_turbine_v_rated = 15          # m/s
        self.wind_turbine_v_cut_out = 25        # m/s
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
                            html.Summary('Turbine Characteristics', style=style_name_summary),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Label('Rated Power [kW]: ', style=style_label),
                                            dcc.Input(id=Wmsg.WT_RP,
                                                      value=self.wind_turbine_rated_power,
                                                      type='number',
                                                      style=style_input)
                                        ], style={'display': 'flex'}),

                                    html.Div(
                                        [
                                            html.Label('Rotor Diameter [m]: ', style=style_label),
                                            dcc.Input(id=Wmsg.WT_RD,
                                                      value=self.wind_turbine_rotor_diameter,
                                                      type='number',
                                                      style=style_input)
                                        ], style={'display': 'flex'}),

                                    html.Div(
                                        [
                                            html.Label('Hub Height [m]: ', style=style_label),
                                            dcc.Input(id=Wmsg.WT_HH,
                                                      value=self.wind_turbine_hub_height,
                                                      type='number',
                                                      style=style_input)
                                        ], style={'display': 'flex'}),

                                    html.Div(
                                        [
                                            html.Label('Cut-in Wind Speed [m/s]: ', style=style_label),
                                            dcc.Input(id=Wmsg.WT_VI,
                                                      value=self.wind_turbine_v_cut_in,
                                                      type='number',
                                                      style=style_input)
                                        ], style={'display': 'flex'}),

                                    html.Div(
                                        [
                                            html.Label('Rated Wind Speed [m/s]: ', style=style_label),
                                            dcc.Input(id=Wmsg.WT_VR,
                                                      value=self.wind_turbine_v_rated,
                                                      type='number',
                                                      style=style_input)
                                        ], style={'display': 'flex'}),

                                    html.Div(
                                        [
                                            html.Label('Cut-out Wind Speed [m/s]: ', style=style_label),
                                            dcc.Input(id=Wmsg.WT_VO,
                                                      value=self.wind_turbine_v_cut_out,
                                                      type='number',
                                                      style=style_input)
                                        ], style={'display': 'flex'}),

                                ], style={'padding': '10px'})

                        ], open=False, style={'margin-top': '20px', 'border': '1px solid lightgray'})
                ], style={'padding': '10px'})

        return layout
