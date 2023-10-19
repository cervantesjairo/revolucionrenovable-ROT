from pyomo.environ import *

from muiscaenergy_models.src.asset.parent.solar import SObj, SSet, SVar, SPar, SCon
from muiscaenergy_models.src.asset.parent.battery import BObj, BSet, BVar, BPar, BCon


class SBset(SSet, BSet):
    def __init__(self, model, config_mode):
        pass


class SBpar(SPar, BPar):
    def __init__(self, model, config_mode):
        self._solar_battery_parameter(model, config_mode)


    def _solar_battery_parameter(self, model, config_mode):
        self._solar_parameter(model, config_mode)
        self._battery_parameter(model, config_mode)


class SBvar(SVar, BVar):
    def __init__(self, model, config_mode):
        self._solar_battery_variable(model, config_mode)

    def _solar_battery_variable(self, model, config_mode):
        self._solar_variable(model, config_mode)
        self._battery_variable(model, config_mode)


class SBobj(SObj, BObj):
    def __init__(self, model, config_mode):
        self._solar_battery_objective(model, config_mode)

    def _solar_battery_objective(self, model, config_mode):
        self._solar_objective(model, config_mode)
        self._battery_objective(model, config_mode)
        self._obj_solar_battery_revenue(model)

    def _obj_solar_battery_revenue(self, model):
        def obj_solar_battery_revenue_rule(model, t):
            return model.SOLAR_GRID_REVENUE - (model.SOLAR_INV_COST + model.SOLAR_PROD_COST) + \
                (model.BATTERY_GRID_REVENUE - model.BATTERY_GRID_COST) - (model.BATTERY_INV_COST + model.BATTERY_PROD_COST)
        model.objective = Objective(rule=obj_solar_battery_revenue_rule, sense=maximize)


class SBcon(SCon, BCon):
    def __init__(self, model, config_mode):
        self._solar_battery_constraint(model, config_mode)

    def _solar_battery_constraint(self, model, config_mode):
        self._solar_constraint(model, config_mode)
        self._battery_constraint(model, config_mode)

        # self._solar_battery_charge_exp1(model)          # only grid charge
        # self._solar_battery_charge_exp2(model)          # only solar charge
        self._solar_battery_charge_exp3(model)          # solar and grid charge

    def _solar_battery_charge_exp1(self, model):
        def solar_battery_charge_exp1_rule(model, t):
            return model.B_CHARGE[t] == model.GtoB[t]
        model.solar_battery_charge_exp1 = Constraint(model.PERIOD, rule=solar_battery_charge_exp1_rule)

    def _solar_battery_charge_exp2(self, model):
        def solar_battery_charge_exp2_rule(model, t):
            return model.B_CHARGE[t] == model.StoB[t]
        model.solar_battery_charge_exp2 = Constraint(model.PERIOD, rule=solar_battery_charge_exp2_rule)

    def _solar_battery_charge_exp3(self, model):
        def solar_battery_charge_exp3_rule(model, t):
            return model.B_CHARGE[t] == model.StoB[t] + model.GtoB[t]
        model.solar_battery_charge_exp3 = Constraint(model.PERIOD, rule=solar_battery_charge_exp3_rule)
