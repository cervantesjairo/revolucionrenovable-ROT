#
# from model.solve import ModelSolution
# from model.data.parameter import Parametrize
# from model.data.dat_file import DatFile

from gr_models.src.renewable.solve import ModelSolution
from gr_models.src.renewable.data.parameter import Parametrize
from gr_models.src.renewable.data.dat_file import DatFile

import time
import datetime
import pandas as pd


class SolveModel:

    def __init__(self, df_ui_timeseries, df_ui_input):
        self.df_ui_timeseries = df_ui_timeseries
        self.df_ui_input = df_ui_input

    def get_results(self):
        now = datetime.datetime.now()
        print("Start:", now.time())
        start_time = time.time()
        pd.set_option('display.max_rows', None)
        print("getting data...")


        #todo
        # data = Parametrize(df_ui_timeseries=self.df_ui_timeseries, df_ui_input=self.df_ui_input)
        # df_mode, df_par, df_timeseries = data.get_data()

        # print("generating model data ...")
        # model_par = DatFile(df_timeseries=df_timeseries, df_par=df_par, df_other=df_mode)
        # model_par.generate_dat_file()
        data = {
            'solar_inverter_mode': ['fix'],
            'solar_ratio_mode': ['fix'],
            'wind_size_mode': ['fix'],
            'battery_power_mode': ['fix'],
            'battery_duration_mode': ['fix'],
            'battery_cycle_mode': ['unrestricted'],
            'battery_dod_mode': ['unrestricted'],
            'info_asset_mode': ['wind_and_solar_and_battery'],
            'iso_price_dropdown_var': ['TH_NP15_GEN-APND'],
            'iso_demand_dropdown_var': ['None']
        }

        df_mode = pd.DataFrame(data)

        print("setting optimization model   ...")
        model = ModelSolution(asset=df_mode)

        print("solving optimization model   ...")
        table_1, table2, fig1, fig2 = model.solve()

        # print("getting results ...")
        # model.get_file(output_var=x, output_time=y)

        end_time = time.time()
        time_taken = (end_time - start_time) / 60
        print("End Time taken: ", time_taken, " minutes")

        return [table_1, table2, fig1, fig2]
