from pyomo.environ import *

from muiscaenergy_models.src.asset.model_structure import Sets, Pars, Vars, Objs, Cons


class AssetModel:
    def __init__(self, config_mode):
        self.model = AbstractModel()
        self.model.dual = Suffix(direction=Suffix.IMPORT_EXPORT)

        self._asset = config_mode['info_asset_mode'][0]

        MySets(self.model, config_mode)
        MyParams(self.model, config_mode)
        MyVars(self.model, config_mode)
        MyObjective(self.model, config_mode)
        MyConstraints(self.model, config_mode)


class MySets(Sets):
    def __init__(self, model, config_mode):
        self._PERIOD(model)

    def _PERIOD(self, model):
        model.PERIOD = Set()


class MyParams(Pars):
    def __init__(self, model, config_mode):
        super().__init__(model, config_mode)

        self._asset_poi(model)
        self._lmp(model)

    def _asset_poi(self, model):
        model.info_asset_poi = Param()

    def _lmp(self, model):
        model.lmp = Param(model.PERIOD)


class MyVars(Vars):
    def __init__(self, model, config_mode):
        super().__init__(model, config_mode)


class MyObjective(Objs):
    def __init__(self, model, config_mode):
        super().__init__(model, config_mode)


class MyConstraints(Cons):
    def __init__(self, model, config_mode):
        super().__init__(model, config_mode)

        _asset = config_mode['info_asset_mode'][0]
        if _asset == 'wind':
            self._wind_asset_poi_limit(model)

        if _asset == 'solar':
            self._solar_asset_poi_limit(model)

        if _asset == 'battery':
            self._battery_charge_asset_poi_limit(model)
            self._battery_discharge_asset_poi_limit(model)

        if _asset == 'wind_and_solar':
            self._wind_asset_poi_limit(model)
            self._solar_asset_poi_limit(model)
            self._wind_solar_at_poi_limit(model)

        if _asset == 'wind_and_battery':
            self._wind_asset_poi_limit(model)
            self._battery_charge_asset_poi_limit(model)
            self._battery_discharge_asset_poi_limit(model)
            self._wind_battery_at_poi_limit(model)

        if _asset == 'solar_and_battery':
            self._solar_asset_poi_limit(model)
            self._battery_charge_asset_poi_limit(model)
            self._battery_discharge_asset_poi_limit(model)
            self._solar_battery_at_poi_limit(model)

        if _asset == 'wind_and_solar_and_battery':
            self._wind_asset_poi_limit(model)
            self._solar_asset_poi_limit(model)
            self._battery_charge_asset_poi_limit(model)
            self._battery_discharge_asset_poi_limit(model)
            self._wind_solar_battery_at_poi_limit(model)


    def _wind_asset_poi_limit(self, model):
        def wind_asset_poi_limit_rule(model, t):
            return model.WtoA[t] <= model.info_asset_poi
        model.wind_at_asset_poi_limit = Constraint(model.PERIOD, rule=wind_asset_poi_limit_rule)

    def _solar_asset_poi_limit(self, model):
        def solar_asset_poi_limit_rule(model, t):
            return model.StoA[t] <= model.info_asset_poi

        model.solar_at_asset_poi_limit = Constraint(model.PERIOD, rule=solar_asset_poi_limit_rule)

    def _battery_charge_asset_poi_limit(self, model):
        def battery_charge_asset_poi_limit_rule(model, t):
            return model.B_CHARGE[t] <= model.info_asset_poi

        model.battery_charge_asset_at_poi_limit = Constraint(model.PERIOD, rule=battery_charge_asset_poi_limit_rule)

    def _battery_discharge_asset_poi_limit(self, model):
        def battery_discharge_asset_poi_limit_rule(model, t):
            return model.B_DISCHARGE[t] <= model.info_asset_poi

        model.battery_discharge_asset_at_poi_limit = Constraint(model.PERIOD, rule=battery_discharge_asset_poi_limit_rule)

    def _wind_solar_at_poi_limit(self, model):
        def wind_solar_at_poi_limit_rule(model, t):
            return model.WtoA[t] + model.StoA[t] <= model.info_asset_poi
        model.wind_solar_at_poi_limit = Constraint(model.PERIOD, rule=wind_solar_at_poi_limit_rule)

    def _wind_battery_at_poi_limit(self, model):
        def wind_battery_at_poi_limit_rule(model, t):
            return model.WtoA[t] + model.B_DISCHARGE[t] <= model.info_asset_poi
        model.wind_battery_at_poi_limit = Constraint(model.PERIOD, rule=wind_battery_at_poi_limit_rule)

    def _solar_battery_at_poi_limit(self, model):
        def solar_battery_at_poi_limit_rule(model, t):
            return model.StoA[t] + model.B_DISCHARGE[t] <= model.info_asset_poi
        model.solar_battery_at_poi_limit = Constraint(model.PERIOD, rule=solar_battery_at_poi_limit_rule)

    def _wind_solar_battery_at_poi_limit(self, model):
        def wind_solar_battery_at_poi_limit_rule(model, t):
            return model.WtoA[t] + model.StoA[t] + model.B_DISCHARGE[t] <= model.info_asset_poi
        model.wind_solar_battery_at_poi_limit = Constraint(model.PERIOD, rule=wind_solar_battery_at_poi_limit_rule)