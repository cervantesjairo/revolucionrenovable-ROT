from pyomo.environ import *


class WSet:
    def __init__(self, model, config_mode):
        # self._wind_set(model, config_mode)
        pass

    def _wind_set(self, model, config_mode):
        self._PERIOD(model)

        return self

    def _PERIOD(self, model):
        model.PERIOD = Set()


class WPar:
    def __init__(self, model, config_mode):
        self._wind_parameter(model, config_mode)

    def _wind_parameter(self, model, config_mode):
        self._wind_poi(model)
        self._wind_cost(model)
        self._wind_cost_inter(model)
        self._wind_cost_fix(model)
        self._wind_cost_variable(model)
        self._wind_size_fix(model)
        self._wind_size_lb_min(model)
        self._wind_size_ub_max(model)

        self._wind_resource(model)
        # self._wind_lmp(model)

        return self

    def _wind_poi(self, model):
        model.wind_poi = Param()

    def _wind_cost(self, model):
        model.wind_cost = Param()

    def _wind_cost_inter(self, model):
        model.wind_cost_inter = Param()

    def _wind_cost_fix(self, model):
        model.wind_cost_fix = Param()

    def _wind_cost_variable(self, model):
        model.wind_cost_variable = Param()

    def _wind_size_fix(self, model):
        model.wind_size_fix = Param()

    def _wind_size_lb_min(self, model):
        model.wind_size_lb_min = Param()

    def _wind_size_ub_max(self, model):
        model.wind_size_ub_max = Param()

    def _wind_resource(self, model):
        model.wind = Param(model.PERIOD)

    def _wind_lmp(self, model):
        model.wind_lmp = Param(model.PERIOD)


class WVar:
    def __init__(self, model, config_mode):
        self._wind_variable(model, config_mode)

    def _wind_variable(self, model, config_mode):
        self._WIND_INV_COST(model)
        self._WIND_PROD_COST(model)
        self._WIND_GRID_REVENUE(model)
        self._WIND_SIZE(model)
        self._WtoA(model)
        self._WLoss(model)

        return self

    def _WIND_INV_COST(self, model):
        model.WIND_INV_COST = Var(within=NonNegativeReals, initialize=0)

    def _WIND_PROD_COST(self, model):
        model.WIND_PROD_COST = Var(within=NonNegativeReals, initialize=0)

    def _WIND_GRID_REVENUE(self, model):
        model.WIND_GRID_REVENUE = Var(within=NonNegativeReals, initialize=0)

    def _WIND_SIZE(self, model):
        model.WIND_SIZE = Var(within=NonNegativeReals, initialize=0)

    def _WtoA(self, model):
        model.WtoA = Var(model.PERIOD, within=NonNegativeReals, initialize=0)

    def _WLoss(self, model):
        model.WLoss = Var(model.PERIOD, within=NonNegativeReals, initialize=0)


class WObj:
    def __init__(self, model, config_mode):
        self._wind_objective(model, config_mode)

    def _wind_objective(self, model, config_mode):
        self._obj_wind_revenue(model) if config_mode['info_asset_mode'][0] == 'wind' else None
        self._wind_exp_grid_revenue(model)
        self._wind_exp_invest_cost(model)
        self._wind_exp_prod_cost(model)

        return self

    def _obj_wind_revenue(self, model):
        def obj_wind_revenue_rule(model):
            return model.WIND_GRID_REVENUE - (model.WIND_INV_COST + model.WIND_PROD_COST)
        model.objective = Objective(rule=obj_wind_revenue_rule, sense=maximize)

    def _wind_exp_grid_revenue(self, model):
        def wind_exp_grid_revenue_rule(model):
            return model.WIND_GRID_REVENUE == sum(model.lmp[t] * model.WtoA[t] for t in model.PERIOD)

        model.wind_exp_grid_revenue = Constraint(rule=wind_exp_grid_revenue_rule)

    def _wind_exp_invest_cost(self, model):  # add interconnection cost
        def wind_exp_invest_cost_rule(model):
            return model.WIND_INV_COST == model.wind_cost * model.WIND_SIZE

        model.wind_exp_invest_cost = Constraint(rule=wind_exp_invest_cost_rule)

    def _wind_exp_prod_cost(self, model):
        def wind_exp_prod_cost_rule(model):
            return model.WIND_PROD_COST == model.wind_cost_fix * model.WIND_SIZE + \
                model.wind_cost_variable * sum(model.WtoA[t] for t in model.PERIOD)

        model.wind_exp_prod_cost = Constraint(rule=wind_exp_prod_cost_rule)


class WCon:
    def __init__(self, model, config_mode):
        self._wind_constraint(model, config_mode)

    def _wind_constraint(self, model, config_mode):
        self._wind_only_prod(model) if config_mode['info_asset_mode'][0] == 'wind' else None
        self._wind_only_prod(model) if config_mode['info_asset_mode'][0] == 'wind_and_solar' else None

        self._wind_at_poi(model)
        self._wind_size_less_than_poi(model)

        mode = config_mode['wind_size_mode'][0]
        if 'fix' in mode:
            self._wind_size_equal_to(model)
            del model.wind_size_less_than_poi
        elif 'range' in mode:
            self._wind_size_lb(model)
            self._wind_size_ub(model)

        return self

    def _wind_only_prod(self, model):
        def wind_prod_rule(model, t):
            return model.WIND_SIZE * model.wind[t] - model.WLoss[t] == \
                model.WtoA[t] #TODO add loss * (1 - model.solar_panel_degradation)

        model.wind_to_asset = Constraint(model.PERIOD, rule=wind_prod_rule)

    def _wind_at_poi(self, model):
        def wind_at_poi_rule(model, t):
            return model.WtoA[t] <= model.wind_poi
        model.wind_at_poi = Constraint(model.PERIOD, rule=wind_at_poi_rule)


    def _wind_size_less_than_poi(self, model):
        def wind_size_less_than_poi_rule(model):
            return model.WIND_SIZE <= model.wind_poi
        model.wind_size_less_than_poi = Constraint(rule=wind_size_less_than_poi_rule)

    def _wind_size_equal_to(self, model):  ## TODO: que es mas effciente. evaluar el modelo con
        def wind_size_equal_to_rule(model):
            return model.WIND_SIZE == model.wind_size_fix

        model.wind_size_equal_to = Constraint(rule=wind_size_equal_to_rule)

    def _wind_size_lb(self, model):
        def wind_size_lb_rule(model):
            return model.wind_size_lb_min <= model.WIND_SIZE

        model.wind_size_lb = Constraint(rule=wind_size_lb_rule)

    def _wind_size_ub(self, model):
        def wind_size_ub_rule(model):
            return model.WIND_SIZE <= model.wind_size_ub_max

        model.wind_size_ub = Constraint(rule=wind_size_ub_rule)
