from gr_comun.src.renewable.asset.ren_asset import RenewableAsset
from gr_comun.src.renewable.storage.battery import BES
from gr_comun.src.renewable.solar.solarpark import SolarPark
from gr_comun.src.renewable.wind.windfarm import WindFarm
from gr_models.src.renewable.asset.nomenclature.asset import AssetNomenclature as An
from gr_models.src.renewable.asset.nomenclature.wind import WindNomenclature as Wn
from gr_models.src.renewable.asset.nomenclature.solar import SolarNomenclature as Sn
from gr_models.src.renewable.asset.nomenclature.battery import BatteryNomenclature as Bn

from gr_comun.src.eng_economy.cashflow import CashFlowMeasures

import pandas as pd


class InvariantSeries:

    def __init__(self,
                 asset: RenewableAsset = None,
                 financial: CashFlowMeasures = None,
                 ):
        self.asset = asset
        self.financial = financial

    def get_invariant_series(self):
        wind = self.asset.wind
        solar = self.asset.solar
        storage = self.asset.storage

        df_asset = pd.DataFrame()
        df_asset[An.pPOI] = [self.asset.poi]

        df_wind = pd.DataFrame()
        if wind:
            df_wind = self.get_wind_invariant_series(wind=wind)

        df_solar = pd.DataFrame()
        if solar:
            df_solar = self.get_solar_invariant_series(solar=solar)

        df_storage = pd.DataFrame()
        if storage:
            df_storage = self.get_storage_invariant_series(storage=storage)

        df = pd.concat([
            df_asset,
            df_wind,
            df_solar,
            df_storage], axis=1)

        return df

    def get_wind_invariant_series(self, wind: WindFarm = None):

        df_wind = pd.DataFrame()

        df_wind[Wn.pPOI] = [wind.poi] if wind.poi else [None]

        crf = self.financial.get_capital_recovery_factor()
        df_wind[Wn.pCost] = [wind.cost.capex_wind * crf] if wind.cost.capex_wind else [None]
        df_wind[Wn.pCostInter] = [wind.cost.capex_inter * crf] if wind.cost.capex_inter else [None]

        df_wind[Wn.pCostFix] = [wind.cost.opex_fix] if wind.cost.opex_fix else [None]
        df_wind[Wn.pCostVar] = [wind.cost.opex_variable] if wind.cost.opex_variable else [None]

        df_wind[Wn.pACLoss] = [wind.loss / 100] if wind.loss else [None]

        if wind.mode.size_conf == 'fix':
            df_wind[Wn.pSizeFix] = [wind.mode.size_fix]
        if wind.mode.size_conf == 'range':
            df_wind[Wn.pSizeLB] = [wind.mode.size_lb_min]
            df_wind[Wn.pSizeUB] = [wind.mode.size_ub_max]

        df_wind = df_wind.dropna(axis=1, how='any')

        return df_wind

    def get_solar_invariant_series(self, solar: SolarPark = None):

        df_solar = pd.DataFrame()

        df_solar[Sn.pPOI] = [solar.poi] if solar.poi else [None]

        crf = self.financial.get_capital_recovery_factor()
        df_solar[Sn.pCostPnl] = [solar.cost.capex_panel * crf] if solar.cost.capex_panel else [None]
        df_solar[Sn.pCostInv] = [solar.cost.capex_inv * crf] if solar.cost.capex_inv else [None]
        df_solar[Sn.pCostBos] = [solar.cost.capex_bos * crf] if solar.cost.capex_bos else [None]

        df_solar[Sn.pCostFix] = [solar.cost.opex_fix] if solar.cost.opex_fix else [None]
        df_solar[Sn.pCostVar] = [solar.cost.opex_var] if solar.cost.opex_var else [None]

        df_solar[Sn.pPnlDeg] = [solar.panel_inv.panel_deg / 100] if solar.panel_inv.panel_deg else [None]
        df_solar[Sn.pInvEff] = [solar.panel_inv.inv_eff / 100] if solar.panel_inv.inv_eff else [None]
        df_solar[Sn.pInvDCLoss] = [solar.panel_inv.inv_dc_loss / 100] if solar.panel_inv.inv_dc_loss else [None]
        df_solar[Sn.pInvACLoss] = [solar.panel_inv.inv_ac_loss / 100] if solar.panel_inv.inv_ac_loss else [None]

        if solar.mode.inv_conf == 'fix':
            df_solar[Sn.pSizeFix] = [solar.mode.inv_fix]
        if solar.mode.inv_conf == 'range':
            df_solar[Sn.pSizeLB] = [solar.mode.inv_lb_min]
            df_solar[Sn.pSizeUB] = [solar.mode.inv_ub_max]

        if solar.mode.ratio_conf == 'fix':
            df_solar[Sn.pRatFix] = [solar.mode.ratio_fix]
        if solar.mode.ratio_conf == 'range':
            df_solar[Sn.pRatLB] = [solar.mode.ratio_lb_min]
            df_solar[Sn.pRatUB] = [solar.mode.ratio_ub_max]

        df_solar = df_solar.dropna(axis=1, how='any')

        return df_solar

        # df = pd.concat([
        #     df_wind_poi,
        #     df_wind_capex,
        #     df_wind_opex,
        #     df_loss_percentage,
        #     df_wind_size_mode_value
        # ], axis=1)

    def get_storage_invariant_series(self, storage: BES = None):

        df_storage = pd.DataFrame()

        df_storage[Bn.pPOI] = [storage.poi] if storage.poi else [None]

        crf = self.financial.get_capital_recovery_factor()
        df_storage[Bn.pCostPow] = [storage.cost.capex_power * crf] if storage.cost.capex_power else [None]
        df_storage[Bn.pCostCap] = [storage.cost.capex_capacity * crf] if storage.cost.capex_capacity else [None]

        df_storage[Bn.pCostFix] = [storage.cost.opex_fix] if storage.cost.opex_fix else [None]
        df_storage[Bn.pCostVar] = [storage.cost.opex_var] if storage.cost.opex_var else [None]

        df_storage[Bn.pRTE] = [storage.battery.rte / 100] if storage.battery.rte else [None]

        if storage.mode.power_conf == 'fix':
            df_storage[Bn.pPowFix] = [storage.mode.power_fix]
        if storage.mode.power_conf == 'range':
            df_storage[Bn.pPowLB] = [storage.mode.power_lb_min]
            df_storage[Bn.pPowUB] = [storage.mode.power_ub_max]

        if storage.mode.dur_conf == 'fix':
            df_storage[Bn.pDurFix] = [storage.mode.dur_fix]
        if storage.mode.dur_conf == 'range':
            df_storage[Bn.pDurLB] = [storage.mode.dur_lb_min]
            df_storage[Bn.pDurUB] = [storage.mode.dur_ub_max]

        if storage.mode.dod_conf == 'unrestricted':
            None
        if storage.mode.dod_conf == 'range':
            df_storage[Bn.pDODLB] = [storage.mode.dod_lb_min]
            df_storage[Bn.pDODUB] = [storage.mode.dod_ub_max]

        if storage.mode.cycle_conf == 'unrestricted':
            None
        if storage.mode.cycle_conf == 'range':
            df_storage[Bn.pCycLB] = [storage.mode.cycle_lb_min]
            df_storage[Bn.pCycUB] = [storage.mode.cycle_ub_max]

        df_storage = df_storage.dropna(axis=1, how='any')

        return df_storage
