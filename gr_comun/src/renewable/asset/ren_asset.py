from gr_comun.src.renewable.wind.windfarm import WindFarm
from gr_comun.src.renewable.solar.solarpark import SolarPark
from gr_comun.src.renewable.storage.battery import BES
# from gr_comun.src.renewable.solar.object.msg import SolarMSG as Smsg


class RenewableAsset:

    def __init__(self,
                 name: str = None,
                 config: str = None,
                 poi=None,
                 loss=None,
                 mode=None,
                 wind: WindFarm = None,
                 solar: SolarPark = None,
                 storage: BES = None,
                 ):
        self.name = name
        self.config = config
        self.poi = poi
        self.loss = loss
        self.mode = mode
        self.wind = wind
        self.solar = solar
        self.storage = storage
