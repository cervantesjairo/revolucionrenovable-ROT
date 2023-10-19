from muiscaenergy_connector.src.caiso.database.demand.query import CAISO_DEMANDS
import time
from datetime import datetime

now = datetime.now()
print("start time:", now.time())
start_time = time.time()


start = datetime(2022, 1, 1)
end = datetime(2022, 1, 25)
database = CAISO_DEMANDS(
    ts_from=start,
    ts_to=end,
    area='CA ISO-TAC'
)
###################################CASE1
df_dem_actual = database.get_demand(market='ACTUAL',
                                    execution_type=None)

df_dem_da = database.get_demand(market='DAM',
                                execution_type=None)

df_dem_2da = database.get_demand(market='2DA',
                                 execution_type=None)

df_dem_7da = database.get_demand(market='7DA',
                                 execution_type=None)

df_dem_rt_5m = database.get_demand(market='RTM',
                                   execution_type='RTD')

df_dem_rt_15m = database.get_demand(market='RTM',
                                    execution_type='RTPD')

df_peak = database.get_demand_peak()

end_time = time.time()
time_taken = (end_time - start_time)/60
print("Time taken: ", time_taken, " min")

x=1