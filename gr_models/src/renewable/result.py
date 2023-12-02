import pandas as pd
from pyomo.environ import *
import plotly.graph_objs as go
import plotly.subplots as sp

from gr_models.src.renewable.solve import ModelSolution
from gr_comun.src.renewable.asset.ren_asset import RenewableAsset
from gr_comun.src.timeseries.ts_rot import TimeSeriesROT


from gr_models.src.renewable.asset.nomenclature.wind import WindNomenclature as Wn
from gr_models.src.renewable.asset.nomenclature.solar import SolarNomenclature as Sn
from gr_models.src.renewable.asset.nomenclature.battery import BatteryNomenclature as Bn
from gr_models.src.renewable.asset.nomenclature.asset import AssetNomenclature as An


class ResultOptimization:



    def __init__(self,
                 instance: ModelSolution,
                 asset: RenewableAsset,
                 timeseries: TimeSeriesROT = None):
        self.instance = instance
        self.asset = asset
        self.timeseries = timeseries
        
    # def get_result_df(self):
        # TODO : need to review teh modes options in the models
        # TODO : need to review the parallel for teh timeseries

    def get_result_df(self):

        MILLION = 1e6

        instance = self.instance
        asset = self.asset.config
        ts = self.timeseries

        cv_wind = pd.DataFrame()
        cv_solar = pd.DataFrame()
        cv_battery = pd.DataFrame()

        if 'wind' in asset:

            cv_wind['Size [kW]'] = [round(value(getattr(instance, Wn.vSize)), 2)]

            cv_wind['Cost Inv [M$]'] = [round(value(getattr(instance, Wn.vCostInvst)) / MILLION, 2)]
            cv_wind['Cost Prod [M$]'] = [round(value(getattr(instance, Wn.vCostProd)) / MILLION, 2)]
            cv_wind['Revenue [M$]'] = [round(value(getattr(instance, Wn.vRevGrid)) / MILLION, 2)]
            cv_wind['Profit [M$]'] = [cv_wind['Revenue [M$]'][0]
                                      - (cv_wind['Cost Inv [M$]'][0] + cv_wind['Cost Prod [M$]'][0])]

            ts[Wn.vWtoA] = [value(getattr(instance, Wn.vWtoA)[j]) for j in getattr(instance, An.PERIOD)]
            ts[Wn.vWLoss] = [value(getattr(instance, Wn.vWLoss)[j]) for j in getattr(instance, An.PERIOD)]
            ts['WbfL'] = ts[Wn.vWtoA] + ts[Wn.vWLoss]

            cv_wind['Energy Delivered [kWh]'] = [round(sum(ts[Wn.vWtoA]), 1)]
            cv_wind['Energy Loss [kWh]'] = [round(sum(ts[Wn.vWLoss]), 1)]
            cv_wind['NCF [p.u.]'] = [round(sum(ts[Wn.vWtoA]) / (len(ts[Wn.vWtoA]) * cv_wind['Size [kW]'][0]), 4)]

            if 'battery' in asset:
                ts[Bn.vWtoB] = [(-1) * value(getattr(instance, Bn.vWtoB)[j]) for j in getattr(instance, An.PERIOD)]
                ts['Resource Wind'] = ts[Wn.vWtoA] - ts[Bn.vWtoB]
                cv_wind['Energy Stored [kWh]'] = [round(sum(ts[Bn.vWtoB]), 1)]
                cv_wind['Resource Wind [kWh]'] = [round(sum(ts['Resource Wind']), 1)]

        if 'solar' in asset:

            cv_solar['Size AC [kW]'] = [round(value(getattr(instance, Sn.vSizeAC)), 2)]
            cv_solar['Size DC [kW]'] = [round(value(getattr(instance, Sn.vSizeDC)), 2)]
            cv_solar['Ratio'] = cv_solar['Size DC [kW]'][0] / cv_solar['Size AC [kW]'][0]
            cv_solar['Size [kW/ratio]'] = '{size_ac}@ {ratio}'.format(size_ac=round(cv_solar['Size AC [kW]'][0]),
                                                                    ratio=round(cv_solar['Ratio'][0], 2))

            cv_solar['Cost Inv [M$]'] = [round(value(getattr(instance, Sn.vCostInvst)) / MILLION, 2)]
            cv_solar['Cost Prod [M$]'] = [round(value(getattr(instance, Sn.vCostProd)) / MILLION, 2)]
            cv_solar['Revenue [M$]'] = [round(value(getattr(instance, Sn.vRevGrid)) / MILLION, 2)]
            cv_solar['Profit [M$]'] = [cv_solar['Revenue [M$]'][0]
                                       - (cv_solar['Cost Inv [M$]'][0] + cv_solar['Cost Prod [M$]'][0])]

            ts[Sn.vStoA] = [value(getattr(instance, Sn.vStoA)[j]) for j in getattr(instance, An.PERIOD)]
            ts[Sn.vProdDC] = [value(getattr(instance, Sn.vProdDC)[j]) for j in getattr(instance, An.PERIOD)]
            ts[Sn.vInvAC] = [value(getattr(instance, Sn.vInvAC)[j]) for j in getattr(instance, An.PERIOD)]
            ts[Sn.vInvDC] = [value(getattr(instance, Sn.vInvDC)[j]) for j in getattr(instance, An.PERIOD)]
            ts[Sn.vLossDC] = [value(getattr(instance, Sn.vLossDC)[j]) for j in getattr(instance, An.PERIOD)]
            ts[Sn.vLossAC] = [value(getattr(instance, Sn.vLossAC)[j]) for j in getattr(instance, An.PERIOD)]
            ts['SbfL'] = ts[Sn.vStoA] + ts[Sn.vLossAC]
            ts['Loss'] = ts[Sn.vLossDC] + ts[Sn.vLossAC]

            cv_solar['Energy Delivered [kWh]'] = [round(sum(ts[Sn.vStoA]), 1)]
            cv_solar['Energy Loss [kWh]'] = [round(sum(ts['Loss']), 1)]
            cv_solar['NCF [p.u.]'] = [round(sum(ts[Sn.vStoA]) / (len(ts[Sn.vStoA]) * cv_solar['Size AC [kW]'][0]), 4)]

            if 'battery' in asset:
                ts[Bn.vStoB] = [(-1) * value(getattr(instance, Bn.vStoB)[j]) for j in getattr(instance, An.PERIOD)]
                ts['Resource Solar'] = ts[Sn.vStoA] - ts[Bn.vStoB]
                cv_solar['Energy Stored [kWh]'] = [round(sum(ts[Bn.vStoB]))]
                cv_solar['Resource Solar [kWh]'] = [round(sum(ts['Resource Solar']))]

        if 'battery' in asset:

            cv_battery['Power Size [kW]'] = [round(value(getattr(instance, Bn.vSizePow)), 2)]
            cv_battery['Cap. Size [kWh]'] = [round(value(getattr(instance, Bn.vSizeCap)), 2)]
            cv_battery['Dur. [hr]'] = [round(cv_battery['Cap. Size [kWh]'][0] / cv_battery['Power Size [kW]'][0], 2)]
            cv_battery['Size [kW/dur]'] = '{size_power}@{dur}hr'.format(size_power=cv_battery['Power Size [kW]'][0],
                                                                    dur=cv_battery['Dur. [hr]'][0])

            cv_battery['Cost Inv [M$]'] = [round(value(getattr(instance, Bn.vCostInvst)) / MILLION, 2)]
            cv_battery['Cost Prod [M$]'] = [round(value(getattr(instance, Bn.vCostProd)) / MILLION, 2)]
            cv_battery['Cost Grid [M$]'] = [round(value(getattr(instance, Bn.vCostGrid)) / MILLION, 2)]
            cv_battery['Revenue [M$]'] = [round(value(getattr(instance, Bn.vRevGrid)) / MILLION, 2)]
            cv_battery['Profit [M$]'] = [(cv_battery['Revenue [M$]'][0] - cv_battery['Cost Grid [M$]'][0])
                                         - (cv_battery['Cost Inv [M$]'][0] + cv_battery['Cost Prod [M$]'][0])]

            ts[Bn.vSOC] = [value(getattr(instance, Bn.vSOC)[j]) for j in getattr(instance, An.PERIOD)]
            ts[Bn.vState] = [value(getattr(instance, Bn.vState)[j]) for j in getattr(instance, An.PERIOD)]
            ts[Bn.vChg] = [value(getattr(instance, Bn.vChg)[j]) for j in getattr(instance, An.PERIOD)]
            ts[Bn.vDch] = [value(getattr(instance, Bn.vDch)[j]) for j in getattr(instance, An.PERIOD)]
            ts[Bn.vGtoB] = [(-1) * value(getattr(instance, Bn.vGtoB)[j]) for j in getattr(instance, An.PERIOD)]
            ts[Bn.vBtoA] = [(-1) * value(getattr(instance, Bn.vBtoA)[j]) for j in getattr(instance, An.PERIOD)]
            ts['Bdispatch'] = ts[Bn.vDch] + ts[Bn.vChg]

            cv_battery['Energy Delivered [kWh]'] = [round(sum(ts[Bn.vDch]), 1)]
            cv_battery['Energy Stored [kWh]'] = [round(sum(ts[Bn.vChg]), 1)]
            cv_battery['Energy Loss [kWh]'] = [100 * round(float((cv_battery['Energy Stored [kWh]'][0]
                                                                  - cv_battery['Energy Delivered [kWh]'][0])
                                                                 / cv_battery['Energy Stored [kWh]'][0]), 4)]
            cv_battery['Cycles'] = [sum(ts[Bn.vDch]) / cv_battery['Cap. Size [kWh]'][0]]

        df_cv = [cv_wind, cv_solar, cv_battery]

        # df_cv = pd.concat([
        #       cv_wind,
        #       cv_solar,
        #       cv_battery], axis=1)

        return df_cv, ts
