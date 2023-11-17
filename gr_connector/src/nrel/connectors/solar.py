from gr_connector.src.nrel.database.resource.query import NREL_RESOURCE
from gr_comun.src.renewable.solar.object.msg import SolarMSG as Smsg
from gr_comun.src.renewable.solar.solarpark import SolarPark
from gr_comun.src.timeseries.object.simulation import Simulation

class SolarResource:
    """
    This object is a
    """
    def __init__(self,
                 simulation: Simulation = None,
                 solar_park: SolarPark = None):
        self.simulation = simulation
        self.solar_park = solar_park
        self.var = 'ghi'

    def get_solar_cap_factor(self):

        resource = (NREL_RESOURCE(ts_from=self.simulation.ts_from,
                                  ts_to=self.simulation.ts_to,
                                  )
                    .get_resource(var=self.var,
                                  lat=self.simulation.lat,
                                  lon=self.simulation.lon,
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
