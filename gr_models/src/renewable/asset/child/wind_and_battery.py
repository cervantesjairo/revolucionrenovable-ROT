from pyomo.environ import *

from gr_models.src.renewable.asset.base.wind import WObj, WSet, WVar, WPar, WCon
from gr_models.src.renewable.asset.base.battery import BObj, BSet, BVar, BPar, BCon
from gr_models.src.renewable.asset.nomenclature.battery import BatteryNomenclature as Bn
from gr_models.src.renewable.asset.nomenclature.wind import WindNomenclature as Wn
from gr_models.src.renewable.asset.nomenclature.solar import SolarNomenclature as Sn

from gr_models.src.renewable.asset.utils import *

# from model.asset.parent.wind import WObj, WSet, WVar, WPar, WCon
# from model.asset.parent.battery import BObj, BSet, BVar, BPar, BCon
# from model.asset.nomenclature.battery import BatteryNomenclature as Bn
# from model.asset.nomenclature.wind import WindNomenclature as Wn
# from model.asset.nomenclature.solar import SolarNomenclature as Sn
#
# from model.asset.utils import *

class WBset(WSet, BSet):
    def __init__(self, model, asset):
        pass


class WBpar(WPar, BPar):
    def __init__(self, model, asset):
        self._wind_battery_parameter(model, asset)

    def _wind_battery_parameter(self, model, asset):
        self._wind_parameter(model, asset)
        self._battery_parameter(model, asset)


class WBvar(WVar, BVar):
    def __init__(self, model, asset):
        self._wind_battery_variable(model, asset)

    def _wind_battery_variable(self, model, asset):
        self._wind_variable(model, asset)
        self._battery_variable(model, asset)


class WBobj(WObj, BObj):
    def __init__(self, model, asset):
        self._wind_battery_objective(model, asset)

    def _wind_battery_objective(self, model, asset):
        self._wind_objective(model, asset)
        self._battery_objective(model, asset)
        self._obj_wind_battery_revenue(model)

    # def _obj_wind_battery_revenue(self, model):
    #     def obj_wind_battery_revenue_rule(model, t):
    #         return model.WIND_GRID_REVENUE - (model.WIND_INV_COST + model.WIND_PROD_COST) + \
    #             (model.BATTERY_GRID_REVENUE - model.BATTERY_GRID_COST) - (model.BATTERY_INV_COST + model.BATTERY_PROD_COST)
    #
    #     model.objective = Objective(rule=obj_wind_battery_revenue_rule, sense=maximize)
    def _obj_wind_battery_revenue(self, model):
        def obj_wind_battery_revenue_rule(model):
            return v(model, Wn.vRevGrid) - (v(model, Wn.vCostInvst) + v(model, Wn.vCostProd)) + \
                (v(model, Bn.vRevGrid) - v(model, Bn.vCostGrid)) - (v(model, Bn.vCostInvst) + v(model, Bn.vCostProd))
        model.objective = Objective(rule=obj_wind_battery_revenue_rule, sense=maximize)


class WBcon(WCon, BCon):
    def __init__(self, model, asset):
        self._wind_battery_constraint(model, asset)

    def _wind_battery_constraint(self, model, asset):
        self._wind_constraint(model, asset)
        self._battery_constraint(model, asset)

        # self._wind_battery_charge_exp1(model)         # only grid charge
        # self._wind_battery_charge_exp2(model)         # only wind charge
        self._wind_battery_charge_exp3(model)           # wind and grid charge

    # def _wind_battery_charge_exp1(self, model):
    #     def wind_battery_charge_exp1_rule(model, t):
    #         return model.B_CHARGE[t] == model.GtoB[t]
    #     model.wind_battery_charge_exp1 = Constraint(model.PERIOD, rule=wind_battery_charge_exp1_rule)
    #
    # def _wind_battery_charge_exp2(self, model):
    #     def wind_battery_charge_exp2_rule(model, t):
    #         return model.B_CHARGE[t] == model.WtoB[t]
    #     model.wind_battery_charge_exp2 = Constraint(model.PERIOD, rule=wind_battery_charge_exp2_rule)
    #
    # def _wind_battery_charge_exp3(self, model):
    #     def wind_battery_charge_exp3_rule(model, t):
    #         return model.B_CHARGE[t] == model.GtoB[t] + model.WtoB[t]
    #     model.wind_battery_charge_exp3 = Constraint(model.PERIOD, rule=wind_battery_charge_exp3_rule)

    def _wind_battery_charge_exp1(self, model):
        def wind_battery_charge_exp1_rule(model, t):
            return v(model, Bn.vChg)[t] == v(model, Bn.vGtoB)[t]
        model.wind_battery_charge_exp1 = Constraint(model.PERIOD, rule=wind_battery_charge_exp1_rule)

    def _wind_battery_charge_exp2(self, model):
        def wind_battery_charge_exp2_rule(model, t):
            return v(model, Bn.vChg)[t] == v(model, Bn.vWtoB)[t]
        model.wind_battery_charge_exp2 = Constraint(model.PERIOD, rule=wind_battery_charge_exp2_rule)

    def _wind_battery_charge_exp3(self, model):
        def wind_battery_charge_exp3_rule(model, t):
            return v(model, Bn.vChg)[t] == v(model, Bn.vGtoB)[t] + v(model, Bn.vWtoB)[t]
        model.wind_battery_charge_exp3 = Constraint(model.PERIOD, rule=wind_battery_charge_exp3_rule)

