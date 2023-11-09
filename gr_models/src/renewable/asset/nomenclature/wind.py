from gr_comun.src.messages.base import Message
import pandas as pd


class WindNomenclature(Message):

    # Sets
    PERIOD = 'PERIOD'

    # Parameters
    pPOI = 'wind_poi'
    pCost = 'wind_cost'
    pCostInter = 'wind_cost_inter'
    pCostFix = 'wind_cost_fix'
    pCostVar = 'wind_cost_variable'
    pSizeFix = 'wind_size_fix'
    pSizeLB = 'wind_size_lb_min'
    pSizeUB = 'wind_size_ub_max'
    pWIND = 'wind' # todo change to scf
    pLMP = 'lmp' # todo change to wind lmp

    # Variables
    vCostInvst = 'WIND_INV_COST'
    vCostProd = 'WIND_PROD_COST'
    vRevGrid = 'WIND_GRID_REVENUE'
    vSize = 'WIND_SIZE'
    vWtoA = 'WtoA'
    vWLoss = 'WLoss'

    def __init__(self):
        self.df = pd.DataFrame()

    # def append_wind_speed(self, value):
    #     self.df[SolarMSG.SP] = value
    #     return self
