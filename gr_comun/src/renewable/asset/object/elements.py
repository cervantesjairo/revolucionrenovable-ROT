class Asset:
    """

    """
    def __init__(self,
                 rte=None,
                 ):
        self.rte = rte


class AssetCost:
    def __init__(self,
                 capex_power=None,
                 capex_capacity=None,
                 opex_var=None,
                 opex_fix=None):
        self.capex_power = capex_power
        self.capex_capacity = capex_capacity
        self.opex_var = opex_var
        self.opex_fix = opex_fix


class AssetMode:

    def __init__(self,
                 power_conf=None,
                 power_fix=None,
                 power_lb_min=None,
                 power_ub_max=None,
                 dur_conf=None,
                 dur_fix=None,
                 dur_lb_min=None,
                 dur_ub_max=None,
                 dod_conf=None,
                 dod_fix=None,
                 dod_lb_min=None,
                 dod_ub_max=None,
                 cycle_conf=None,
                 cycle_fix=None,
                 cycle_lb_min=None,
                 cycle_ub_max=None,
                 ):
        self.power_conf = power_conf
        self.power_fix = power_fix
        self.power_lb_min = power_lb_min
        self.power_ub_max = power_ub_max
        self.dur_conf = dur_conf
        self.dur_fix = dur_fix
        self.dur_lb_min = dur_lb_min
        self.dur_ub_max = dur_ub_max
        self.dod_conf = dod_conf
        self.dod_fix = dod_fix
        self.dod_lb_min = dod_lb_min
        self.dod_ub_max = dod_ub_max
        self.cycle_conf = cycle_conf
        self.cycle_fix = cycle_fix
        self.cycle_lb_min = cycle_lb_min
        self.cycle_ub_max = cycle_ub_max
