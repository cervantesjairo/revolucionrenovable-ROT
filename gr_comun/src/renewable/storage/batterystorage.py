from gr_comun.src.renewable.storage.object.elements import Battery, BatteryCost, BatteryMode
# from gr_comun.src.renewable.solar.object.msg import SolarMSG as Smsg


class BES:

    def __init__(self,
                 poi=None,
                 mode: BatteryMode = None,
                 cost: BatteryCost = None,
                 battery: Battery = None,
                 loss=None
                 ):
        self.poi = poi
        self.mode = mode
        self.cost = cost
        self.battery = battery
        self.loss = loss


    def cap_factor(self, ts_solar=None):

        # ts_sp = self.panel_power_curve(ts_solar=ts_solar)
        # ts_sp = ts_sp / self.panel_inv.panel_power_nominal
        #
        # ts_solar[Smsg.SCF] = ts_sp

        return ts_solar

