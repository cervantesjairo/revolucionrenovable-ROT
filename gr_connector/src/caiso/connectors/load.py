from gr_connector.src.caiso.database.demand.query import CAISO_DEMAND
from gr_comun.src.timeseries.object.simulation import Simulation

class LOAD:
    """
    This object is a
    """
    def __init__(self,
                 simulation: Simulation = None,
                 ):
        self.simulation = simulation

    def get_demand_actual(self,  area: str = None,):

        quantity = CAISO_DEMAND(ts_from=self.simulation.ts_from,
                                ts_to=self.simulation.ts_to
                                ).get_demand(market='ACTUAL',
                                             area=area)

        return quantity


