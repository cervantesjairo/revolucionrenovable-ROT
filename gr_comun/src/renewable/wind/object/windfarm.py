from gr_comun.src.renewable.wind.object.turbine import WindTurbine
from gr_comun.src.renewable.wind.msg import WindMSG as Wmsg
import pandas as pd
import numpy as np


class WindFarm(WindTurbine):
    """

    """

    def __init__(self, wind_poi=None,
                 wind_size_mode=None,
                 wind_cost=None,
                 wind_cost_inter=None,
                 wind_cost_fix=None,
                 wind_cost_variable=None,
                 wind_size_fix=None,
                 wind_size_lb_min=None,
                 wind_size_ub_max=None,
                 turbine: WindTurbine() = None,
                 ):
        # super().__init__()
        self.wind_poi = wind_poi
        self.wind_size_mode = wind_size_mode
        self.wind_cost = wind_cost
        self.wind_cost_inter = wind_cost_inter
        self.wind_cost_fix = wind_cost_fix
        self.wind_cost_variable = wind_cost_variable
        self.wind_size_fix = wind_size_fix
        self.wind_size_lb_min = wind_size_lb_min
        self.wind_size_ub_max = wind_size_ub_max
        self.turbine = turbine

    def cap_factor(self, ts_windspeed=None):

        ts_wp = self.power_curve(rated_power=self.turbine.rated_power,
                                 v_rated=self.turbine.v_rated,
                                 v_cut_in=self.turbine.v_cut_in,
                                 v_cut_out=self.turbine.v_cut_out,
                                 ts_ws=ts_windspeed)

        ts_windspeed[Wmsg.WCF] = ts_wp[Wmsg.WP] / self.turbine.rated_power

        return ts_windspeed

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
