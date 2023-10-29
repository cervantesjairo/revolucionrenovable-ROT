class WindTurbine:
    """

    """
    def __init__(self,
                 rated_power=None,
                 v_rated=None,
                 v_cut_in=None,
                 v_cut_out=None,
                 hub_height=None,
                 rotor_diameter=None):
        self.rated_power = rated_power
        self.v_rated = v_rated
        self.v_cut_in = v_cut_in
        self.v_cut_out = v_cut_out
        self.hub_height = hub_height
        self.rotor_diameter = rotor_diameter


class WindCost:
    """
    """
    def __init__(self,
                 capex_wind=None,
                 capex_inter=None,
                 opex_fix=None,
                 opex_variable=None,
                 ):
        self.capex_wind = capex_wind
        self.capex_inter = capex_inter
        self.opex_fix = opex_fix
        self.opex_variable = opex_variable


class WindMode:

    def __init__(self,
                 size_conf: str = None,
                 size_fix=None,
                 size_lb_min=None,
                 size_ub_max=None,
                 ):
        self.size_conf = size_conf
        self.size_fix = size_fix
        self.size_lb_min = size_lb_min
        self.size_ub_max = size_ub_max
