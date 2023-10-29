from gr_comun.src.messages.base import Message
import pandas as pd


class WindMSG(Message):
    # NO_VA_AQUI = 'wind_speed'   # TODO: remove this line
    # S_HH = 'wind_speed_hub_height '# TODO: remove this line
    WS = 'wind_speed'
    WP = 'wind_power'
    WCF = 'wind_capacity_factor'

    WT_HH = 'turbine_hub_height'
    WT_RP = 'turbine_rated_power'
    WT_VR = 'turbine_vrated'
    WT_VI = 'turbine_vin'
    WT_VO = 'turbine_vout'
    WT_RD = 'turbine_rotor_diameter'

    def __init__(self):
        super().__init__()
        self.df = pd.DataFrame()

    def append_wind_speed(self, value):
        self.df[WindMSG.WS] = value
        return self

    def append_wind_turbine(self, value):
        self.df[WindMSG.WT_HH] = value.wt_hh
        self.df[WindMSG.WT_RP] = value.wt_rp
        self.df[WindMSG.WT_VR] = value.wt_vr
        self.df[WindMSG.WT_VI] = value.wt_vi
        self.df[WindMSG.WT_VO] = value.wt_vo
        self.df[WindMSG.WT_RD] = value.wt_rd

        return self

