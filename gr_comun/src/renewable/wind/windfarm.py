from gr_comun.src.renewable.wind.object.elements import WindTurbine, WindCost, WindMode
from gr_comun.src.renewable.wind.object.msg import WindMSG as Wmsg
import numpy as np


class WindFarm:
    """

    """

    def __init__(self,
                 poi=None,
                 mode: WindMode = None,
                 cost: WindCost = None,
                 turbine: WindTurbine = None,
                 loss=None
                 ):
        self.poi = poi
        self.mode = mode
        self.cost = cost
        self.turbine = turbine
        self.loss = loss

    def cap_factor(self, ts_wind=None):

        ts_wp = self.power_curve(rated_power=self.turbine.rated_power,
                                 v_rated=self.turbine.v_rated,
                                 v_cut_in=self.turbine.v_cut_in,
                                 v_cut_out=self.turbine.v_cut_out,
                                 ts_ws=ts_wind)

        ts_wind[Wmsg.WCF] = ts_wp[Wmsg.WP] / self.turbine.rated_power

        return ts_wind

    def power_curve(self, ts_ws=None, rated_power=None, v_rated=None, v_cut_in=None, v_cut_out=None):
        turbine = self.turbine
        # https://www.thewindpower.net/turbine_en_296_clipper_liberty-c96.php
        power_curve = np.where(ts_ws[Wmsg.WS] < turbine.v_cut_in,
                               0,
                               np.where(ts_ws[Wmsg.WS] > turbine.v_cut_out,
                                        0,
                                        np.where(ts_ws[Wmsg.WS] >= turbine.v_rated,
                                                 turbine.rated_power,
                                                 turbine.rated_power * (
                                                         8E-05 * (ts_ws[Wmsg.WS] ** 5)
                                                         - 0.0037 * (ts_ws[Wmsg.WS] ** 4)
                                                         + 0.0621 * (ts_ws[Wmsg.WS] ** 3)
                                                         - 0.4672 * (ts_ws[Wmsg.WS] ** 2)
                                                         + 1.6559 * (ts_ws[Wmsg.WS] ** 1)
                                                         - 2.2083)
                                                 )
                                        )
                               )

        ts_ws[Wmsg.WP] = power_curve

        return ts_ws
