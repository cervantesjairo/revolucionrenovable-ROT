from muiscaenergy_connector.src.caiso.database.price.query import CAISO_PRICE
from muiscaenergy_comun.src.timeseries.base import get_timeseries
from muiscaenergy_comun.src.messages.base import TimeSeriesMessage as TSm
from datetime import datetime
import time
import pandas as pd

database = CAISO_PRICE(ts_from=datetime(2022, 1, 1),
                       ts_to=datetime(2022, 2, 11))
###################################CASE1
now = datetime.now()
print("start time:", now.time())
start_time = time.time()
df = database.get_lmp(market='DAM',
                      node='TH_NP15_GEN-APND',
                      )

end_time = time.time()
time_taken = (end_time - start_time)/60
print("Time taken: ", time_taken, " min")

x=1