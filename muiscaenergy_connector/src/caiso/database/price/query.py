from muiscaenergy_comun.src.timeseries.base import get_timeseries
from muiscaenergy_comun.src.messages.base import TimeSeriesMessage as TSm
from datetime import datetime, timedelta
import requests
import zipfile
import io
import pandas as pd
import time
import concurrent.futures

class CAISO_PRICES:
    """
    :param name:
    :returns df:
    
    #############################
    # https://www.caiso.com/Documents/OASIS-Frequently-Asked-Questions.pdf
    # https://www.caiso.com/Documents/OASIS-InterfaceSpecification_v5_1_1Clean_Fall2017Release.pdf
    # https://github.com/caheredia/caiso_connector/blob/master/tests/test_connector.py
    # https://github.com/ambrishambekar/CAISO-ADS/blob/master/ADS_LMP.py
    # https://github.com/cwBerkeley/code/blob/master/CAISO-oasisAPI-operations.R
    # https://github.com/caheredia/caiso_connector/blob/master/tests/test_connector.py
    ###############################
    """
    MAX_FETCH = 28  # days

    def __init__(self,
                 ts_from: datetime,
                 ts_to: datetime,
                 ):
        self.ts_from = ts_from
        self.ts_to = ts_to

    def get_lmp(self, market=None, node=None):

        frequency_map = {
            'DAM': 'H',
            'RTPD': '15T',
            'RTM': '5T'
        }
        frequency = frequency_map.get(market, 'H')
        timeseries = get_timeseries(ts_from=self.ts_from,
                                    ts_to=self.ts_to,
                                    freq=frequency,
                                    tz='America/Los_Angeles')
        df_ts = timeseries.df

        first_row = df_ts[TSm.DT_UTC].iloc[0]
        last_row = df_ts[TSm.DT_UTC].iloc[-1]
        total_days = (last_row - first_row).days + 2
        n_parallel = round(total_days / self.MAX_FETCH) + 1
        periods = range(0, total_days, self.MAX_FETCH)

        total_df = pd.DataFrame()
        with concurrent.futures.ThreadPoolExecutor(max_workers=n_parallel) as executor:
            futures = []
            for start_day in periods:
                time.sleep(6)
                if start_day == 0:
                    ref_start = df_ts[TSm.DT_UTC].iloc[start_day] - timedelta(days=1)
                else:
                    ref_start = df_ts[TSm.DT_UTC].iloc[(start_day * 24) - 24]
                ref_end = ref_start + timedelta(days=self.MAX_FETCH)
                url_start = ref_start.strftime('%Y%m%d')
                url_end = ref_end.strftime('%Y%m%d')

                query_names = {
                    'DAM': 'PRC_LMP',
                    'RTPD': 'PRC_RTPD_LMP',
                    'RTM': 'PRC_INTVL_LMP'
                }
                if market in query_names:
                    query_name = query_names[market]
                    url = self.get_lmp_url(query_name=query_name,
                                           mkt_id=market, node=node,
                                           date_start=url_start,
                                           date_end=url_end)

                    futures.append(executor.submit(self.fetch_demand_data, url))

            for future in concurrent.futures.as_completed(futures):
                df = future.result()
                total_df = pd.concat([total_df, df], ignore_index=True)

        total_df = total_df.drop_duplicates(subset=['INTERVALSTARTTIME_GMT', 'NODE', 'LMP_TYPE'], keep='first')

        col = ['INTERVALSTARTTIME_GMT', 'INTERVALENDTIME_GMT']
        total_df[col] = total_df[col].apply(pd.to_datetime)
        out_ts = df_ts.merge(total_df, how='inner', left_on=TSm.DT_UTC, right_on='INTERVALSTARTTIME_GMT')

        out = self.post_process_lmp(df=out_ts, market=market)
        return out

    def post_process_lmp(self, df=None, market=None):

        column_mapping = {
            'DAM': {'MW': 'price'},
            'RTPD': {'PRC': 'price'},
            'RTM': {'MW': 'price'}
        }

        if market in column_mapping:
            df.rename(columns=column_mapping[market], inplace=True)

        var_name = 'LMP'
        var = [var_name]  # ['LMP', 'MCC', 'MCE', 'MCL', 'MGHG']
        filtered_df = df[df['LMP_TYPE'].isin(var)]

        out_col = [TSm.DT_UTC, TSm.DT_FROM, TSm.DT_TO, var_name]
        df = filtered_df[out_col]

        return df

    def get_lmp_url(self, query_name=None, mkt_id=None, node=None, date_start=None, date_end=None):
        return ('http://oasis.caiso.com/oasisapi/SingleZip?'
                'queryname={query}'
                '&'
                'market_run_id={market}'
                '&'
                'node={node}'
                '&'
                'startdatetime={start}T07:00-0000'
                '&'
                'enddatetime={end}T07:00-0000'
                '&'
                'resultformat=6'
                '&'
                'version=1'
                ).format(
            query=query_name,
            market=mkt_id,
            node=node,
            start=date_start,
            end=date_end,
        )

    ############# FETCH #############
    def fetch_demand_data(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Verificar si la respuesta HTTP es exitosa
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                csv_filename = zip_ref.namelist()[0]
                with zip_ref.open(csv_filename) as csv_file:
                    df = pd.read_csv(csv_file)
            return df
        except requests.exceptions.RequestException as e:
            print(f"Error al descargar datos: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        return pd.DataFrame()
