from gr_connector.src.caiso.database.price.query import CAISO_PRICE
import numpy as np


class LMP:
    """
    This object is a
    """
    def __init__(self,
                 ts_from=None,
                 ts_to=None
                 ):
        self.start = ts_from
        self.end = ts_to

    def get_lmp_da(self, node=None):

        quantity = CAISO_PRICE(ts_from=self.start,
                               ts_to=self.end
                               ).get_lmp(market='DAM',
                                         node=node)

        return quantity

    def get_lmp_rtpd(self, node=None):

        quantity = CAISO_PRICE(ts_from=self.start,
                            ts_to=self.end
                            ).get_lmp(market='RTPD',
                                        node=node)

        return quantity

    def get_lmp_rtm(self, node=None):

        quantity = CAISO_PRICE(ts_from=self.start,
                               ts_to=self.end
                               ).get_lmp(market='RTM',
                                         node=node)

        return quantity
