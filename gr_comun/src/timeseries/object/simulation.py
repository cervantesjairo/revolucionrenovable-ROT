from datetime import datetime


class Simulation:
    def __init__(self,
                 ts_from: datetime,
                 ts_to: datetime,
                 lat: float = None,
                 lon: float = None,
                 tz: str = None,
                 freq: str = None):
        self.ts_from = ts_from
        self.ts_to = ts_to
        self.lat = lat
        self.lon = lon
        self.tz = tz
        self.freq = freq
