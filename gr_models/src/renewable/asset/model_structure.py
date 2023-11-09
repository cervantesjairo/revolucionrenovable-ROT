from gr_models.src.renewable.asset.parent.wind import WObj, WSet, WVar, WPar, WCon
from gr_models.src.renewable.asset.parent.solar import SObj, SSet, SVar, SPar, SCon
from gr_models.src.renewable.asset.parent.battery import BObj, BSet, BVar, BPar, BCon
from gr_models.src.renewable.asset.child.wind_and_solar import WSobj, WSset, WSvar, WSpar, WScon
from gr_models.src.renewable.asset.child.wind_and_battery import WBobj, WBset, WBvar, WBpar, WBcon
from gr_models.src.renewable.asset.child.solar_and_battery import SBobj, SBset, SBvar, SBpar, SBcon
from gr_models.src.renewable.asset.child.wind_and_solar_and_battery import WSBobj, WSBset, WSBvar, WSBpar, WSBcon


class Sets:
    def __init__(self, model, config_mode):
        _asset = config_mode
        if _asset == 'wind':
            WSet(model, config_mode)

        if _asset == 'solar':
            SSet(model, config_mode)

        if _asset == 'battery':
            BSet(model, config_mode)

        if _asset == 'wind_and_solar':
            WSset(model, config_mode)

        if _asset == 'wind_and_battery':
            WBset(model, config_mode)

        if _asset == 'solar_and_battery':
            SBset(model, config_mode)

        if _asset == 'wind_and_solar_and_battery':
            WSBset(model, config_mode)


class Pars:
    def __init__(self, model, config_mode):
        _asset = config_mode#['info_asset_mode'][0]
        if _asset == 'wind':
            WPar(model, config_mode)

        if _asset == 'solar':
            SPar(model, config_mode)

        if _asset == 'battery':
            BPar(model, config_mode)

        if _asset == 'wind_and_solar':
            WSpar(model, config_mode)

        if _asset == 'wind_and_battery':
            WBpar(model, config_mode)

        if _asset == 'solar_and_battery':
            SBpar(model, config_mode)

        if _asset == 'wind_and_solar_and_battery':
            WSBpar(model, config_mode)


class Vars:
    def __init__(self, model, config_mode):
        _asset = config_mode
        if _asset == 'wind':
            WVar(model, config_mode)

        if _asset == 'solar':
            SVar(model, config_mode)

        if _asset == 'battery':
            BVar(model, config_mode)

        if _asset == 'wind_and_solar':
            WSvar(model, config_mode)

        if _asset == 'wind_and_battery':
            WBvar(model, config_mode)

        if _asset == 'solar_and_battery':
            SBvar(model, config_mode)

        if _asset == 'wind_and_solar_and_battery':
            WSBvar(model, config_mode)


class Objs:
    def __init__(self, model, config_mode):
        _asset = config_mode
        if _asset == 'wind':
            WObj(model, config_mode)

        if _asset == 'solar':
            SObj(model, config_mode)

        if _asset == 'battery':
            BObj(model, config_mode)

        if _asset == 'wind_and_solar':
            WSobj(model, config_mode)

        if _asset == 'wind_and_battery':
            WBobj(model, config_mode)

        if _asset == 'solar_and_battery':
            SBobj(model, config_mode)

        if _asset == 'wind_and_solar_and_battery':
            WSBobj(model, config_mode)


class Cons:
    def __init__(self, model, config_mode):
        _asset = config_mode
        if _asset == 'wind':
            WCon(model, config_mode)

        if _asset == 'solar':
            SCon(model, config_mode)

        if _asset == 'battery':
            BCon(model, config_mode)

        if _asset == 'wind_and_solar':
            WScon(model, config_mode)

        if _asset == 'wind_and_battery':
            WBcon(model, config_mode)

        if _asset == 'solar_and_battery':
            SBcon(model, config_mode)

        if _asset == 'wind_and_solar_and_battery':
            WSBcon(model, config_mode)
