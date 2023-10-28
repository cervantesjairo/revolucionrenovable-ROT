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
        df_scf = self.solar_msg(df=scf)

        return df_scf

    def solar_msg(self, df=None):
        col_msg = [Smsg.DT_UTC, Smsg.DT_FROM, Smsg.DT_TO, Smsg.SCF]
        df = df[col_msg]

        return df
