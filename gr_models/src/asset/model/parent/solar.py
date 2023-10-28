from pyomo.environ import *


class SSet:
    def __init__(self, model, config_mode):
        # self._solar_set(model, config_mode)
        pass

    def _solar_set(self, model, config_mode):
        self._PERIOD(model)

        return self

    def _PERIOD(self, model):
        model.PERIOD = Set()


class SPar:
    def __init__(self, model, config_mode):
        self._solar_parameter(model, config_mode)

    def _solar_parameter(self, model, config_mode):
        self._solar_poi(model)
        self._solar_cost_inverter(model)
        self._solar_cost_bos(model)
        self._solar_cost_panel(model)
        self._solar_cost_fix(model)
        self._solar_cost_variable(model)
        self._solar_panel_degradation(model)
        self._solar_inv_eff(model)
        self._solar_inv_pre_loss(model)
        self._solar_inv_post_loss(model)

        self._solar_ratio_fix(model)
        self._solar_ratio_lb_min(model)
        self._solar_ratio_ub_max(model)
        self._solar_size_fix(model)
        self._solar_size_lb_min(model)
        self._solar_size_ub_max(model)

        self._solar_resource(model)
        # self._solar_lmp(model)

        return self


    def _solar_poi(self, model):
        model.solar_poi = Param()

    def _solar_cost_inverter(self, model):
        model.solar_cost_inverter = Param()

    def _solar_cost_bos(self, model):
        model.solar_cost_bos = Param()

    def _solar_cost_panel(self, model):
        model.solar_cost_panel = Param()

    def _solar_cost_fix(self, model):
        model.solar_cost_fix = Param()

    def _solar_cost_variable(self, model):
        model.solar_cost_variable = Param()

    def _solar_panel_degradation(self, model):
        model.solar_panel_degradation = Param()

    def _solar_inv_eff(self, model):
        model.solar_inv_eff = Param()

    def _solar_inv_pre_loss(self, model):
        model.solar_inv_pre_loss = Param(default=0)

    def _solar_inv_post_loss(self, model):
        model.solar_inv_post_loss = Param(default=0)

    def _solar_ratio_fix(self, model):
        model.solar_ratio_fix = Param()

    def _solar_ratio_lb_min(self, model):
        model.solar_ratio_lb_min = Param(default=1)

    def _solar_ratio_ub_max(self, model):
        model.solar_ratio_ub_max = Param(default=1.5)

    def _solar_size_fix(self, model):
        model.solar_size_fix = Param()

    def _solar_size_lb_min(self, model):
        model.solar_size_lb_min = Param(default=3)

    def _solar_size_ub_max(self, model):
        model.solar_size_ub_max = Param(default=10)

    def _solar_resource(self, model):
        model.solar = Param(model.PERIOD)

    def _solar_lmp(self, model):
        model.solar_lmp = Param(model.PERIOD)


class SVar:
    def __init__(self, model, config_mode):
        self._solar_variable(model, config_mode)


    def _solar_variable(self, model, config_mode):
        self._SOLAR_INV_COST(model)
        self._SOLAR_PROD_COST(model)
        self._SOLAR_GRID_REVENUE(model)
        self._SOLAR_AC_SIZE(model)
        self._SOLAR_DC_SIZE(model)
        self._SOLAR_DC_PROD(model)
        self._StoA(model)
        self._SLoss_DC(model)
        self._SLoss_AC(model)
        self._SOLAR_DC_INV(model)
        self._SOLAR_AC_INV(model)

        return self

    def _SOLAR_INV_COST(self, model):
        model.SOLAR_INV_COST = Var(within=NonNegativeReals, initialize=0)

    def _SOLAR_PROD_COST(self, model):
        model.SOLAR_PROD_COST = Var(within=NonNegativeReals, initialize=0)

    def _SOLAR_GRID_REVENUE(self, model):
        model.SOLAR_GRID_REVENUE = Var(within=NonNegativeReals, initialize=0)

    def _SOLAR_AC_SIZE(self, model):
        model.SOLAR_AC_SIZE = Var(within=NonNegativeReals, initialize=0)

    def _SOLAR_DC_SIZE(self, model):
        model.SOLAR_DC_SIZE = Var(within=NonNegativeReals, initialize=0)

    def _SOLAR_DC_PROD(self, model):
        model.SOLAR_DC_PROD = Var(model.PERIOD, within=NonNegativeReals, initialize=0)

    def _StoA(self, model):
        model.StoA = Var(model.PERIOD, within=NonNegativeReals, initialize=0)

    def _SLoss_DC(self, model):
        model.SLoss_DC = Var(model.PERIOD, within=NonNegativeReals, initialize=0)

    def _SLoss_AC(self, model):
        model.SLoss_AC = Var(model.PERIOD, within=NonNegativeReals, initialize=0)

    def _SOLAR_DC_INV(self, model):
        model.SOLAR_DC_INV = Var(model.PERIOD, within=NonNegativeReals, initialize=0)

    def _SOLAR_AC_INV(self, model):
        model.SOLAR_AC_INV = Var(model.PERIOD, within=NonNegativeReals, initialize=0)


class SObj:
    def __init__(self, model, config_mode):
        self._solar_objective(model, config_mode)


    def _solar_objective(self, model, config_mode):
        self._obj_solar_revenue(model) if config_mode['info_asset_mode'][0] == 'solar' else None
        self._solar_exp_grid_revenue(model)
        self._solar_exp_invest_cost(model)
        self._solar_exp_prod_cost(model)

        return self


    def _obj_solar_revenue(self, model):
        def obj_solar_revenue_rule(model):
            return model.SOLAR_GRID_REVENUE - (model.SOLAR_INV_COST + model.SOLAR_PROD_COST)
        model.objective = Objective(rule=obj_solar_revenue_rule, sense=maximize)

    def _solar_exp_grid_revenue(self, model):
        def solar_exp_grid_revenue_rule(model):
            return model.SOLAR_GRID_REVENUE == sum(model.lmp[t] * model.StoA[t] for t in model.PERIOD)

        model.solar_exp_grid_revenue = Constraint(rule=solar_exp_grid_revenue_rule)

    def _solar_exp_invest_cost(self, model):
        def solar_exp_invest_cost_rule(model):
            return model.SOLAR_INV_COST == model.solar_cost_inverter * model.SOLAR_AC_SIZE + \
                (model.solar_cost_bos + model.solar_cost_panel) * model.SOLAR_DC_SIZE

        model.solar_exp_invest_cost = Constraint(rule=solar_exp_invest_cost_rule)

    def _solar_exp_prod_cost(self, model):
        def solar_exp_prod_cost_rule(model):
            return model.SOLAR_PROD_COST == model.solar_cost_fix * model.SOLAR_AC_SIZE + \
                model.solar_cost_variable * sum(model.StoA[t] for t in model.PERIOD)

        model.solar_exp_prod_cost = Constraint(rule=solar_exp_prod_cost_rule)


class SCon:
    def __init__(self, model, config_mode):
        self._solar_constraint(model, config_mode)


    def _solar_constraint(self, model, config_mode):
        self._solar_at_poi(model)

        self._solar_size_less_than_poi(model)
        self._solar_ratio(model)

        self._solar_dc_prod(model)
        self._solar_dc_inv_prod(model)
        self._solar_ac_inv_prod(model)
        self._solar_ac_inv_limit(model)
        self._solar_only_prod(model) if config_mode['info_asset_mode'][0] == 'solar' else None
        self._solar_only_prod(model) if config_mode['info_asset_mode'][0] == 'wind_and_solar' else None

        mode_inv = config_mode['solar_inverter_mode'][0]
        if 'fix' in mode_inv:
            self._solar_ac_inv_size_equal_to(model)
            del model.solar_size_less_than_poi
        elif 'range' in mode_inv:
            self._solar_ac_size_lb(model)
            self._solar_ac_size_ub(model)

        mode_ratio = config_mode['solar_ratio_mode'][0]
        if 'fix' in mode_ratio:
            self._solar_ratio_equal_to(model)
        elif 'range' in mode_ratio:
            self._solar_ratio_lb(model)
            self._solar_ratio_ub(model)

        return self
    def _solar_only_prod(self, model):
        def solar_ac_prod_rule(model, t):
            return model.SOLAR_AC_INV[t] * (1 - model.solar_inv_post_loss) \
                - model.SLoss_AC[t] == \
                model.StoA[t]
        model.solar_to_asset = Constraint(model.PERIOD, rule=solar_ac_prod_rule)


    def _solar_at_poi(self, model):
        def solar_at_poi_rule(model, t):
            return model.StoA[t] <= model.solar_poi
        model.solar_at_poi = Constraint(model.PERIOD, rule=solar_at_poi_rule)

    def _solar_size_less_than_poi(self, model):
        def solar_size_less_than_poi_rule(model):
            return model.SOLAR_AC_SIZE <= model.solar_poi
        model.solar_size_less_than_poi = Constraint(rule=solar_size_less_than_poi_rule)

    def _solar_dc_prod(self, model):
        def solar_dc_prod_rule(model, t):
            return model.SOLAR_DC_PROD[t] == \
                model.SOLAR_DC_SIZE * model.solar[t] * (1 - model.solar_panel_degradation)

        model.solar_dc_prod = Constraint(model.PERIOD, rule=solar_dc_prod_rule)

    def _solar_dc_inv_prod(self, model):
        def solar_dc_inv_prod_rule(model, t):
            return model.SOLAR_DC_PROD[t] * (1 - model.solar_inv_pre_loss) - model.SLoss_DC[t] == \
                model.SOLAR_DC_INV[t]

        model.solar_dc_inv_prod = Constraint(model.PERIOD, rule=solar_dc_inv_prod_rule)

    def _solar_ac_inv_prod(self, model):
        def solar_ac_inv_prod_rule(model, t):
            return model.SOLAR_DC_INV[t] * model.solar_inv_eff == model.SOLAR_AC_INV[t]

        model.solar_ac_inv_prod = Constraint(model.PERIOD, rule=solar_ac_inv_prod_rule)


    def _solar_ac_inv_limit(self, model):
        def solar_ac_inv_limit_rule(model, t):
            return model.SOLAR_AC_INV[t] <= model.SOLAR_AC_SIZE

        model.solar_ac_inv_limit = Constraint(model.PERIOD, rule=solar_ac_inv_limit_rule)

    def _solar_ac_inv_size_equal_to(self, model):  ## TODO: que es mas effciente. evaluar el modelo con
        def solar_ac_inv_size_equal_to_rule(model):
            return model.SOLAR_AC_SIZE == model.solar_size_fix

        model.solar_ac_inv_size_equal_to = Constraint(rule=solar_ac_inv_size_equal_to_rule)

    def _solar_ac_size_lb(self, model):
        def solar_ac_size_lb_rule(model):
            return model.solar_size_lb_min <= model.SOLAR_AC_SIZE

        model.solar_ac_size_lb = Constraint(rule=solar_ac_size_lb_rule)

    def _solar_ac_size_ub(self, model):
        def solar_ac_size_ub_rule(model):
            return model.SOLAR_AC_SIZE <= model.solar_size_ub_max

        model.solar_ac_size_ub = Constraint(rule=solar_ac_size_ub_rule)

    def _solar_ratio(self, model):
        def solar_ratio_rule(model):
            return model.SOLAR_DC_SIZE >= model.SOLAR_AC_SIZE

        model.solar_ratio = Constraint(rule=solar_ratio_rule)

    def _solar_ratio_equal_to(self, model):
        def solar_ratio_equal_to_rule(model):
            return model.SOLAR_DC_SIZE == model.SOLAR_AC_SIZE * model.solar_ratio_fix

        model.solar_ratio_equal_to = Constraint(rule=solar_ratio_equal_to_rule)

    def _solar_ratio_lb(self, model):
        def solar_ratio_lb_rule(model):
            return model.SOLAR_DC_SIZE >= model.solar_ratio_lb_min * model.SOLAR_AC_SIZE

        model.solar_ratio_range_lb = Constraint(rule=solar_ratio_lb_rule)

    def _solar_ratio_ub(self, model):
        def solar_ratio_ub_rule(model):
            return model.SOLAR_DC_SIZE <= model.solar_ratio_ub_max * model.SOLAR_AC_SIZE
        model.solar_ratio_range_ub = Constraint(rule=solar_ratio_ub_rule)
