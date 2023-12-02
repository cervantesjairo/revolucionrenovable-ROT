from pyomo.environ import *

from gr_models.src.renewable.asset.nomenclature.solar import SolarNomenclature as Sn
from gr_models.src.renewable.asset.utils import *


class SSet:
    def __init__(self, model, asset):
        # self._solar_set(model, asset)
        pass

    def _solar_set(self, model, asset):
        self._PERIOD(model)

        return self

    def _PERIOD(self, model):
        set(model, Sn.PERIOD)


class SPar:
    def __init__(self, model, asset):
        self._solar_parameter(model, asset)

    def _solar_parameter(self, model, asset):
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
        par(model, Sn.pPOI)

    def _solar_cost_inverter(self, model):
        par(model, Sn.pCostInv)

    def _solar_cost_bos(self, model):
        par(model, Sn.pCostBos)
    def _solar_cost_panel(self, model):
        par(model, Sn.pCostPnl)

    def _solar_cost_fix(self, model):
        par(model, Sn.pCostFix)

    def _solar_cost_variable(self, model):
        par(model, Sn.pCostVar)

    def _solar_panel_degradation(self, model):
        par(model, Sn.pPnlDeg)

    def _solar_inv_eff(self, model):
        par(model, Sn.pInvEff)

    def _solar_inv_pre_loss(self, model):
        par(model, Sn.pInvDCLoss, default=0)

    def _solar_inv_post_loss(self, model):
        par(model, Sn.pInvACLoss, default=0)

    def _solar_ratio_fix(self, model):
        par(model, Sn.pRatFix)

    def _solar_ratio_lb_min(self, model):
        par(model, Sn.pRatLB, default=1)

    def _solar_ratio_ub_max(self, model):
        par(model, Sn.pRatUB, default=1.5)

    def _solar_size_fix(self, model):
        par(model, Sn.pSizeFix)

    def _solar_size_lb_min(self, model):
        par(model, Sn.pSizeLB, default=3)

    def _solar_size_ub_max(self, model):
        par(model, Sn.pSizeUB, default=10)

    def _solar_resource(self, model):
        par(model, Sn.pSOLAR, Sn.PERIOD)

    def _solar_lmp(self, model):
        par(model, Sn.pLMP, Sn.PERIOD)


class SVar:
    def __init__(self, model, asset):
        self._solar_variable(model, asset)

    def _solar_variable(self, model, asset):
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
        var_pos(model, Sn.vCostInvst, initialize=0)

    def _SOLAR_PROD_COST(self, model):
        var_pos(model, Sn.vCostProd, initialize=0)

    def _SOLAR_GRID_REVENUE(self, model):
        var_pos(model, Sn.vRevGrid, initialize=0)

    def _SOLAR_AC_SIZE(self, model):
        var_pos(model, Sn.vSizeAC, initialize=0)

    def _SOLAR_DC_SIZE(self, model):
        var_pos(model, Sn.vSizeDC, initialize=0)

    def _SOLAR_DC_PROD(self, model):
        var_pos(model, Sn.vProdDC, Sn.PERIOD, initialize=0)

    def _StoA(self, model):
        var_pos(model, Sn.vStoA, Sn.PERIOD, initialize=0)

    def _SLoss_DC(self, model):
        var_pos(model, Sn.vLossDC, Sn.PERIOD, initialize=0)

    def _SLoss_AC(self, model):
        var_pos(model, Sn.vLossAC, Sn.PERIOD, 0)

    def _SOLAR_DC_INV(self, model):
        var_pos(model, Sn.vInvDC, Sn.PERIOD, 0)

    def _SOLAR_AC_INV(self, model):
        var_pos(model, Sn.vInvAC, Sn.PERIOD, 0)


class SObj:
    def __init__(self, model, asset):
        self._solar_objective(model, asset)

    def _solar_objective(self, model, asset):
        self._obj_solar_revenue(model) if asset.config == 'solar' else None
        self._solar_exp_grid_revenue(model)
        self._solar_exp_invest_cost(model)
        self._solar_exp_prod_cost(model)

        return self

    def _obj_solar_revenue(self, model):
        def obj_solar_revenue_rule(model):
            return v(model, Sn.vRevGrid) - (v(model, Sn.vCostInvst) + v(model, Sn.vCostProd))
        model.objective = Objective(rule=obj_solar_revenue_rule, sense=maximize)

    def _solar_exp_grid_revenue(self, model):
        def solar_exp_grid_revenue_rule(model):
            return v(model, Sn.vRevGrid) == sum(p(model, Sn.pLMP)[t] * v(model, Sn.vStoA)[t] for t in s(model, Sn.PERIOD))
        model.solar_exp_grid_revenue = Constraint(rule=solar_exp_grid_revenue_rule)

    def _solar_exp_invest_cost(self, model):
        def solar_exp_invest_cost_rule(model):
            return v(model, Sn.vCostInvst) == p(model, Sn.pCostInv) * v(model, Sn.vSizeAC) + \
                (p(model, Sn.pCostBos) + p(model, Sn.pCostPnl)) * v(model, Sn.vSizeDC)
        model.solar_exp_invest_cost = Constraint(rule=solar_exp_invest_cost_rule)

    def _solar_exp_prod_cost(self, model):
        def solar_exp_prod_cost_rule(model):
            return v(model, Sn.vCostProd) == p(model, Sn.pCostFix) * v(model, Sn.vSizeAC) + \
                p(model, Sn.pCostVar) * sum(v(model, Sn.vStoA)[t] for t in s(model, Sn.PERIOD))
        model.solar_exp_prod_cost = Constraint(rule=solar_exp_prod_cost_rule)


class SCon:
    def __init__(self, model, asset):
        self._solar_constraint(model, asset)

    def _solar_constraint(self, model, asset):
        self._solar_at_poi(model)

        self._solar_size_less_than_poi(model)
        self._solar_ratio(model)

        self._solar_dc_prod(model)
        self._solar_dc_inv_prod(model)
        self._solar_ac_inv_prod(model)
        self._solar_ac_inv_limit(model)
        self._solar_only_prod(model) if asset.config == 'solar' else None
        self._solar_only_prod(model) if asset.config == 'wind_solar' else None

        mode_inv = asset.solar.mode.inv_conf
        if 'fix' in mode_inv:
            self._solar_ac_inv_size_equal_to(model)
            del model.solar_size_less_than_poi
        elif 'range' in mode_inv:
            self._solar_ac_size_lb(model)
            self._solar_ac_size_ub(model)

        mode_ratio = asset.solar.mode.ratio_conf
        if 'fix' in mode_ratio:
            self._solar_ratio_equal_to(model)
        elif 'range' in mode_ratio:
            self._solar_ratio_lb(model)
            self._solar_ratio_ub(model)

        return self

    def _solar_only_prod(self, model):
        def solar_ac_prod_rule(model, t):
            return v(model, Sn.vInvAC)[t] * (1 - p(model, Sn.pInvACLoss)) \
                - v(model, Sn.vLossAC)[t] == \
                v(model, Sn.vStoA)[t]
        model.solar_to_asset = Constraint(s(model, Sn.PERIOD), rule=solar_ac_prod_rule)

    def _solar_at_poi(self, model):
        def solar_at_poi_rule(model, t):
            return v(model, Sn.vStoA)[t] <= p(model, Sn.pPOI)#model.solar_poi
        model.solar_at_poi = Constraint(s(model, Sn.PERIOD), rule=solar_at_poi_rule)

    def _solar_size_less_than_poi(self, model):
        def solar_size_less_than_poi_rule(model):
            return v(model, Sn.vSizeAC) <= p(model, Sn.pPOI)
        model.solar_size_less_than_poi = Constraint(rule=solar_size_less_than_poi_rule)

    def _solar_dc_prod(self, model):
        def solar_dc_prod_rule(model, t):
            return v(model, Sn.vProdDC)[t] == \
                v(model, Sn.vSizeDC) * p(model, Sn.pSOLAR)[t] * (1 - p(model, Sn.pPnlDeg))
        model.solar_dc_prod = Constraint(s(model, Sn.PERIOD), rule=solar_dc_prod_rule)

    def _solar_dc_inv_prod(self, model):
        def solar_dc_inv_prod_rule(model, t):
            return v(model, Sn.vProdDC)[t] * (1 - p(model, Sn.pInvDCLoss)) - v(model, Sn.vLossDC)[t] == \
                v(model, Sn.vInvDC)[t]
        model.solar_dc_inv_prod = Constraint(s(model, Sn.PERIOD), rule=solar_dc_inv_prod_rule)

    def _solar_ac_inv_prod(self, model):
        def solar_ac_inv_prod_rule(model, t):
            return v(model, Sn.vInvDC)[t] * p(model, Sn.pInvEff) == v(model, Sn.vInvAC)[t]
        model.solar_ac_inv_prod = Constraint(s(model, Sn.PERIOD), rule=solar_ac_inv_prod_rule)

    def _solar_ac_inv_limit(self, model):
        def solar_ac_inv_limit_rule(model, t):
            return v(model, Sn.vInvAC)[t] <= v(model, Sn.vSizeAC)
        model.solar_ac_inv_limit = Constraint(s(model, Sn.PERIOD), rule=solar_ac_inv_limit_rule)

    def _solar_ac_inv_size_equal_to(self, model):  ## TODO: que es mas effciente. evaluar el modelo con
        def solar_ac_inv_size_equal_to_rule(model):
            return v(model, Sn.vSizeAC) == p(model, Sn.pSizeFix)
        model.solar_ac_inv_size_equal_to = Constraint(rule=solar_ac_inv_size_equal_to_rule)

    def _solar_ac_size_lb(self, model):
        def solar_ac_size_lb_rule(model):
            return p(model, Sn.pSizeLB) <= v(model, Sn.vSizeAC)
        model.solar_ac_size_lb = Constraint(rule=solar_ac_size_lb_rule)

    def _solar_ac_size_ub(self, model):
        def solar_ac_size_ub_rule(model):
            return v(model, Sn.vSizeAC) <= p(model, Sn.pSizeUB)
        model.solar_ac_size_ub = Constraint(rule=solar_ac_size_ub_rule)

    def _solar_ratio(self, model):
        def solar_ratio_rule(model):
            return v(model, Sn.vSizeDC) >= v(model, Sn.vSizeAC)
        model.solar_ratio = Constraint(rule=solar_ratio_rule)

    def _solar_ratio_equal_to(self, model):
        def solar_ratio_equal_to_rule(model):
            return v(model, Sn.vSizeDC) == v(model, Sn.vSizeAC) * p(model, Sn.pRatFix)
        model.solar_ratio_equal_to = Constraint(rule=solar_ratio_equal_to_rule)

    def _solar_ratio_lb(self, model):
        def solar_ratio_lb_rule(model):
            return v(model, Sn.vSizeDC) >= p(model, Sn.pRatLB) * v(model, Sn.vSizeAC)
        model.solar_ratio_range_lb = Constraint(rule=solar_ratio_lb_rule)

    def _solar_ratio_ub(self, model):
        def solar_ratio_ub_rule(model):
            return v(model, Sn.vSizeDC) <= p(model, Sn.pRatUB) * v(model, Sn.vSizeAC)
        model.solar_ratio_range_ub = Constraint(rule=solar_ratio_ub_rule)
