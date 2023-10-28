from gr_comun.src.renewable.wind.msg import WindMSG as Wmsg
import pandas as pd
import numpy as np


class SolarCF:
    """
    two inputs ts_windspeed and wind_turbine

    """

    def __init__(self, ts_windspeed=None, wind_turbine=None):
        self.ts_ws = ts_windspeed
        self.wt = wind_turbine

    def get_power_curve_wt1(self):
        # https: // www.thewindpower.net / turbine_en_296_clipper_liberty - c96.php
        power_curve = ((np.where(self.ts_ws[Wmsg.WS] < self.wt.vin, 0,
                                 np.where(self.ts_ws[Wmsg.WS] > self.wt.vout, 0,
                                          np.where(self.ts_ws[Wmsg.WS] >= self.wt.vrated,
                                                   self.wt.ratedpower,
                                                   self.wt.ratedpower * (
                                                           8E-05 * (self.ts_ws[Wmsg.WS] ** 5)
                                                           - 0.0037 * (self.ts_ws[Wmsg.WS] ** 4)
                                                           + 0.0621 * (self.ts_ws[Wmsg.WS] ** 3)
                                                           - 0.4672 * (self.ts_ws[Wmsg.WS] ** 2)
                                                           + 1.6559 * (self.ts_ws[Wmsg.WS] ** 1)
                                                           - 2.2083)))))
                       / self.wt.ratedpower)

        return power_curve
