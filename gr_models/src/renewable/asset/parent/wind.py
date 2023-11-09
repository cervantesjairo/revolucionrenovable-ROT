from pyomo.environ import *


from gr_models.src.renewable.asset.nomenclature.wind import WindNomenclature as Wn
from gr_models.src.renewable.asset.utils import *


class WSet:
    def __init__(self, model, config_mode):
        # self._wind_set(model, config_mode)
        pass

    def _wind_set(self, model, config_mode):
        self._PERIOD(model)

        return self

    def _PERIOD(self, model):
        set(model, Wn.PERIOD)


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
        par(model=model, name=Wn.pPOI, time=None, default=None)

    def _wind_cost(self, model):
        par(model, Wn.pCost)

    def _wind_cost_inter(self, model):
        par(model, Wn.pCostInter)

    def _wind_cost_fix(self, model):
        par(model, Wn.pCostFix)

    def _wind_cost_variable(self, model):
        par(model, Wn.pCostVar)

    def _wind_size_fix(self, model):
        par(model, Wn.pSizeFix)

    def _wind_size_lb_min(self, model):
        par(model, Wn.pSizeLB)

    def _wind_size_ub_max(self, model):
        par(model, Wn.pSizeUB)

    def _wind_resource(self, model):
        par(model, Wn.pWIND, Wn.PERIOD)

    def _wind_lmp(self, model):
        par(model, Wn.pLMP, Wn.PERIOD)


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
        var_pos(model, Wn.vCostInvst)

    def _WIND_PROD_COST(self, model):
        var_pos(model, Wn.vCostProd)

    def _WIND_GRID_REVENUE(self, model):
        var_pos(model, Wn.vRevGrid)

    def _WIND_SIZE(self, model):
        var_pos(model, Wn.vSize)

    def _WtoA(self, model):
        var_pos(model, Wn.vWtoA, Wn.PERIOD, initialize=0)

    def _WLoss(self, model):
        var_pos(model, Wn.vWLoss, Wn.PERIOD, initialize=0)


class WObj:
    def __init__(self, model, config_mode):
        self._wind_objective(model, config_mode)

    def _wind_objective(self, model, config_mode):
        self._obj_wind_revenue(model) if config_mode == 'wind' else None
        self._wind_exp_grid_revenue(model)
        self._wind_exp_invest_cost(model)
        self._wind_exp_prod_cost(model)

        return self

    def _obj_wind_revenue(self, model):
        def obj_wind_revenue_rule(model):
            return v(model, Wn.vRevGrid) - (v(model, Wn.vCostInvst) + v(model, Wn.vCostProd))
        model.objective = Objective(rule=obj_wind_revenue_rule, sense=maximize)

    def _wind_exp_grid_revenue(self, model):
        def wind_exp_grid_revenue_rule(model):
            return v(model, Wn.vRevGrid) == sum(p(model, Wn.pLMP)[t] * v(model, Wn.vWtoA)[t] for t in s(model, Wn.PERIOD))
        model.wind_exp_grid_revenue = Constraint(rule=wind_exp_grid_revenue_rule)

    def _wind_exp_invest_cost(self, model):
        def wind_exp_invest_cost_rule(model):
            return v(model, Wn.vCostInvst) == p(model, Wn.pCost) * v(model, Wn.vSize)
        model.wind_exp_invest_cost = Constraint(rule=wind_exp_invest_cost_rule)

    def _wind_exp_prod_cost(self, model):
        def wind_exp_prod_cost_rule(model):
            return v(model, Wn.vCostProd) == p(model, Wn.pCostFix) * v(model, Wn.vSize) + \
                p(model, Wn.pCostVar) * sum(v(model, Wn.vWtoA)[t] for t in s(model, Wn.PERIOD))
        model.wind_exp_prod_cost = Constraint(rule=wind_exp_prod_cost_rule)


class WCon:
    def __init__(self, model, config_mode):
        self._wind_constraint(model, config_mode)

    def _wind_constraint(self, model, config_mode):
        self._wind_only_prod(model) if config_mode == 'wind' else None
        self._wind_only_prod(model) if config_mode == 'wind_and_solar' else None

        self._wind_at_poi(model)
        self._wind_size_less_than_poi(model)

        mode = 'fix'#config_mode['wind_size_mode'][0] TODO FIX
        if 'fix' in mode:
            self._wind_size_equal_to(model)
            del model.wind_size_less_than_poi
        elif 'range' in mode:
            self._wind_size_lb(model)
            self._wind_size_ub(model)

        return self

    def _wind_only_prod(self, model):
        def wind_prod_rule(model, t):
            return v(model, Wn.vSize) * p(model, Wn.pWIND)[t] - v(model, Wn.vWLoss)[t] == \
                v(model, Wn.vWtoA)[t]   # TODO add loss * (1 - model.solar_panel_degradation)
        model.wind_to_asset = Constraint(s(model, Wn.PERIOD), rule=wind_prod_rule)

    def _wind_at_poi(self, model):
        def wind_at_poi_rule(model, t):
            return v(model, Wn.vWtoA)[t] <= p(model, Wn.pPOI)
        model.wind_at_poi = Constraint(s(model, Wn.PERIOD), rule=wind_at_poi_rule)

    def _wind_size_less_than_poi(self, model):
        def wind_size_less_than_poi_rule(model):
            return v(model, Wn.vSize) <= p(model, Wn.pPOI)
        model.wind_size_less_than_poi = Constraint(rule=wind_size_less_than_poi_rule)

    def _wind_size_equal_to(self, model):  ## TODO: que es mas effciente. evaluar el modelo con
        def wind_size_equal_to_rule(model):
            return v(model, Wn.vSize) == p(model, Wn.pSizeFix)
        model.wind_size_equal_to = Constraint(rule=wind_size_equal_to_rule)

    def _wind_size_lb(self, model):
        def wind_size_lb_rule(model):
            return p(model, Wn.pSizeLB) <= v(model, Wn.vSize)
        model.wind_size_lb = Constraint(rule=wind_size_lb_rule)

    def _wind_size_ub(self, model):
        def wind_size_ub_rule(model):
            return v(model, Wn.vSize) <= p(model, Wn.pSizeUB)
        model.wind_size_ub = Constraint(rule=wind_size_ub_rule)

