from pyomo.environ import *

from gr_models.src.asset.parent.wind import WObj, WSet, WVar, WPar, WCon
from gr_models.src.asset.parent.solar import SObj, SSet, SVar, SPar, SCon
from gr_models.src.asset.parent.battery import BObj, BSet, BVar, BPar, BCon


class WSBset(WSet, SSet, BSet):
    def __init__(self, model, config_mode):
        pass


class WSBpar(WPar, SPar, BPar):
    def __init__(self, model, config_mode):
        self._wind_solar_battery_parameter(model, config_mode)

    def _wind_solar_battery_parameter(self, model, config_mode):
        self._wind_parameter(model, config_mode)
        self._solar_parameter(model, config_mode)
        self._battery_parameter(model, config_mode)


class WSBvar(WVar, SVar, BVar):
    def __init__(self, model, config_mode):
        self._wind_solar_battery_variable(model, config_mode)

    def _wind_solar_battery_variable(self, model, config_mode):
        self._wind_variable(model, config_mode)
        self._solar_variable(model, config_mode)
        self._battery_variable(model, config_mode)


class WSBobj(WObj, SObj, BObj):
    def __init__(self, model, config_mode):
        self._wind_solar_battery_objective(model, config_mode)

    def _wind_solar_battery_objective(self, model, config_mode):
        self._wind_objective(model, config_mode)
        self._solar_objective(model, config_mode)
        self._battery_objective(model, config_mode)
        self._obj_wind_solar_battery_revenue(model)

    def _obj_wind_solar_battery_revenue(self, model):
        def obj_wind_solar_battery_revenue_rule(model, t):
            return model.SOLAR_GRID_REVENUE - (model.SOLAR_INV_COST + model.SOLAR_PROD_COST) + \
                model.WIND_GRID_REVENUE - (model.WIND_INV_COST + model.WIND_PROD_COST) + \
                (model.BATTERY_GRID_REVENUE - model.BATTERY_GRID_COST) - (model.BATTERY_INV_COST + model.BATTERY_PROD_COST)
        model.objective = Objective(rule=obj_wind_solar_battery_revenue_rule, sense=maximize)


class WSBcon(WCon, SCon, BCon):
    def __init__(self, model, config_mode):
        self._wind_solar_battery_constraint(model, config_mode)

    def _wind_solar_battery_constraint(self, model, config_mode):
        self._wind_constraint(model, config_mode)
        self._solar_constraint(model, config_mode)
        self._battery_constraint(model, config_mode)

        # self._wind_solar_battery_charge_exp1(model)          # only grid charge
        # self._wind_solar_battery_charge_exp2(model)          # only wind charge
        self._wind_solar_battery_charge_exp3(model)          # wind and grid charge

    def _wind_solar_battery_charge_exp1(self, model):
        def wind_solar_battery_charge_exp1_rule(model, t):
            return model.B_CHARGE[t] == model.GtoB[t]
        model.wind_solar_battery_charge_exp1 = Constraint(model.PERIOD, rule=wind_solar_battery_charge_exp1_rule)

    def _wind_solar_battery_charge_exp2(self, model):
        def wind_solar_battery_charge_exp2_rule(model, t):
            return model.B_CHARGE[t] == model.WtoB[t] + model.StoB[t]
        model.wind_solar_battery_charge_exp2 = Constraint(model.PERIOD, rule=wind_solar_battery_charge_exp2_rule)

    def _wind_solar_battery_charge_exp3(self, model):
        def wind_solar_battery_charge_exp3_rule(model, t):
            return model.B_CHARGE[t] == model.WtoB[t] + model.StoB[t] + model.GtoB[t]
        model.wind_solar_battery_charge_exp3 = Constraint(model.PERIOD, rule=wind_solar_battery_charge_exp3_rule)

