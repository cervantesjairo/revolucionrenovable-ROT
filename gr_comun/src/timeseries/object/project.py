
from datetime import datetime
from gr_comun.src.timeseries.object.simulation import Simulation
from gr_comun.src.eng_economy.cashflow import CashFlowMeasures


class ProjectRenewable:
    def __init__(self,
                 name: str = 'project',
                 config: str = None,
                 simulation: Simulation = None,
                 financial: CashFlowMeasures = None,
                 ):
        self.name = name
        self.config = config
        self.simulation = simulation
        self.financial = financial
