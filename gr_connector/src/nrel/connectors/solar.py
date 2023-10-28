from gr_connector.src.nrel.database.resource.query import NREL_RESOURCE
from gr_comun.src.renewable.solar.msg import SolarMSG as Smsg
# from gr_comun.src.renewable.solar.
import numpy as np



class Solar:
    """
    This object is a
    """
    def __init__(self,
                 ts_from=None,
                 ts_to=None,
                 lon=None,
                 lat=None,
                 solar_park=None):
        self.start = ts_from
        self.end = ts_to
        self.lon = lon
        self.lat = lat
        self.solar_park = solar_park
        self.var = 'ghi'

    def get_wind_factor(self):

        resource = (NREL_RESOURCE(ts_from=self.start,
                                  ts_to=self.end
                                  )
                    .get_resource(var=self.var,
                                  lat=self.lat,
                                  lon=self.lon
                                  )
                    )

        nrel_height = 10
        power_law_exponent = 0.4  # https://en.wikipedia.org/wiki/Wind_gradient calibrar el Wind
        hub_height = self.solar_park.hubheight
        factor = (hub_height / nrel_height) ** power_law_exponent

        df_wind_speed = resource.df()
        df_wind_speed['wind_speed_hub_height'] = factor * df_wind_speed[Wmsg.WS]


        df_ws = WindFarm(ts_windspeed=df_wind_speed,
                         wind_turbine=self.wind_turbine).get_capacity_factor()

        df = self.post_process_wind(df=df_ws)

        return df

    def post_process_wind(self, df=None):

        columns_to_keep = ['local_datetime', 'wind']  # Replace with your actual column names
        df = df[columns_to_keep]

        return df

class NREL_SOLAR:
    """
    :param name:
    :returns df:
    """

    def __init__(self, df_panel=None, df_resource=None):
        self.df_panel = df_panel
        self.df_resource = df_resource

    # def get_solar_factor(self):
    #     panel_eff_area = self.df_panel['solar_panel_area'][0] * self.df_panel['solar_panel_eff'][0] / 100
    #
    #     df = self.df_resource
    #
    #     df['watt'] = df['ghi'] * panel_eff_area
    #     panel_watt = max(df['watt'])
    #
    #     UNIT = 1e3
    #     panel_quantity_per_kw = UNIT / panel_watt
    #     df['solar'] = df['watt'] * panel_quantity_per_kw / UNIT
    #
    #     df = self.post_process_solar(df=df)
    #
    #     return df
    #
    # def post_process_solar(self, df=None):
    #
    #     columns_to_keep = ['local_datetime', 'solar']  # Replace with your actual column names
    #     df = df[columns_to_keep]
    #
    #     return df