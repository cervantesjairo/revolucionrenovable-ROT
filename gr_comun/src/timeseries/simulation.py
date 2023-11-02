from datetime import datetime


class Simulation:
    def __init__(self,
                 ts_from: datetime = None,
                 ts_to: datetime = None,
                 lat=None,
                 lon=None,
                 tz: str=None):
        self.ts_from = ts_from
        self.ts_to = ts_to
        self.lat = lat
        self.lon = lon
        self.tz = tz
