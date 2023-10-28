from gr_comun.src.renewable.wind.object.turbine import WindTurbine
from gr_comun.src.renewable.wind.msg import WindMSG as Wmsg
from gr_comun.src.renewable.solar.object.panel import PanelInv
from gr_comun.src.renewable.solar.msg import SolarMSG as Smsg
import pandas as pd
import numpy as np

class SolarPark:

    def __init__(self,
                 solar_poi=None,

                 solar_inverter_mode=None,
                 solar_ratio_mode=None,

                 solar_cost_panel=None,
                 solar_cost_bos=None,
                 solar_cost_inverter=None,

                 solar_cost_variable=None,
                 solar_cost_fix=None,

                 solar_size_fix=None,
                 solar_size_lb_min=None,
                 solar_size_ub_max=None,

                 solar_ratio_fix=None,
                 solar_ratio_lb_min=None,
                 solar_ratio_ub_max=None,
                 panel_inv: PanelInv = None,
                 ):

        self.solar_poi = solar_poi
        self.solar_inverter_mode = solar_inverter_mode
        self.solar_ratio_mode = solar_ratio_mode
        self.solar_cost_panel = solar_cost_panel
        self.solar_cost_bos = solar_cost_bos
        self.solar_cost_inverter = solar_cost_inverter
        self.solar_cost_variable = solar_cost_variable
        self.solar_cost_fix = solar_cost_fix
        self.solar_size_fix = solar_size_fix
        self.solar_size_lb_min = solar_size_lb_min
        self.solar_size_ub_max = solar_size_ub_max
        self.solar_ratio_fix = solar_ratio_fix
        self.solar_ratio_lb_min = solar_ratio_lb_min
        self.solar_ratio_ub_max = solar_ratio_ub_max

        self.panel_inv = panel_inv

    def cap_factor(self, ts_solar=None):

        ts_sp = self.panel_power_curve(ts_solar=ts_solar)
        ts_sp = ts_sp / self.panel_inv.panel_pmax

        # ts_sp = np.where(ts_sp >= 1,
        #                  1,
        #                  ts_sp)
        ts_solar[Smsg.SCF] = ts_sp

        return ts_solar

    def panel_power_curve(self, ts_solar=None):
        panel = self.panel_inv

        panel_eff_area = panel.panel_area * panel.panel_eff / 100
        # panel_power_curve = ts_solar[Smsg.GHI] * panel_eff_area
        panel_power_curve = ts_solar[Smsg.GHI] * panel_eff_area * ((100 - panel.panel_deg) / 100)

        return panel_power_curve

    def panels_per_kw(self):
        num_panel = 1e3 / self.panel_inv.panel_pmax
        return num_panel

    def panels_per_mw(self):
        num_panel = 1e6 / self.panel_inv.panel_pmax
        return num_panel
