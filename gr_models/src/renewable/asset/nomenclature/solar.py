from gr_comun.src.messages.base import Message
import pandas as pd


class SolarNomenclature(Message):

    # Sets
    PERIOD = 'PERIOD'

    # Parameters
    pPOI = 'solar_poi'
    pCostInv = 'solar_cost_inverter'
    pCostBos = 'solar_cost_bos'
    pCostPnl = 'solar_cost_panel'
    pCostFix = 'solar_cost_fix'
    pCostVar = 'solar_cost_variable'
    pPnlDeg = 'solar_panel_degradation'
    pInvEff = 'solar_inv_eff'
    pInvDCLoss = 'solar_inv_pre_loss'
    pInvACLoss = 'solar_inv_post_loss'
    pRatFix = 'solar_ratio_fix'
    pRatLB = 'solar_ratio_lb_min'
    pRatUB = 'solar_ratio_ub_max'
    pSizeFix = 'solar_size_fix'
    pSizeLB = 'solar_size_lb_min'
    pSizeUB = 'solar_size_ub_max'
    pSOLAR = 'solar'  # todo change to scf
    pLMP = 'lmp'  # todo change to solar lmp

    # Variables
    vCostInvst = 'SOLAR_INV_COST'
    vCostProd = 'SOLAR_PROD_COST'
    vRevGrid = 'SOLAR_GRID_REVENUE'
    vSizeAC = 'SOLAR_AC_SIZE'
    vSizeDC = 'SOLAR_DC_SIZE'
    vProdDC = 'SOLAR_DC_PROD'
    vStoA = 'StoA'
    vLossDC = 'SLoss_DC'
    vLossAC = 'SLoss_AC'
    vInvDC = 'SOLAR_DC_INV'
    vInvAC = 'SOLAR_AC_INV'

    def __init__(self):
        self.df = pd.DataFrame()

    # def append_wind_speed(self, value):
    #     self.df[SolarMSG.SP] = value
    #     return self
