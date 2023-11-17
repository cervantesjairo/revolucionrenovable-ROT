from pyomo.environ import *
from gr_models.src.renewable.asset.nomenclature.wind import WindNomenclature as Wn
from gr_models.src.renewable.asset.nomenclature.solar import SolarNomenclature as Sn
from gr_models.src.renewable.asset.nomenclature.battery import BatteryNomenclature as Bn

from gr_models.src.renewable.asset.utils import *


class BSet:
    def __init__(self, model, asset):
        # self._battery_set(model, asset)
        pass

    def _battery_set(self, model, asset):
        self._PERIOD(model)

        return self

    def _PERIOD(self, model):
        set(model, Bn.PERIOD)


class BPar:
    def __init__(self, model, asset):
        self._battery_parameter(model, asset)

    def _battery_parameter(self, model, asset):

        self._battery_poi(model)

        self._battery_power_fix(model)
        self._battery_power_lb_min(model)
        self._battery_power_ub_max(model)
        self._battery_duration_fix(model)
        self._battery_duration_lb_min(model)
        self._battery_duration_ub_max(model)
        self._battery_cost_power(model)
        self._battery_cost_capacity(model)
        self._battery_cost_fix(model)
        self._battery_cost_variable(model)
        self._battery_rte(model)
        self._battery_rte_charge(model)
        self._battery_rte_discharge(model)
        self._battery_dod_lb_min(model)
        self._battery_dod_ub_max(model)
        self._battery_cycle_lb_min(model)
        self._battery_cycle_ub_max(model)

        # self._battery_lmp(model)

        return self

    def _battery_poi(self, model):
        par(model, Bn.pPOI)

    def _battery_power_fix(self, model):
        par(model, Bn.pPowFix)

    def _battery_power_lb_min(self, model):
        par(model, Bn.pPowLB)

    def _battery_power_ub_max(self, model):
        par(model, Bn.pPowUB)

    def _battery_duration_fix(self, model):
        par(model, Bn.pDurFix)

    def _battery_duration_lb_min(self, model):
        par(model, Bn.pDurLB)

    def _battery_duration_ub_max(self, model):
        par(model, Bn.pDurUB)

    def _battery_cost_power(self, model):
        par(model, Bn.pCostPow)

    def _battery_cost_capacity(self, model):
        par(model, Bn.pCostCap)

    def _battery_cost_fix(self, model):
        par(model, Bn.pCostFix)

    def _battery_cost_variable(self, model):
        par(model, Bn.pCostVar)

    def _battery_rte(self, model):
        par(model, Bn.pRTE)

    def _battery_rte_charge(self, model):
        par(model, Bn.pRTEChg)

    def _battery_rte_discharge(self, model):
        par(model, Bn.pRTEDch)

    def _battery_dod_lb_min(self, model):
        par(model, Bn.pDODLB)

    def _battery_dod_ub_max(self, model):
        par(model, Bn.pDODUB)

    def _battery_cycle_lb_min(self, model):
        par(model, Bn.pCycLB)

    def _battery_cycle_ub_max(self, model):
        par(model, Bn.pCycUB)

    def _battery_lmp(self, model):
        par(model, Bn.pLMP)


class BVar:
    def __init__(self, model, asset):
        self._battery_variable(model, asset)

    def _battery_variable(self, model, asset):
        self._BATTERY_INV_COST(model)
        self._BATTERY_PROD_COST(model)
        self._BATTERY_GRID_COST(model)
        self._BATTERY_GRID_REVENUE(model)
        self._BATTERY_SIZE_POWER(model)
        self._BATTERY_SIZE_CAPACITY(model)
        self._B_SOC(model)
        self._B_STATE(model)
        self._B_CHARGE(model)
        self._B_DISCHARGE(model)
        self._GtoB(model)
        self._BtoA(model)
        self._WtoB(model) if asset.config in ['wind_battery', 'wind_solar_battery'] else None
        self._StoB(model) if asset.config in ['solar_battery', 'wind_solar_battery'] else None

        return self

    def _BATTERY_INV_COST(self, model):
        var_pos(model, Bn.vCostInvst, initialize=0)

    def _BATTERY_PROD_COST(self, model):
        var_pos(model, Bn.vCostProd, initialize=0)

    def _BATTERY_GRID_COST(self, model):
        var_pos(model, Bn.vCostGrid, initialize=0)

    def _BATTERY_GRID_REVENUE(self, model):
        var_pos(model, Bn.vRevGrid, initialize=0)

    def _BATTERY_SIZE_POWER(self, model):
        var_pos(model, Bn.vSizePow, initialize=0)

    def _BATTERY_SIZE_CAPACITY(self, model):
        var_pos(model, Bn.vSizeCap, initialize=0)

    def _B_SOC(self, model):
        var_pos(model, Bn.vSOC, Bn.PERIOD, initialize=0)

    def _B_STATE(self, model):
        var_bin(model, Bn.vState, Bn.PERIOD, initialize=0)

    def _B_CHARGE(self, model):
        var_pos(model, Bn.vChg, Bn.PERIOD, initialize=0)

    def _B_DISCHARGE(self, model):
        var_pos(model, Bn.vDch, Bn.PERIOD, initialize=0)

    def _GtoB(self, model):
        var_pos(model, Bn.vGtoB, Bn.PERIOD, initialize=0)

    def _BtoA(self, model):
        var_pos(model, Bn.vBtoA, Bn.PERIOD, initialize=0)

    def _WtoB(self, model):
        var_pos(model, Bn.vWtoB, Bn.PERIOD, initialize=0)

    def _StoB(self, model):
        var_pos(model, Bn.vStoB, Bn.PERIOD, initialize=0)

          
class BObj:
    def __init__(self, model, asset):
        self._battery_objective(model, asset)

    def _battery_objective(self, model, asset):
        self._obj_battery_revenue(model) if asset.config == 'battery' else None
        self._battery_exp_grid_revenue(model)
        self._battery_exp_grid_cost(model)
        self._battery_exp_invest_cost(model)
        self._battery_exp_prod_cost(model)

        return self

    def _obj_battery_revenue(self, model):
        def obj_battery_revenue_rule(model):
            return (v(model, Bn.vRevGrid) - v(model, Bn.vCostGrid)) - (v(model, Bn.vCostInvst) + v(model, Bn.vCostProd))
        model.objective = Objective(rule=obj_battery_revenue_rule, sense=maximize)

    def _battery_exp_grid_cost(self, model):
        def battery_exp_grid_cost_rule(model):
            return v(model, Bn.vCostGrid) == \
                sum(p(model, Bn.pLMP)[t] * v(model, Bn.vGtoB)[t] for t in s(model, Bn.PERIOD))
        model.battery_exp_grid_cost = Constraint(rule=battery_exp_grid_cost_rule)

    def _battery_exp_grid_revenue(self, model):
        def battery_exp_grid_revenue_rule(model):
            return v(model, Bn.vRevGrid) == \
                sum(p(model, Bn.pLMP)[t] * v(model, Bn.vDch)[t] for t in s(model, Bn.PERIOD))
        model.battery_exp_grid_revenue = Constraint(rule=battery_exp_grid_revenue_rule)

    def _battery_exp_invest_cost(self, model):
        def battery_exp_invest_cost_rule(model):
            return v(model, Bn.vCostInvst) == p(model, Bn.pCostPow) * v(model, Bn.vSizePow) \
                + p(model, Bn.pCostCap) * v(model, Bn.vSizeCap)
        model.battery_exp_invest_cost = Constraint(rule=battery_exp_invest_cost_rule)

    def _battery_exp_prod_cost(self, model):
        def battery_exp_prod_cost_rule(model):
            return v(model, Bn.vCostProd) == p(model, Bn.pCostFix) + v(model, Bn.vSizePow) + \
                p(model, Bn.pCostVar) * sum(v(model, Bn.vDch)[t] for t in s(model, Bn.PERIOD))
        model.battery_exp_prod_cost = Constraint(rule=battery_exp_prod_cost_rule)


class BCon:
    def __init__(self, model, asset):
        self._battery_constraint(model, asset)

    def _battery_constraint(self, model, asset):
        self._wind_battery_prod(model) if asset.config in ['wind_battery', 'wind_solar_battery'] else None
        self._solar_battery_prod(model) if asset.config in ['solar_battery', 'wind_solar_battery'] else None

        self._battery_only_charge(model) if asset.config == 'battery' else None
        self._battery_discharge_grid(model)
        
        self._battery_discharge_at_poi(model)
        self._battery_charge_at_poi(model)

        self._battery_size_less_than_poi(model)

        self._battery_state_charge(model)
        self._battery_state_discharge(model)
        self._battery_charge_limit(model)
        self._battery_discharge_limit(model)

        self._battery_soc_rte_charge(model)
        # self._battery_soc_rte_charge_discharge(model)
        self._battery_soc_limit(model)

        # mode_power = asset['battery_power_mode'][0] TODO FIX
        mode_power = 'fix'
        if 'fix' in mode_power:
            self._battery_power_equal_to(model)
            del model.battery_size_less_than_poi
            del model.battery_discharge_at_poi
            del model.battery_charge_at_poi
        elif 'range' in mode_power:
            self._battery_power_lb(model)
            self._battery_power_ub(model)

        self._battery_duration(model)
        # mode_dur = asset['battery_duration_mode'][0] TODO FIX
        mode_dur = 'fix'
        if 'fix' in mode_dur:
            self._battery_duration_equal_to(model)
        elif 'range' in mode_dur:
            self._battery_duration_lb(model)
            self._battery_duration_ub(model)

        # mode_cycle = asset['battery_cycle_mode'][0] TODO FIX
        mode_cycle = 'unrestricted'
        if 'unrestricted' in mode_cycle:
            pass
        elif 'range' in mode_cycle:
            self._battery_cycle_lb(model)
            self._battery_cycle_ub(model)

        # mode_dod = asset['battery_dod_mode'][0] TODO FIX
        mode_dod = 'unrestricted'
        if 'unrestricted' in mode_dod:
            pass
        elif 'range' in mode_dod:
            self._battery_dod_lb(model)
            self._battery_dod_ub(model)

        return self

    def _wind_battery_prod(self, model):
        def wind_prod_rule(model, t):
            return v(model, Wn.vSize) * p(model, Wn.pWIND)[t] - v(model, Wn.vWLoss)[t] - v(model, Bn.vWtoB)[t] == \
                v(model, Wn.vWtoA)[t]

        model.wind_to_asset = Constraint(s(model, Wn.PERIOD), rule=wind_prod_rule)

    def _solar_battery_prod(self, model):
        def solar_ac_prod_rule(model, t):
            return v(model, Sn.vInvAC)[t] * (1 - p(model, Sn.pInvACLoss)) \
                - v(model, Sn.vLossAC)[t] - v(model, Bn.vStoB)[t] == \
                v(model, Sn.vStoA)[t]
        model.solar_to_asset = Constraint(s(model, Sn.PERIOD), rule=solar_ac_prod_rule)

    def _battery_discharge_at_poi(self, model):
        def battery_at_poi_rule(model, t):
            return v(model, Bn.vDch)[t] <= p(model, Bn.pPOI)
        model.battery_charge_at_poi = Constraint(s(model, Bn.PERIOD), rule=battery_at_poi_rule)

    def _battery_charge_at_poi(self, model):
        def battery_at_poi_rule(model, t):
            return v(model, Bn.vChg)[t] <= p(model, Bn.pPOI)
        model.battery_discharge_at_poi = Constraint(s(model, Bn.PERIOD), rule=battery_at_poi_rule)

    def _battery_size_less_than_poi(self, model):
        def battery_size_less_than_poi_rule(model):
            return v(model, Bn.vSizePow) <= p(model, Bn.pPOI)
        model.battery_size_less_than_poi = Constraint(rule=battery_size_less_than_poi_rule)

    def _battery_power_equal_to(self, model):
        def battery_power_equal_to_rule(model):
            return v(model, Bn.vSizePow) == p(model, Bn.pPowFix)
        model.battery_power_equal_to = Constraint(rule=battery_power_equal_to_rule)

    def _battery_power_lb(self, model):
        def battery_power_lb_rule(model):
            return p(model, Bn.pPowLB) <= v(model, Bn.vSizePow)
        model.battery_power_lb = Constraint(rule=battery_power_lb_rule)

    def _battery_power_ub(self, model):
        def battery_power_ub_rule(model):
            return v(model, Bn.vSizePow) <= p(model, Bn.pPowUB)
        model.battery_power_ub = Constraint(rule=battery_power_ub_rule)

    def _battery_duration(self, model):
        def battery_duration_rule(model):
            return v(model, Bn.vSizePow) <= v(model, Bn.vSizeCap)
        model.battery_duration = Constraint(rule=battery_duration_rule)

    def _battery_duration_equal_to(self, model):
        def battery_duration_equal_to_rule(model):
            return v(model, Bn.vSizePow) * p(model, Bn.pDurFix) == v(model, Bn.vSizeCap)
        model.battery_duration_equal_to = Constraint(rule=battery_duration_equal_to_rule)

    def _battery_duration_lb(self, model):
        def battery_duration_lb_rule(model):
            return v(model, Bn.vSizeCap) >= p(model, Bn.pDurLB) * v(model, Bn.vSizePow)
        model.battery_duration_lb = Constraint(rule=battery_duration_lb_rule)

    def _battery_duration_ub(self, model):
        def battery_duration_ub_rule(model):
            return v(model, Bn.vSizeCap) <= p(model, Bn.pDurUB) * v(model, Bn.vSizePow)
        model.battery_duration_ub = Constraint(rule=battery_duration_ub_rule)

    def _battery_only_charge(self, model):
        def battery_only_charge_rule(model, t):
            return v(model, Bn.vChg)[t] == v(model, Bn.vGtoB)[t]
        model.battery_only_charge = Constraint(s(model, Bn.PERIOD), rule=battery_only_charge_rule)

    def _battery_discharge_grid(self, model):
        def battery_discharge_grid_rule(model, t):
            return v(model, Bn.vDch)[t] == v(model, Bn.vBtoA)[t]
        model.battery_discharge_grid = Constraint(s(model, Bn.PERIOD), rule=battery_discharge_grid_rule)
    def _battery_soc_rte_charge(self, model):
        def battery_soc_rte_charge_rule(model, t):
            if t < 1:
                return v(model, Bn.vSOC)[t] == p(model, Bn.pRTE) * v(model, Bn.vChg)[t] - v(model, Bn.vDch)[t]
            else:
                return v(model, Bn.vSOC)[t] == \
                    v(model, Bn.vSOC)[t - 1] + p(model, Bn.pRTE) * v(model, Bn.vChg)[t] - v(model, Bn.vDch)[t]

        model.battery_soc_rte_charge = Constraint(s(model, Bn.PERIOD), rule=battery_soc_rte_charge_rule)

    def _battery_soc_rte_charge_discharge(self, model):
        def battery_soc_rte_charge_discharge_rule(model, t):
            if t < 1:
                return v(model, Bn.vSOC)[t] == \
                    p(model, Bn.pRTEChg) * v(model, Bn.vChg)[t] - p(model, Bn.pRTEDch) * v(model, Bn.vDch)[t]
            else:
                return v(model, Bn.vSOC)[t] == v(model, Bn.vSOC)[t - 1] \
                    + p(model, Bn.pRTEChg) * v(model, Bn.vChg)[t] - p(model, Bn.pRTEDch) * v(model, Bn.vDch)[t]

        model.battery_soc_rte_charge_discharge = Constraint(s(model, Bn.PERIOD), rule=battery_soc_rte_charge_discharge_rule)

    def _battery_state_charge(self, model):
        def battery_state_charge_rule(model, t):
            return v(model, Bn.vChg)[t] <= 1000 * v(model, Bn.vState)[t]

        model.battery_state_charge = Constraint(s(model, Bn.PERIOD), rule=battery_state_charge_rule)

    def _battery_state_discharge(self, model):
        def battery_state_discharge_rule(model, t):
            return v(model, Bn.vDch)[t] <= 1000 * (1 - v(model, Bn.vState)[t])

        model.battery_state_discharge = Constraint(s(model, Bn.PERIOD), rule=battery_state_discharge_rule)

    def _battery_charge_limit(self, model):
        def battery_charge_limit_rule(model, t):
            return v(model, Bn.vChg)[t] <= v(model, Bn.vSizePow)

        model.battery_charge_limit = Constraint(s(model, Bn.PERIOD), rule=battery_charge_limit_rule)

    def _battery_discharge_limit(self, model):
        def battery_discharge_limit_rule(model, t):
            return v(model, Bn.vDch)[t] <= v(model, Bn.vSizePow)

        model.battery_discharge_limit = Constraint(s(model, Bn.PERIOD), rule=battery_discharge_limit_rule)

    def _battery_soc_limit(self, model):
        def battery_soc_limit_rule(model, t):
            return v(model, Bn.vSOC)[t] <= v(model, Bn.vSizeCap)

        model.battery_soc_limit = Constraint(s(model, Bn.PERIOD), rule=battery_soc_limit_rule)
    def _battery_dod_lb(self, model):
        def battery_dod_lb_rule(model, t):
            return p(model, Bn.pDODLB) * v(model, Bn.vSizeCap) <= v(model, Bn.vSOC)[t]

        model.battery_dod_lb = Constraint(s(model, Bn.PERIOD), rule=battery_dod_lb_rule)

    def _battery_dod_ub(self, model):
        def battery_dod_ub_rule(model, t):
            return v(model, Bn.vSOC)[t] <= p(model, Bn.pDODUB) * v(model, Bn.vSizeCap)

        model.battery_dod_ub = Constraint(s(model, Bn.PERIOD), rule=battery_dod_ub_rule)

    def _battery_cycle_lb(self, model):
        def battery_cycle_lb_rule(model):
            return p(model, Bn.pCycLB) * v(model, Bn.vSizeCap) \
                <= sum(v(model, Bn.vDch)[t] for t in s(model, Bn.PERIOD))

        model.battery_cycle_lb = Constraint(rule=battery_cycle_lb_rule)

    def _battery_cycle_ub(self, model):
        def battery_cycle_ub_rule(model):
            return sum(v(model, Bn.vDch)[t] for t in s(model, Bn.PERIOD)) <= \
                p(model, Bn.pCycUB) * v(model, Bn.vSizeCap)

        model.battery_cycle_ub = Constraint(rule=battery_cycle_ub_rule)
