from pyomo.environ import *

from gr_models.src.renewable.asset.parent.wind import WObj, WSet, WVar, WPar, WCon
from gr_models.src.renewable.asset.parent.solar import SObj, SSet, SVar, SPar, SCon
from gr_models.src.renewable.asset.nomenclature.battery import BatteryNomenclature as Bn
from gr_models.src.renewable.asset.nomenclature.wind import WindNomenclature as Wn
from gr_models.src.renewable.asset.nomenclature.solar import SolarNomenclature as Sn

from gr_models.src.renewable.asset.utils import *

#
# from model.asset.parent.wind import WObj, WSet, WVar, WPar, WCon
# from model.asset.parent.solar import SObj, SSet, SVar, SPar, SCon
# from model.asset.nomenclature.battery import BatteryNomenclature as Bn
# from model.asset.nomenclature.wind import WindNomenclature as Wn
# from model.asset.nomenclature.solar import SolarNomenclature as Sn
#
# from model.asset.utils import *

class WSset(WSet, SSet):
    def __init__(self, model, asset):
        pass


class WSpar(WPar, SPar):
    def __init__(self, model, asset):
        self._wind_solar_parameter(model, asset)

    def _wind_solar_parameter(self, model, asset):
        self._wind_parameter(model, asset)
        self._solar_parameter(model, asset)


class WSvar(WVar, SVar):
    def __init__(self, model, asset):
        self._wind_solar_variable(model, asset)

    def _wind_solar_variable(self, model, asset):
        self._wind_variable(model, asset)
        self._solar_variable(model, asset)


class WSobj(WObj, SObj):
    def __init__(self, model, asset):
        self._wind_solar_objective(model, asset)

    def _wind_solar_objective(self, model, asset):
        self._wind_objective(model, asset)
        self._solar_objective(model, asset)
        self._obj_wind_solar_revenue(model)

    # def _obj_wind_solar_revenue(self, model):
    #     def obj_wind_solar_revenue_rule(model, t):
    #         return model.SOLAR_GRID_REVENUE - (model.SOLAR_INV_COST + model.SOLAR_PROD_COST) +\
    #             model.WIND_GRID_REVENUE - (model.WIND_INV_COST + model.WIND_PROD_COST)
    #     model.objective = Objective(rule=obj_wind_solar_revenue_rule, sense=maximize)

    def _obj_wind_solar_revenue(self, model):
        def obj_wind_solar_revenue_rule(model):
            return v(model, Sn.vRevGrid) - (v(model, Sn.vCostInvst) + v(model, Sn.vCostProd)) +\
                v(model, Wn.vRevGrid) - (v(model, Wn.vCostInvst) + v(model, Wn.vCostProd))
        model.objective = Objective(rule=obj_wind_solar_revenue_rule, sense=maximize)


class WScon(WCon, SCon):
    def __init__(self, model, asset):
        self._wind_solar_constraint(model, asset)

    def _wind_solar_constraint(self, model, asset):
        self._wind_constraint(model, asset)
        self._solar_constraint(model, asset)
