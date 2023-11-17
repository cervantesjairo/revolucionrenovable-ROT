from gr_comun.src.messages.base import TimeSeriesMessage as TSm
from gr_comun.src.timeseries.object.simulation import Simulation
from gr_comun.src.timeseries.base import get_timeseries

from gr_comun.src.renewable.wind.windfarm import WindFarm
from gr_comun.src.renewable.solar.solarpark import SolarPark
from gr_comun.src.renewable.storage.battery import BES
from gr_comun.src.load.object.load import Load
from gr_comun.src.price.object.price import Price


from gr_connector.src.nrel.connectors.wind import WindResource
from gr_connector.src.nrel.connectors.solar import SolarResource
from gr_connector.src.caiso.connectors.lmp import LMP
from gr_connector.src.caiso.connectors.load import LOAD

import pandas as pd


class TimeSeriesROT:

    def __init__(self,
                 simulation: Simulation,
                 wind: WindFarm = None,
                 solar: SolarPark = None,
                 storage: BES = None,
                 load: Load = None,
                 price: Price = None,
                 ):
        self.simulation = simulation
        self.wind = wind
        self.solar = solar
        self.storage = storage
        self.load = load
        self.price = price

    def get_timeseries_data(self):

        df_wind = None
        df_solar = None
        df_price = None
        df_load = None

        ts = get_timeseries(ts_from=self.simulation.ts_from,
                            ts_to=self.simulation.ts_to,
                            freq=self.simulation.freq,
                            lat=self.simulation.lat,
                            lon=self.simulation.lon,
                            tz=self.simulation.tz,
                            ).df

        if self.wind:
            df_wind = WindResource(simulation=self.simulation,
                                   wind_farm=self.wind,).get_wind_cap_factor()

        if self.solar:
            df_solar = SolarResource(simulation=self.simulation,
                                     solar_park=self.solar,).get_solar_cap_factor()
        #
        # if self.price:
        #     df_price = (LMP(simulation=self.simulation,)
        #                 .get_lmp_da(node=self.price.price_node_id))

        # if self.load:
        #     df_load = (LOAD(simulation=self.simulation,)
        #                .get_demand_actual(area=self.load.area))

        dataframes = [df_wind, df_solar, df_price, df_load]
        for df in dataframes:
            if df is not None:
                ts = pd.merge(ts, df,
                              how='inner',
                              left_on=[TSm.DT_UTC, TSm.DT_FROM, TSm.DT_TO],
                              right_on=[TSm.DT_UTC, TSm.DT_FROM, TSm.DT_TO])

        return ts
