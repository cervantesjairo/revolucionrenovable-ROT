from gr_comun.src.renewable.solar.object.elements import PanelInv, SolarCost, SolarMode
from gr_comun.src.renewable.solar.object.msg import SolarMSG as Smsg


class SolarPark:

    def __init__(self,
                 poi=None,
                 mode: SolarMode = None,
                 cost: SolarCost = None,
                 panel_inv: PanelInv = None,
                 loss=None,
                 ):
        self.poi = poi
        self.mode = mode
        self.cost = cost
        self.loss = loss
        self.panel_inv = panel_inv

    def cap_factor(self, ts_solar=None):

        ts_sp = self.panel_power_curve(ts_solar=ts_solar)
        ts_sp = ts_sp / self.panel_inv.panel_power_nominal

        ts_solar[Smsg.SCF] = ts_sp

        return ts_solar

    def panel_power_curve(self, ts_solar=None):
        panel = self.panel_inv

        panel_eff_area = panel.panel_area * panel.panel_eff / 100
        # panel_power_curve = ts_solar[Smsg.GHI] * panel_eff_area
        panel_power_curve = ts_solar[Smsg.GHI] * panel_eff_area * ((100 - panel.panel_deg) / 100)

        return panel_power_curve

    def panels_per_kw(self):
        num_panel = 1e3 / self.panel_inv.panel_power_nominal
        return num_panel

    def panels_per_mw(self):
        num_panel = 1e6 / self.panel_inv.panel_power_nominal
        return num_panel
