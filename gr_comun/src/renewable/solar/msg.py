from gr_comun.src.messages.base import Message
import pandas as pd


class SolarMSG(Message):
    # WS = 'wind_speed'
    P_AREA = 'solar_panel_area'
    P_EFF = 'solar_panel_eff'
    P_DEG = 'solar_panel_degradation'
    I_EFF = 'solar_inv_eff'
    I_DC_LOSS = 'solar_inv_pre_loss'
    I_AC_LOSS = 'solar_inv_post_loss'

    def __init__(self):
        self.df = pd.DataFrame()

    def append_wind_speed(self, value):
        self.df[SolarMSG.WS] = value
        return self

