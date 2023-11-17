from gr_comun.src.messages.base import Message
import pandas as pd


class BatteryMSG(Message):
    # WS = 'wind_speed'
    GHI = 'ghi'
    DHI = 'dhi'
    DNI = 'dni'
    TEMP = 'solar_temp'

    SP = 'solar_power'
    SCF = 'solar_capacity_factor'

    P_AREA = 'solar_panel_area'
    P_EFF = 'solar_panel_eff'
    P_DEG = 'solar_panel_degradation'
    I_EFF = 'solar_inv_eff'
    I_DC_LOSS = 'solar_inv_pre_loss'
    I_AC_LOSS = 'solar_inv_post_loss'

    def __init__(self):
        self.df = pd.DataFrame()

    def append_wind_speed(self, value):
        self.df[BatteryMSG.SP] = value
        return self

