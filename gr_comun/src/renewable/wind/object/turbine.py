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

    def turbine_1(self):
        return self.rated_power, self.v_rated, self.v_cut_in, self.v_cut_out, self.hub_height, self.rotor_diameter
