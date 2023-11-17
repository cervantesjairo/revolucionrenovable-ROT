from pyomo.environ import *

from gr_models.src.renewable.asset.model_structure import Sets, Pars, Vars, Objs, Cons

from gr_models.src.renewable.asset.nomenclature.asset import AssetNomenclature as An
from gr_models.src.renewable.asset.nomenclature.wind import WindNomenclature as Wn
from gr_models.src.renewable.asset.nomenclature.solar import SolarNomenclature as Sn
from gr_models.src.renewable.asset.nomenclature.battery import BatteryNomenclature as Bn
from gr_models.src.renewable.asset.utils import *

class ModelSets(Sets):
    def __init__(self,
                 model=None,
                 asset=None):
        self._PERIOD(model)

    def _PERIOD(self, model):
        set(model, An.PERIOD)

class ModelParams(Pars):
    def __init__(self,
                 model=None,
                 asset=None):
        super().__init__(model, asset)

        self._asset_poi(model)
        self._lmp(model)

    def _asset_poi(self, model):
        par(model, An.pPOI)

    def _lmp(self, model):
        par(model, An.pLMP, An.PERIOD)


class ModelVars(Vars):
    def __init__(self,
                 model=None,
                 asset=None):
        super().__init__(model, asset)


class ModelObjective(Objs):
    def __init__(self,
                 model=None,
                 asset=None):
        super().__init__(model, asset)


class ModelConstraints(Cons):
    def __init__(self,
                 model=None,
                 asset=None):
        super().__init__(model, asset)

        # _asset = asset
        # _asset = config_mode['info_asset_mode'][0]
        if asset.config == 'wind':
            self._wind_asset_poi_limit(model)

        if asset.config == 'solar':
            self._solar_asset_poi_limit(model)

        if asset.config == 'battery':
            self._battery_charge_asset_poi_limit(model)
            self._battery_discharge_asset_poi_limit(model)

        if asset.config == 'wind_solar':
            self._wind_asset_poi_limit(model)
            self._solar_asset_poi_limit(model)
            self._wind_solar_at_poi_limit(model)

        if asset.config == 'wind_battery':
            self._wind_asset_poi_limit(model)
            self._battery_charge_asset_poi_limit(model)
            self._battery_discharge_asset_poi_limit(model)
            self._wind_battery_at_poi_limit(model)

        if asset.config == 'solar_battery':
            self._solar_asset_poi_limit(model)
            self._battery_charge_asset_poi_limit(model)
            self._battery_discharge_asset_poi_limit(model)
            self._solar_battery_at_poi_limit(model)

        if asset.config == 'wind_solar_battery':
            self._wind_asset_poi_limit(model)
            self._solar_asset_poi_limit(model)
            self._battery_charge_asset_poi_limit(model)
            self._battery_discharge_asset_poi_limit(model)
            self._wind_solar_battery_at_poi_limit(model)


    # def _wind_asset_poi_limit(self, model):
    #     def wind_asset_poi_limit_rule(model, t):
    #         return model.WtoA[t] <= model.info_asset_poi
    #     model.wind_at_asset_poi_limit = Constraint(model.PERIOD, rule=wind_asset_poi_limit_rule)

    def _wind_asset_poi_limit(self, model):
        def wind_asset_poi_limit_rule(model, t):
            return v(model, Wn.vWtoA)[t] <= p(model, An.pPOI)

        model.wind_at_asset_poi_limit = Constraint(s(model, An.PERIOD), rule=wind_asset_poi_limit_rule)

    # def _solar_asset_poi_limit(self, model):
    #     def solar_asset_poi_limit_rule(model, t):
    #         return model.StoA[t] <= model.info_asset_poi
    #
    #     model.solar_at_asset_poi_limit = Constraint(model.PERIOD, rule=solar_asset_poi_limit_rule)

    def _solar_asset_poi_limit(self, model):
        def solar_asset_poi_limit_rule(model, t):
            return v(model, Sn.vStoA)[t] <= p(model, An.pPOI)

        model.solar_at_asset_poi_limit = Constraint(s(model, An.PERIOD), rule=solar_asset_poi_limit_rule)

    # def _battery_charge_asset_poi_limit(self, model):
    #     def battery_charge_asset_poi_limit_rule(model, t):
    #         return model.B_CHARGE[t] <= model.info_asset_poi
    #
    #     model.battery_charge_asset_at_poi_limit = Constraint(model.PERIOD, rule=battery_charge_asset_poi_limit_rule)

    def _battery_charge_asset_poi_limit(self, model):
        def battery_charge_asset_poi_limit_rule(model, t):
            return v(model, Bn.vChg)[t] <= p(model, An.pPOI)

        model.battery_charge_asset_at_poi_limit = Constraint(s(model, An.PERIOD), rule=battery_charge_asset_poi_limit_rule)

    # def _battery_discharge_asset_poi_limit(self, model):
    #     def battery_discharge_asset_poi_limit_rule(model, t):
    #         return model.B_DISCHARGE[t] <= model.info_asset_poi
    #
    #     model.battery_discharge_asset_at_poi_limit = Constraint(model.PERIOD, rule=battery_discharge_asset_poi_limit_rule)

    def _battery_discharge_asset_poi_limit(self, model):
        def battery_discharge_asset_poi_limit_rule(model, t):
            return v(model, Bn.vDch)[t] <= p(model, An.pPOI)

        model.battery_discharge_asset_at_poi_limit = Constraint(s(model, An.PERIOD), rule=battery_discharge_asset_poi_limit_rule)


    # def _wind_solar_at_poi_limit(self, model):
    #     def wind_solar_at_poi_limit_rule(model, t):
    #         return model.WtoA[t] + model.StoA[t] <= model.info_asset_poi
    #     model.wind_solar_at_poi_limit = Constraint(model.PERIOD, rule=wind_solar_at_poi_limit_rule)

    def _wind_solar_at_poi_limit(self, model):
        def wind_solar_at_poi_limit_rule(model, t):
            return v(model, Wn.vWtoA)[t] + v(model, Sn.vStoA)[t] <= p(model, An.pPOI)

        model.wind_solar_at_poi_limit = Constraint(s(model, An.PERIOD), rule=wind_solar_at_poi_limit_rule)


    # def _wind_battery_at_poi_limit(self, model):
    #     def wind_battery_at_poi_limit_rule(model, t):
    #         return model.WtoA[t] + model.B_DISCHARGE[t] <= model.info_asset_poi
    #     model.wind_battery_at_poi_limit = Constraint(model.PERIOD, rule=wind_battery_at_poi_limit_rule)

    def _wind_battery_at_poi_limit(self, model):
        def wind_battery_at_poi_limit_rule(model, t):
            return v(model, Wn.vWtoA)[t] + v(model, Bn.vDch)[t] <= p(model, An.pPOI)

        model.wind_battery_at_poi_limit = Constraint(s(model, An.PERIOD), rule=wind_battery_at_poi_limit_rule)


    # def _solar_battery_at_poi_limit(self, model):
    #     def solar_battery_at_poi_limit_rule(model, t):
    #         return model.StoA[t] + model.B_DISCHARGE[t] <= model.info_asset_poi
    #     model.solar_battery_at_poi_limit = Constraint(model.PERIOD, rule=solar_battery_at_poi_limit_rule)

    def _solar_battery_at_poi_limit(self, model):
        def solar_battery_at_poi_limit_rule(model, t):
            return v(model, Sn.vStoA)[t] + v(model, Bn.vDch)[t] <= p(model, An.pPOI)

        model.solar_battery_at_poi_limit = Constraint(s(model, An.PERIOD), rule=solar_battery_at_poi_limit_rule)

    # def _wind_solar_battery_at_poi_limit(self, model):
    #     def wind_solar_battery_at_poi_limit_rule(model, t):
    #         return model.WtoA[t] + model.StoA[t] + model.B_DISCHARGE[t] <= model.info_asset_poi
    #     model.wind_solar_battery_at_poi_limit = Constraint(model.PERIOD, rule=wind_solar_battery_at_poi_limit_rule)

    def _wind_solar_battery_at_poi_limit(self, model):
        def wind_solar_battery_at_poi_limit_rule(model, t):
            return v(model, Wn.vWtoA)[t] + v(model, Sn.vStoA)[t] + v(model, Bn.vDch)[t] <= p(model, An.pPOI)

        model.wind_solar_battery_at_poi_limit = Constraint(s(model, An.PERIOD), rule=wind_solar_battery_at_poi_limit_rule)