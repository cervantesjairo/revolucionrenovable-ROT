import pandas as pd
import numpy as np


class PanelInv:
    """
    two inputs ts_windspeed and wind_turbine
class SolarMSG(Message):
    # WS = 'wind_speed'
    P_AREA = 'solar_panel_area'
    P_EFF = 'solar_panel_eff'
    P_DEG = 'solar_panel_degradation'
    I_EFF = 'solar_inv_eff'
    I_DC_LOSS = 'solar_inv_pre_loss'
    I_AC_LOSS = 'solar_inv_post_loss'
    """
    def __init__(self,
                 panel_pmax: int,
                 panel_area=None,
                 panel_eff=None,
                 panel_deg=None,
                 inv_eff=None,
                 inv_dc_loss=None,
                 inv_ac_loss=None):
        self.panel_pmax = panel_pmax
        self.panel_area = panel_area
        self.panel_eff = panel_eff
        self.panel_deg = panel_deg
        self.inv_eff = inv_eff
        self.inv_dc_loss = inv_dc_loss
        self.inv_ac_loss = inv_ac_loss
