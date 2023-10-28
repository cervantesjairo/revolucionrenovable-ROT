from gr_connector.src.nrel.database.resource.query import NREL_RESOURCE
from gr_comun.src.renewable.solar.msg import SolarMSG as Smsg
from gr_comun.src.renewable.solar.object.solarpark import SolarPark
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
                 solar_park: SolarPark = None):
        self.start = ts_from
        self.end = ts_to
        self.lon = lon
        self.lat = lat
        self.solar_park = solar_park
        self.var = 'ghi'

    def get_solar_cap_factor(self):

        resource = (NREL_RESOURCE(ts_from=self.start,
                                  ts_to=self.end
                                  )
                    .get_resource(var=self.var,
                                  lat=self.lat,
                                  lon=self.lon
                                  )
                    )

        sp = self.solar_park
        scf = sp.cap_factor(ts_solar=resource)

        #
        # df_scf = self.solar_msg(df=scf)

        return sp #df_scf

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