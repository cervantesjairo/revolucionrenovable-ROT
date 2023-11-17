from gr_comun.src.messages.base import Message
import pandas as pd


class AssetNomenclature(Message):

    # Sets
    PERIOD = 'PERIOD'

    # Parameters
    pPOI = 'asset_poi'
    pLMP = 'lmp'    # todo change to wind/solar/battery lmp

    def __init__(self):
        self.df = pd.DataFrame()
