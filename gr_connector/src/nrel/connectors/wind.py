from gr_connector.src.nrel.database.resource.query import NREL_RESOURCE
from gr_comun.src.renewable.wind.object.msg import WindMSG as Wmsg
from gr_comun.src.renewable.wind.windfarm import WindFarm
from gr_comun.src.timeseries.object.simulation import Simulation


class WindResource:
    """
    write doc of this class and its methods
    """
    def __init__(self,
                 simulation: Simulation = None,
                 wind_farm: WindFarm = None,
                 ):
        self.simulation = simulation
        self.wind_farm = wind_farm
        self.var = 'wind_speed'

    def get_wind_cap_factor(self):

        resource = (NREL_RESOURCE(ts_from=self.simulation.ts_from,
                                  ts_to=self.simulation.ts_to,
                                  ).get_resource(var=self.var,
                                                 lat=self.simulation.lat,
                                                 lon=self.simulation.lon,
                                                 )
                    )

        wind_hh = self.nrel_10m_to_hh(resource=resource)

        wf = self.wind_farm
        wcf = wf.cap_factor(ts_wind=wind_hh)

        df_wcf = self.wind_msg(df=wcf)

        return df_wcf

    def wind_msg(self, df=None):
        col_msg = [Wmsg.DT_UTC, Wmsg.DT_FROM, Wmsg.DT_TO, Wmsg.WCF] ## TODO: conector need tobe in function of the Nomemcletaure
        df = df[col_msg]

        return df

    def nrel_10m_to_hh(self, resource=None):
        df_wind_speed = resource
        turbine = self.wind_farm.turbine

        nrel_height = 10
        power_law_exponent = 0.4
        factor = (turbine.hub_height / nrel_height) ** power_law_exponent

        df_wind_speed[Wmsg.WS] = factor * df_wind_speed[Wmsg.WS]

        return df_wind_speed
