from pyomo.environ import *


# from model.asset.parent.solar import SObj, SSet, SVar, SPar, SCon
# from model.asset.parent.battery import BObj, BSet, BVar, BPar, BCon
# from model.asset.nomenclature.battery import BatteryNomenclature as Bn
# from model.asset.nomenclature.wind import WindNomenclature as Wn
# from model.asset.nomenclature.solar import SolarNomenclature as Sn

from gr_models.src.renewable.asset.base.solar import SObj, SSet, SVar, SPar, SCon
from gr_models.src.renewable.asset.base.battery import BObj, BSet, BVar, BPar, BCon
from gr_models.src.renewable.asset.nomenclature.battery import BatteryNomenclature as Bn
from gr_models.src.renewable.asset.nomenclature.wind import WindNomenclature as Wn
from gr_models.src.renewable.asset.nomenclature.solar import SolarNomenclature as Sn


from gr_models.src.renewable.asset.utils import *

# from model.asset.utils import *

class SBset(SSet, BSet):
    def __init__(self, model, asset):
        pass


class SBpar(SPar, BPar):
    def __init__(self, model, asset):
        self._solar_battery_parameter(model, asset)

    def _solar_battery_parameter(self, model, asset):
        self._solar_parameter(model, asset)
        self._battery_parameter(model, asset)


class SBvar(SVar, BVar):
    def __init__(self, model, asset):
        self._solar_battery_variable(model, asset)

    def _solar_battery_variable(self, model, asset):
        self._solar_variable(model, asset)
        self._battery_variable(model, asset)


class SBobj(SObj, BObj):
    def __init__(self, model, asset):
        self._solar_battery_objective(model, asset)

    def _solar_battery_objective(self, model, asset):
        self._solar_objective(model, asset)
        self._battery_objective(model, asset)
        self._obj_solar_battery_revenue(model)

    # def _obj_solar_battery_revenue(self, model):
    #     def obj_solar_battery_revenue_rule(model, t):
    #         return model.SOLAR_GRID_REVENUE - (model.SOLAR_INV_COST + model.SOLAR_PROD_COST) + \
    #             (model.BATTERY_GRID_REVENUE - model.BATTERY_GRID_COST) - (model.BATTERY_INV_COST + model.BATTERY_PROD_COST)
    #     model.objective = Objective(rule=obj_solar_battery_revenue_rule, sense=maximize)

    def _obj_solar_battery_revenue(self, model):
        def obj_solar_battery_revenue_rule(model):
            return v(model, Sn.vRevGrid) - (v(model, Sn.vCostInvst) + v(model, Sn.vCostProd)) + \
                (v(model, Bn.vRevGrid) - v(model, Bn.vCostGrid)) - (v(model, Bn.vCostInvst) + v(model, Bn.vCostProd))
        model.objective = Objective(rule=obj_solar_battery_revenue_rule, sense=maximize)


class SBcon(SCon, BCon):
    def __init__(self, model, asset):
        self._solar_battery_constraint(model, asset)

    def _solar_battery_constraint(self, model, asset):
        self._solar_constraint(model, asset)
        self._battery_constraint(model, asset)

        # self._solar_battery_charge_exp1(model)          # only grid charge
        # self._solar_battery_charge_exp2(model)          # only solar charge
        self._solar_battery_charge_exp3(model)          # solar and grid charge

    # def _solar_battery_charge_exp1(self, model):
    #     def solar_battery_charge_exp1_rule(model, t):
    #         return model.B_CHARGE[t] == model.GtoB[t]
    #     model.solar_battery_charge_exp1 = Constraint(model.PERIOD, rule=solar_battery_charge_exp1_rule)
    #

    def _solar_battery_charge_exp1(self, model):
        def solar_battery_charge_exp1_rule(model, t):
            return v(model, Bn.vChg)[t] == v(model, Bn.vGtoB)[t]
        model.solar_battery_charge_exp2 = Constraint(s(model, Sn.PERIOD), rule=solar_battery_charge_exp1_rule)

    # def _solar_battery_charge_exp2(self, model):
    #     def solar_battery_charge_exp2_rule(model, t):
    #         return model.B_CHARGE[t] == model.StoB[t]
    #     model.solar_battery_charge_exp2 = Constraint(model.PERIOD, rule=solar_battery_charge_exp2_rule)
    #
    def _solar_battery_charge_exp2(self, model):
        def solar_battery_charge_exp2_rule(model, t):
            return v(model, Bn.vChg)[t] == v(model, Bn.vStoB)[t]
        model.solar_battery_charge_exp2 = Constraint(s(model, Sn.PERIOD), rule=solar_battery_charge_exp2_rule)

    # def _solar_battery_charge_exp3(self, model):
    #     def solar_battery_charge_exp3_rule(model, t):
    #         return model.B_CHARGE[t] == model.StoB[t] + model.GtoB[t]
    #     model.solar_battery_charge_exp3 = Constraint(model.PERIOD, rule=solar_battery_charge_exp3_rule)
    def _solar_battery_charge_exp3(self, model):
        def solar_battery_charge_exp3_rule(model, t):
            return v(model, Bn.vChg)[t] == v(model, Bn.vStoB)[t] + v(model, Bn.vGtoB)[t]
        model.solar_battery_charge_exp3 = Constraint(s(model, Sn.PERIOD), rule=solar_battery_charge_exp3_rule)
