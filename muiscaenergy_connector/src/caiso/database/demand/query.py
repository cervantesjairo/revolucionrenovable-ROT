from datetime import timedelta
import requests
import zipfile
import io
import pandas as pd
import time
from muiscaenergy_comun.src.timeseries.base import get_timeseries
from muiscaenergy_comun.src.messages.base import TimeSeriesMessage as TSm
from datetime import datetime
import concurrent.futures


class CAISO_DEMANDS:
    """
    :param name:
    :returns df:
    """
    MAX_FETCH = 28  # days

    def __init__(self,
                 ts_from: datetime,
                 ts_to: datetime,
                 area: str
                 ):
        self.ts_from = ts_from
        self.ts_to = ts_to
        self.area = area

###################  DEMAND MW-h  ##############
    def get_demand(self, market=None, execution_type=None) -> TSm():
        """

        :param market: this parameter supports 'ACTUAL', 'DAM', '2DA', '7DA', 'RTM'
        :param execution_type: this parameter is only for RTM market. two options: RTD (5min) or RTPD (15min)
        :return:
        """

        if execution_type == 'RTD':
            frequency = '5T'
        elif execution_type == 'RTPD':
            frequency = '15T'
        else:
            frequency = 'H'

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

                market_names = ['ACTUAL', 'DAM', '2DA', '7DA', 'RTM']
                if market in market_names:
                    if market == 'RTM':
                        execution_type = execution_type
                    else:
                        execution_type = None

                    url = self.get_demand_url(query_name='SLD_FCST',
                                              mkt_id=market,
                                              execution_type=execution_type,
                                              date_start=url_start,
                                              date_end=url_end
                                              )

                    futures.append(executor.submit(self.fetch_demand_data, url))

            for future in concurrent.futures.as_completed(futures):
                df = future.result()
                total_df = pd.concat([total_df, df], ignore_index=True)

        total_df = total_df.drop_duplicates(subset=['INTERVALSTARTTIME_GMT', 'TAC_AREA_NAME'], keep='first')

        col_dt = ['INTERVALSTARTTIME_GMT', 'INTERVALENDTIME_GMT']
        total_df[col_dt] = total_df[col_dt].apply(pd.to_datetime)
        out_ts = df_ts.merge(total_df, how='inner', left_on=TSm.DT_UTC, right_on='INTERVALSTARTTIME_GMT')

        out = self.post_process_demand(df=out_ts, market=market)

        return out

    def get_demand_url(self, query_name=None, mkt_id=None, execution_type=None, date_start=None, date_end=None):
        if execution_type:
            url_demand = ('http://oasis.caiso.com/oasisapi/SingleZip?'
                          'queryname={query}'
                          '&'
                          'market_run_id={market}'
                          '&'
                          'execution_type={execution_type}'
                          '&'
                          'startdatetime={start}T07:00-0000'
                          '&'
                          'enddatetime={end}T07:00-0000'
                          '&'
                          'resultformat=6'
                          '&'
                          'version=1').format(
                query=query_name,
                market=mkt_id,
                execution_type=execution_type,
                start=date_start,
                end=date_end,
            )

        if not execution_type:
            url_demand = ('http://oasis.caiso.com/oasisapi/SingleZip?'
                          'queryname={query}'
                          '&'
                          'market_run_id={market}'
                          '&'
                          'startdatetime={start}T07:00-0000'
                          '&'
                          'enddatetime={end}T07:00-0000'
                          '&'
                          'resultformat=6'
                          '&'
                          'version=1').format(
                query=query_name,
                market=mkt_id,
                start=date_start,
                end=date_end,
            )

        return url_demand

    def post_process_demand(self, df=None, market=None):

        var_name = 'load'
        df.rename(columns={'MW': var_name}, inplace=True)

        var = [self.area]
        filtered_df = df[df['TAC_AREA_NAME'].isin(var)]

        out_col = [TSm.DT_UTC, TSm.DT_FROM, TSm.DT_TO, var_name]
        df = filtered_df[out_col]

        return df

###################  PEAK  ##############
    def get_demand_peak(self):

        frequency = 'H'

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

                url = self.get_demand_peak_url(query_name='SLD_FCST_PEAK',
                                               date_start=url_start,
                                               date_end=url_end
                                               )

                futures.append(executor.submit(self.fetch_demand_data, url))

            for future in concurrent.futures.as_completed(futures):
                df = future.result()
                total_df = pd.concat([total_df, df], ignore_index=True)

        total_df = total_df.drop_duplicates(subset=['INTERVALSTARTTIME_GMT', 'TAC_AREA_NAME'], keep='first')

        col_dt = ['INTERVALSTARTTIME_GMT', 'INTERVALENDTIME_GMT']
        total_df[col_dt] = total_df[col_dt].apply(pd.to_datetime)
        out_ts = df_ts.merge(total_df, how='inner', left_on=TSm.DT_UTC, right_on='INTERVALSTARTTIME_GMT')

        out = self.post_process_demand_peak(df=out_ts)

        return out

    def get_demand_peak_url(self, query_name=None, date_start=None, date_end=None):
        url_demand = ('http://oasis.caiso.com/oasisapi/SingleZip?'
                      'queryname={query}'
                      '&'
                      'startdatetime={start}T07:00-0000'
                      '&'
                      'enddatetime={end}T07:00-0000'
                      '&'
                      'resultformat=6'
                      '&'
                      'version=1').format(
            query=query_name,
            start=date_start,
            end=date_end,
        )

        return url_demand

    def post_process_demand_peak(self, df=None, market=None):

        var_name = 'peak_load'
        df.rename(columns={'LOAD_MW': var_name}, inplace=True)

        var = [self.area]
        filtered_df = df[df['TAC_AREA_NAME'].isin(var)]

        out_col = [TSm.DT_UTC, TSm.DT_FROM, TSm.DT_TO, var_name]
        df = filtered_df[out_col]

        return df


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
