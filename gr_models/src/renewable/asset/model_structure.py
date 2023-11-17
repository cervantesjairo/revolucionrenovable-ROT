from gr_models.src.renewable.asset.parent.wind import WObj, WSet, WVar, WPar, WCon
from gr_models.src.renewable.asset.parent.solar import SObj, SSet, SVar, SPar, SCon
from gr_models.src.renewable.asset.parent.battery import BObj, BSet, BVar, BPar, BCon
from gr_models.src.renewable.asset.child.wind_and_solar import WSobj, WSset, WSvar, WSpar, WScon
from gr_models.src.renewable.asset.child.wind_and_battery import WBobj, WBset, WBvar, WBpar, WBcon
from gr_models.src.renewable.asset.child.solar_and_battery import SBobj, SBset, SBvar, SBpar, SBcon
from gr_models.src.renewable.asset.child.wind_and_solar_and_battery import WSBobj, WSBset, WSBvar, WSBpar, WSBcon


class Sets:
    def __init__(self, model, asset):
        # asset.config = asset
        if asset.config == 'wind':
            WSet(model, asset)

        if asset.config == 'solar':
            SSet(model, asset)

        if asset.config == 'battery':
            BSet(model, asset)

        if asset.config == 'wind_solar':
            WSset(model, asset)

        if asset.config == 'wind_battery':
            WBset(model, asset)

        if asset.config == 'solar_battery':
            SBset(model, asset)

        if asset.config == 'wind_solar_battery':
            WSBset(model, asset)


class Pars:
    def __init__(self, model, asset):
        # asset.config = asset#['infoasset.config_mode'][0]
        if asset.config == 'wind':
            WPar(model, asset)

        if asset.config == 'solar':
            SPar(model, asset)

        if asset.config == 'battery':
            BPar(model, asset)

        if asset.config == 'wind_solar':
            WSpar(model, asset)

        if asset.config == 'wind_battery':
            WBpar(model, asset)

        if asset.config == 'solar_battery':
            SBpar(model, asset)

        if asset.config == 'wind_solar_battery':
            WSBpar(model, asset)


class Vars:
    def __init__(self, model, asset):
        # asset.config = asset
        if asset.config == 'wind':
            WVar(model, asset)

        if asset.config == 'solar':
            SVar(model, asset)

        if asset.config == 'battery':
            BVar(model, asset)

        if asset.config == 'wind_solar':
            WSvar(model, asset)

        if asset.config == 'wind_battery':
            WBvar(model, asset)

        if asset.config == 'solar_battery':
            SBvar(model, asset)

        if asset.config == 'wind_solar_battery':
            WSBvar(model, asset)


class Objs:
    def __init__(self, model, asset):
        # asset.config = asset
        if asset.config == 'wind':
            WObj(model, asset)

        if asset.config == 'solar':
            SObj(model, asset)

        if asset.config == 'battery':
            BObj(model, asset)

        if asset.config == 'wind_solar':
            WSobj(model, asset)

        if asset.config == 'wind_battery':
            WBobj(model, asset)

        if asset.config == 'solar_battery':
            SBobj(model, asset)

        if asset.config == 'wind_solar_battery':
            WSBobj(model, asset)


class Cons:
    def __init__(self, model, asset):
        # asset.config = asset
        if asset.config == 'wind':
            WCon(model, asset)

        if asset.config == 'solar':
            SCon(model, asset)

        if asset.config == 'battery':
            BCon(model, asset)

        if asset.config == 'wind_solar':
            WScon(model, asset)

        if asset.config == 'wind_battery':
            WBcon(model, asset)

        if asset.config == 'solar_battery':
            SBcon(model, asset)

        if asset.config == 'wind_solar_battery':
            WSBcon(model, asset)
