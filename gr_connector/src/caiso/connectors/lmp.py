from gr_connector.src.caiso.database.price.query import CAISO_PRICE
from gr_comun.src.timeseries.object.simulation import Simulation


class LMP:
    """
    This object is a
    """
    def __init__(self,
                 simulation: Simulation = None,
                 ):
        self.simulation = simulation

    def get_lmp_da(self, node):
        quantity = CAISO_PRICE(ts_from=self.simulation.ts_from,
                               ts_to=self.simulation.ts_to
                               ).get_lmp(market='DAM',
                                         node=node)
        return quantity

    def get_lmp_rtpd(self, node=None):
        quantity = CAISO_PRICE(ts_from=self.simulation.ts_from,
                            ts_to=self.simulation.ts_to
                            ).get_lmp(market='RTPD',
                                        node=node)
        return quantity

    def get_lmp_rtm(self, node=None):
        quantity = CAISO_PRICE(ts_from=self.simulation.ts_from,
                               ts_to=self.simulation.ts_to
                               ).get_lmp(market='RTM',
                                         node=node)
        return quantity


    #
    # def get_lmp_da(self, node=None):
    #
    #     quantity = CAISO_PRICE(ts_from=self.start,
    #                            ts_to=self.end
    #                            ).get_lmp(market='DAM',
    #                                      node=node)
    #
    #     return quantity
    #
    # def get_lmp_rtpd(self, node=None):
    #
    #     quantity = CAISO_PRICE(ts_from=self.start,
    #                         ts_to=self.end
    #                         ).get_lmp(market='RTPD',
    #                                     node=node)
    #
    #     return quantity
    #
    # def get_lmp_rtm(self, node=None):
    #
    #     quantity = CAISO_PRICE(ts_from=self.start,
    #                            ts_to=self.end
    #                            ).get_lmp(market='RTM',
    #                                      node=node)
    #
    #     return quantity
