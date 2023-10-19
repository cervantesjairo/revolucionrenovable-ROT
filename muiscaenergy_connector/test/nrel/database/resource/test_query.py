from muiscaenergy_connector.src.nrel.database.resource.query import NREL_RESOURCE
from datetime import datetime
import time


###################################CASE1
now = datetime.now()
print("start time:", now.time())
start_time = time.time()
lat = 34
lon = -120
start = datetime(2022, 1, 1)
end = datetime(2022, 12, 31)
var = 'ghi'     # 'ghi,wind_speed'
resource = NREL_RESOURCE(ts_from=start,
                         ts_to=end
                         )

df = resource.get_resource(var=var, lat=lat, lon=lon)
end_time = time.time()
time_taken = (end_time - start_time)/60
print("Time taken: ", time_taken, " min")

