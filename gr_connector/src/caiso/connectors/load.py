from gr_connector.src.caiso.database.demand.query import CAISO_DEMAND


class LOAD:
    """
    This object is a
    """
    def __init__(self,
                 ts_from=None,
                 ts_to=None
                 ):
        self.start = ts_from
        self.end = ts_to

    def get_demand_actual(self,  area: str = None,):

        quantity = CAISO_DEMAND(ts_from=self.start,
                                ts_to=self.end
                                ).get_demand(market='ACTUAL',
                                             area=area)

        return quantity


