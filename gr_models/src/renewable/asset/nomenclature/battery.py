from gr_comun.src.messages.base import Message
import pandas as pd


class BatteryNomenclature(Message):

    # Sets
    PERIOD = 'PERIOD'

    # Parameters
    pPOI = 'battery_poi'
    pCostPow = 'battery_cost_power'
    pCostCap = 'battery_cost_capacity'
    pCostFix = 'battery_cost_fix'
    pCostVar = 'battery_cost_variable'
    pRTE = 'battery_rte'
    pRTEChg = 'battery_rte_charge'
    pRTEDch = 'battery_rte_discharge'
    pDODLB = 'battery_dod_lb_min'
    pDODUB = 'battery_dod_ub_max'
    pCycLB = 'battery_cycle_lb_min'
    pCycUB = 'battery_cycle_ub_max'
    pPowFix = 'battery_power_fix'
    pPowLB = 'battery_power_lb_min'
    pPowUB = 'battery_power_ub_max'
    pDurFix = 'battery_duration_fix'
    pDurLB = 'battery_duration_lb_min'
    pDurUB = 'battery_duration_ub_max'
    pLMP = 'lmp' # todo change to battery lmp


    # Variables
    vCostInvst = 'BATTERY_INV_COST'
    vCostProd = 'BATTERY_PROD_COST'
    vCostGrid = 'BATTERY_GRID_COST'
    vRevGrid = 'BATTERY_GRID_REVENUE'
    vSizePow = 'BATTERY_SIZE_POWER'
    vSizeCap = 'BATTERY_SIZE_CAPACITY'
    vSOC = 'B_SOC'
    vState = 'B_STATE'
    vChg = 'B_CHARGE'
    vDch = 'B_DISCHARGE'
    vGtoB = 'GtoB'
    vBtoA = 'BtoA'
    vWtoB = 'WtoB'
    vStoB = 'StoB'
    vDisp = 'B_DISPATCH'
