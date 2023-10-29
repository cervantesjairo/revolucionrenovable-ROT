class PanelInv:
    """
    """
    def __init__(self,
                 panel_power_nominal: int,
                 panel_area=None,
                 panel_eff=None,
                 panel_deg=None,
                 inv_eff=None,
                 inv_dc_loss=None,
                 inv_ac_loss=None):
        self.panel_power_nominal = panel_power_nominal
        self.panel_area = panel_area
        self.panel_eff = panel_eff
        self.panel_deg = panel_deg
        self.inv_eff = inv_eff
        self.inv_dc_loss = inv_dc_loss
        self.inv_ac_loss = inv_ac_loss


class SolarCost:

    def __init__(self,
                 capex_panel=None,
                 capex_bos=None,
                 capex_inv=None,
                 opex_var=None,
                 opex_fix=None):
        self.capex_panel = capex_panel
        self.capex_bos = capex_bos
        self.capex_inv = capex_inv
        self.opex_var = opex_var
        self.opex_fix = opex_fix


class SolarMode:

    def __init__(self,
                 inv_conf=None,
                 inv_fix=None,
                 inv_lb_min=None,
                 inv_ub_max=None,
                 ratio_conf=None,
                 ratio_fix=None,
                 ratio_lb_min=None,
                 ratio_ub_max=None,
                 ):
        self.inv_conf = inv_conf
        self.inv_fix = inv_fix
        self.inv_lb_min = inv_lb_min
        self.inv_ub_max = inv_ub_max
        self.ratio_conf = ratio_conf
        self.ratio_fix = ratio_fix
        self.ratio_lb_min = ratio_lb_min
        self.ratio_ub_max = ratio_ub_max
