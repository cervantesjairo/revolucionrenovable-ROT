from pyomo.environ import *


class BSet:
    def __init__(self, model, config_mode):
        # self._battery_set(model, config_mode)
        pass


    def _battery_set(self, model, config_mode):
        self._PERIOD(model)

        return self

    def _PERIOD(self, model):
        model.PERIOD = Set()


class BPar:
    def __init__(self, model, config_mode):
        self._battery_parameter(model, config_mode)

    def _battery_parameter(self, model, config_mode):

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
        model.battery_poi = Param()

    def _battery_power_fix(self, model):
        model.battery_power_fix = Param()

    def _battery_power_lb_min(self, model):
        model.battery_power_lb_min = Param()

    def _battery_power_ub_max(self, model):
        model.battery_power_ub_max = Param()

    def _battery_duration_fix(self, model):
        model.battery_duration_fix = Param()

    def _battery_duration_lb_min(self, model):
        model.battery_duration_lb_min = Param()

    def _battery_duration_ub_max(self, model):
        model.battery_duration_ub_max = Param()

    def _battery_cost_power(self, model):
        model.battery_cost_power = Param()

    def _battery_cost_capacity(self, model):
        model.battery_cost_capacity = Param()

    def _battery_cost_fix(self, model):
        model.battery_cost_fix = Param()

    def _battery_cost_variable(self, model):
        model.battery_cost_variable = Param()

    def _battery_rte(self, model):
        model.battery_rte = Param()

    def _battery_rte_charge(self, model):
        model.battery_rte_charge = Param(default=1)

    def _battery_rte_discharge(self, model):
        model.battery_rte_discharge = Param(default=1)

    def _battery_dod_lb_min(self, model):
        model.battery_dod_lb_min = Param()

    def _battery_dod_ub_max(self, model):
        model.battery_dod_ub_max = Param()

    def _battery_cycle_lb_min(self, model):
        model.battery_cycle_lb_min = Param()

    def _battery_cycle_ub_max(self, model):
        model.battery_cycle_ub_max = Param()

    def _battery_lmp(self, model):
        model.battery_lmp = Param(model.PERIOD)


class BVar:
    def __init__(self, model, config_mode):
        self._battery_variable(model, config_mode)

    def _battery_variable(self, model, config_mode):
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
        self._WtoB(model) if config_mode['info_asset_mode'][0] in ['wind_and_battery', 'wind_and_solar_and_battery'] else None
        self._StoB(model) if config_mode['info_asset_mode'][0] in ['solar_and_battery', 'wind_and_solar_and_battery'] else None

        return self


    def _BATTERY_INV_COST(self, model):
        model.BATTERY_INV_COST = Var(within=NonNegativeReals, initialize=0)

    def _BATTERY_PROD_COST(self, model):
        model.BATTERY_PROD_COST = Var(within=NonNegativeReals, initialize=0)

    def _BATTERY_GRID_COST(self, model):
        model.BATTERY_GRID_COST = Var(within=NonNegativeReals, initialize=0)

    def _BATTERY_GRID_REVENUE(self, model):
        model.BATTERY_GRID_REVENUE = Var(within=NonNegativeReals, initialize=0)


    def _BATTERY_SIZE_POWER(self, model):
        model.BATTERY_SIZE_POWER = Var(within=NonNegativeReals, initialize=0)

    def _BATTERY_SIZE_CAPACITY(self, model):
        model.BATTERY_SIZE_CAPACITY = Var(within=NonNegativeReals, initialize=0)

    def _B_SOC(self, model):
        model.B_SOC = Var(model.PERIOD, within=NonNegativeReals, initialize=0)

    def _B_STATE(self, model):
        model.B_STATE = Var(model.PERIOD, within=Binary, initialize=0)

    def _B_CHARGE(self, model):
        model.B_CHARGE = Var(model.PERIOD, within=NonNegativeReals, initialize=0)

    def _B_DISCHARGE(self, model):
        model.B_DISCHARGE = Var(model.PERIOD, within=NonNegativeReals, initialize=0)
        
    def _GtoB(self, model):
        model.GtoB = Var(model.PERIOD, within=NonNegativeReals, initialize=0)
        
    def _BtoA(self, model):
        model.BtoA = Var(model.PERIOD, within=NonNegativeReals, initialize=0)
        
    def _WtoB(self, model):
        model.WtoB = Var(model.PERIOD, within=NonNegativeReals, initialize=0)
        
    def _StoB(self, model):
        model.StoB = Var(model.PERIOD, within=NonNegativeReals, initialize=0)
             
          
class BObj:
    def __init__(self, model, config_mode):
        self._battery_objective(model, config_mode)


    def _battery_objective(self, model, config_mode):
        self._obj_battery_revenue(model) if config_mode['info_asset_mode'][0] == 'battery' else None
        self._battery_exp_grid_revenue(model)
        self._battery_exp_grid_cost(model)
        self._battery_exp_invest_cost(model)
        self._battery_exp_prod_cost(model)

        return self

    def _obj_battery_revenue(self, model):
        def obj_battery_revenue_rule(model):
            return (model.BATTERY_GRID_REVENUE - model.BATTERY_GRID_COST) - (model.BATTERY_INV_COST + model.BATTERY_PROD_COST)
        model.objective = Objective(rule=obj_battery_revenue_rule, sense=maximize)

    def _battery_exp_grid_cost(self, model):
        def battery_exp_grid_cost_rule(model):
            return model.BATTERY_GRID_COST == \
                sum(model.lmp[t] * model.GtoB[t] for t in model.PERIOD)
        model.battery_exp_grid_cost = Constraint(rule=battery_exp_grid_cost_rule)

    def _battery_exp_grid_revenue(self, model):
        def battery_exp_grid_revenue_rule(model):
            return model.BATTERY_GRID_REVENUE == \
                sum(model.lmp[t] * model.B_DISCHARGE[t] for t in model.PERIOD)
        model.battery_exp_grid_revenue = Constraint(rule=battery_exp_grid_revenue_rule)

    def _battery_exp_invest_cost(self, model):
        def battery_exp_invest_cost_rule(model):
            return model.BATTERY_INV_COST == model.battery_cost_power * model.BATTERY_SIZE_POWER \
                + model.battery_cost_capacity * model.BATTERY_SIZE_CAPACITY

        model.battery_exp_invest_cost = Constraint(rule=battery_exp_invest_cost_rule)

    def _battery_exp_prod_cost(self, model):
        def battery_exp_prod_cost_rule(model):
            return model.BATTERY_PROD_COST == model.battery_cost_fix + model.BATTERY_SIZE_POWER + \
                model.battery_cost_variable * sum(model.B_DISCHARGE[t] for t in model.PERIOD)

        model.battery_exp_prod_cost = Constraint(rule=battery_exp_prod_cost_rule)


class BCon:
    def __init__(self, model, config_mode):
        self._battery_constraint(model, config_mode)

    def _battery_constraint(self, model, config_mode):
        self._wind_battery_prod(model) if config_mode['info_asset_mode'][0] in ['wind_and_battery',
                                                                                'wind_and_solar_and_battery'] else None
        self._solar_battery_prod(model) if config_mode['info_asset_mode'][0] in ['solar_and_battery',
                                                                                 'wind_and_solar_and_battery'] else None

        self._battery_only_charge(model) if config_mode['info_asset_mode'][0] == 'battery' else None
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

        mode_power = config_mode['battery_power_mode'][0]
        if 'fix' in mode_power:
            self._battery_power_equal_to(model)
            del model.battery_size_less_than_poi
            del model.battery_discharge_at_poi
            del model.battery_charge_at_poi
        elif 'range' in mode_power:
            self._battery_power_lb(model)
            self._battery_power_ub(model)

        self._battery_duration(model)
        mode_dur = config_mode['battery_duration_mode'][0]
        if 'fix' in mode_dur:
            self._battery_duration_equal_to(model)
        elif 'range' in mode_dur:
            self._battery_duration_lb(model)
            self._battery_duration_ub(model)

        mode_cycle = config_mode['battery_cycle_mode'][0]
        if 'unrestricted' in mode_cycle:
            pass
        elif 'range' in mode_cycle:
            self._battery_cycle_lb(model)
            self._battery_cycle_ub(model)

        mode_dod = config_mode['battery_dod_mode'][0]
        if 'unrestricted' in mode_dod:
            pass
        elif 'range' in mode_dod:
            self._battery_dod_lb(model)
            self._battery_dod_ub(model)

        return self

################################# BATTERY AND WIND/SOLAR #########################################
    def _wind_battery_prod(self, model):
        def wind_prod_rule(model, t):
            return model.WIND_SIZE * model.wind[t] - model.WLoss[t] - model.WtoB[t] == \
                model.WtoA[t]

        model.wind_to_asset = Constraint(model.PERIOD, rule=wind_prod_rule)

    def _solar_battery_prod(self, model):
        def solar_ac_prod_rule(model, t):
            return model.SOLAR_AC_INV[t] * (1 - model.solar_inv_post_loss) \
                - model.SLoss_AC[t] - model.StoB[t] == \
                model.StoA[t]
        model.solar_to_asset = Constraint(model.PERIOD, rule=solar_ac_prod_rule)

########################## BATTERY ONLY #########################################
    def _battery_discharge_at_poi(self, model):
        def battery_at_poi_rule(model, t):
            return model.B_DISCHARGE[t] <= model.battery_poi
        model.battery_charge_at_poi = Constraint(model.PERIOD, rule=battery_at_poi_rule)

    def _battery_charge_at_poi(self, model):
        def battery_at_poi_rule(model, t):
            return model.B_CHARGE[t] <= model.battery_poi
        model.battery_discharge_at_poi = Constraint(model.PERIOD, rule=battery_at_poi_rule)

    def _battery_size_less_than_poi(self, model):
        def battery_size_less_than_poi_rule(model):
            return model.BATTERY_SIZE_POWER <= model.battery_poi
        model.battery_size_less_than_poi = Constraint(rule=battery_size_less_than_poi_rule)

    def _battery_power_equal_to(self, model):
        def battery_power_equal_to_rule(model):
            return model.BATTERY_SIZE_POWER == model.battery_power_fix
        model.battery_power_equal_to = Constraint(rule=battery_power_equal_to_rule)

    def _battery_power_lb(self, model):
        def battery_power_lb_rule(model):
            return model.battery_power_lb_min <= model.BATTERY_SIZE_POWER
        model.battery_power_lb = Constraint(rule=battery_power_lb_rule)

    def _battery_power_ub(self, model):
        def battery_power_ub_rule(model):
            return model.BATTERY_SIZE_POWER <= model.battery_power_ub_max
        model.battery_power_ub = Constraint(rule=battery_power_ub_rule)

    def _battery_duration(self, model):
        def battery_duration_rule(model):
            return model.BATTERY_SIZE_POWER <= model.BATTERY_SIZE_CAPACITY

        model.battery_duration = Constraint(rule=battery_duration_rule)

    def _battery_duration_equal_to(self, model):
        def battery_duration_equal_to_rule(model):
            return model.BATTERY_SIZE_POWER * model.battery_duration_fix == model.BATTERY_SIZE_CAPACITY
        model.battery_duration_equal_to = Constraint(rule=battery_duration_equal_to_rule)

    def _battery_duration_lb(self, model):
        def battery_duration_lb_rule(model):
            return model.BATTERY_SIZE_CAPACITY >= model.battery_duration_lb_min * model.BATTERY_SIZE_POWER
        model.battery_duration_lb = Constraint(rule=battery_duration_lb_rule)

    def _battery_duration_ub(self, model):
        def battery_duration_ub_rule(model):
            return model.BATTERY_SIZE_CAPACITY <= model.battery_duration_ub_max * model.BATTERY_SIZE_POWER
        model.battery_duration_ub = Constraint(rule=battery_duration_ub_rule)

    def _battery_only_charge(self, model):
        def battery_only_charge_rule(model, t):
            return model.B_CHARGE[t] == model.GtoB[t]
        model.battery_only_charge = Constraint(model.PERIOD, rule=battery_only_charge_rule)
        
    def _battery_discharge_grid(self, model):
        def battery_discharge_grid_rule(model, t):
            return model.B_DISCHARGE[t] == model.BtoA[t]
        model.battery_discharge_grid = Constraint(model.PERIOD, rule=battery_discharge_grid_rule)

    def _battery_soc_rte_charge(self, model):
        def battery_soc_rte_charge_rule(model, t):
            if t < 1:
                return model.B_SOC[t] == model.battery_rte * model.B_CHARGE[t] - model.B_DISCHARGE[t]
            else:
                return model.B_SOC[t] == \
                    model.B_SOC[t - 1] + model.battery_rte * model.B_CHARGE[t] - model.B_DISCHARGE[t]

        model.battery_soc_rte_charge = Constraint(model.PERIOD, rule=battery_soc_rte_charge_rule)

    def _battery_soc_rte_charge_discharge(self, model):
        def battery_soc_rte_charge_discharge_rule(model, t):
            if t < 1:
                return model.B_SOC[t] == \
                    model.battery_rte_charge * model.B_CHARGE[t] - model.battery_rte_discharge * model.B_DISCHARGE[t]
            else:
                return model.B_SOC[t] == model.B_SOC[t - 1] \
                    + model.battery_rte_charge * model.B_CHARGE[t] - model.battery_rte_discharge * model.B_DISCHARGE[t]

        model.battery_soc_rte_charge_discharge = Constraint(model.PERIOD, rule=battery_soc_rte_charge_discharge_rule)

    def _battery_state_charge(self, model):
        def battery_state_charge_rule(model, t):
            return model.B_CHARGE[t] <= 1000 * model.B_STATE[t]

        model.battery_state_charge = Constraint(model.PERIOD, rule=battery_state_charge_rule)

    def _battery_state_discharge(self, model):
        def battery_state_discharge_rule(model, t):
            return model.B_DISCHARGE[t] <= 1000 * (1 - model.B_STATE[t])

        model.battery_state_discharge = Constraint(model.PERIOD, rule=battery_state_discharge_rule)

    def _battery_charge_limit(self, model):
        def battery_charge_limit_rule(model, t):
            return model.B_CHARGE[t] <= model.BATTERY_SIZE_POWER

        model.battery_charge_limit = Constraint(model.PERIOD, rule=battery_charge_limit_rule)

    def _battery_discharge_limit(self, model):
        def battery_discharge_limit_rule(model, t):
            return model.B_DISCHARGE[t] <= model.BATTERY_SIZE_POWER

        model.battery_discharge_limit = Constraint(model.PERIOD, rule=battery_discharge_limit_rule)

    def _battery_soc_limit(self, model):
        def battery_soc_limit_rule(model, t):
            return model.B_SOC[t] <= model.BATTERY_SIZE_CAPACITY

        model.battery_soc_limit = Constraint(model.PERIOD, rule=battery_soc_limit_rule)

    def _battery_dod_lb(self, model):
        def battery_dod_lb_rule(model, t):
            return model.battery_dod_lb_min * model.BATTERY_SIZE_CAPACITY <= model.B_SOC[t]

        model.battery_dod_lb = Constraint(model.PERIOD, rule=battery_dod_lb_rule)

    def _battery_dod_ub(self, model):
        def battery_dod_ub_rule(model, t):
            return model.B_SOC[t] <= model.battery_dod_ub_max * model.BATTERY_SIZE_CAPACITY

        model.battery_dod_ub = Constraint(model.PERIOD, rule=battery_dod_ub_rule)

    def _battery_cycle_lb(self, model):
        def battery_cycle_lb_rule(model):
            return model.battery_cycle_lb_min * model.BATTERY_SIZE_CAPACITY \
                <= sum(model.B_DISCHARGE[t] for t in model.PERIOD)

        model.battery_cycle_lb = Constraint(rule=battery_cycle_lb_rule)

    def _battery_cycle_ub(self, model):
        def battery_cycle_ub_rule(model):
            return sum(model.B_DISCHARGE[t] for t in model.PERIOD) <= \
                model.battery_cycle_ub_max * model.BATTERY_SIZE_CAPACITY

        model.battery_cycle_ub = Constraint(rule=battery_cycle_ub_rule)
