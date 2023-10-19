from revolucionrenovable_ROT.src.layers.renewable.solar.mode.solar_inv_config import SolarInvConf
from revolucionrenovable_ROT.src.layers.renewable.solar.mode.solar_ratio_config import SolarRatioConf
from revolucionrenovable_ROT.src.layers.renewable.battery.mode.battery_power_config import BatteryPowerConf
from revolucionrenovable_ROT.src.layers.renewable.battery.mode.battery_cap_config import BatteryCapConf
from revolucionrenovable_ROT.src.layers.renewable.battery.mode.battery_cycle_config import BatteryCycleConf
from revolucionrenovable_ROT.src.layers.renewable.battery.mode.battery_dod_config import BatteryDoDConf
from revolucionrenovable_ROT.src.layers.renewable.wind.mode.wind_config import WindConf
from revolucionrenovable_ROT.src.layers.timeseries.mode.latlon import LatLon
from revolucionrenovable_ROT.src.web.tab_result.run import Run


# Definir funciones para configurar los callbacks
# TODO separarlas o crear un archivo que ve haga solar ocn todos los set_up_callbackas(app)
def setup_callbacks(app):
    Run().setup_callbacks(app)
    WindConf().setup_callbacks(app)
    LatLon().setup_callbacks(app)
    SolarInvConf().setup_callbacks(app)
    SolarRatioConf().setup_callbacks(app)
    BatteryPowerConf().setup_callbacks(app)
    BatteryCapConf().setup_callbacks(app)
    BatteryCycleConf().setup_callbacks(app)
    BatteryDoDConf().setup_callbacks(app)
