from pyomo.environ import *

from gr_models.src.asset.parent.wind import WObj, WSet, WVar, WPar, WCon
from gr_models.src.asset.parent.solar import SObj, SSet, SVar, SPar, SCon


class WSset(WSet, SSet):
    def __init__(self, model, config_mode):
        pass


class WSpar(WPar, SPar):
    def __init__(self, model, config_mode):
        self._wind_solar_parameter(model, config_mode)

    def _wind_solar_parameter(self, model, config_mode):
        self._wind_parameter(model, config_mode)
        self._solar_parameter(model, config_mode)


class WSvar(WVar, SVar):
    def __init__(self, model, config_mode):
        self._wind_solar_variable(model, config_mode)

    def _wind_solar_variable(self, model, config_mode):
        self._wind_variable(model, config_mode)
        self._solar_variable(model, config_mode)


class WSobj(WObj, SObj):
    def __init__(self, model, config_mode):
        self._wind_solar_objective(model, config_mode)

    def _wind_solar_objective(self, model, config_mode):
        self._wind_objective(model, config_mode)
        self._solar_objective(model, config_mode)
        self._obj_wind_solar_revenue(model)

    def _obj_wind_solar_revenue(self, model):
        def obj_wind_solar_revenue_rule(model, t):
            return model.SOLAR_GRID_REVENUE - (model.SOLAR_INV_COST + model.SOLAR_PROD_COST) +\
                model.WIND_GRID_REVENUE - (model.WIND_INV_COST + model.WIND_PROD_COST)
        model.objective = Objective(rule=obj_wind_solar_revenue_rule, sense=maximize)


class WScon(WCon, SCon):
    def __init__(self, model, config_mode):
        self._wind_solar_constraint(model, config_mode)

    def _wind_solar_constraint(self, model, config_mode):
        self._wind_constraint(model, config_mode)
        self._solar_constraint(model, config_mode)
