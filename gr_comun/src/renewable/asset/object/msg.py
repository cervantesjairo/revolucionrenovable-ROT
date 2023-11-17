from gr_comun.src.messages.base import Message
import pandas as pd


class AssetMSG(Message):
    # WS = 'wind_speed'
    PERIOD = 'time'


    def __init__(self):
        self.df = pd.DataFrame()

