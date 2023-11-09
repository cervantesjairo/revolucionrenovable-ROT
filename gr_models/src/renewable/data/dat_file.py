# from model.model_data import DataModel
import pandas as pd
import numpy as np


class DatFile:
    def __init__(self, df_timeseries, df_par, df_other):
        self.df_timeseries = df_timeseries
        self.df_par = df_par
        self.df_mode = df_other

    def generate_dat_file(self):

        _asset = self.df_mode['info_asset_mode'][0]
        df_par = round(self.df_par, 4)
        df_timeseries = round(self.df_timeseries, 4)
        df_timeseries = df_timeseries.reset_index()                   ### TODO: Thre should be one for each solar
        model_file = r'C:/Users/jhcer/Documents/3. Projects/web_test/model/data/model_data.dat'
        # C:/Users/jhcer/Documents/3. Projects/web_test/model/data/model_data.dat
        with open(model_file, 'w') as file:
            for i in df_par.columns:
                file.write(f'param {i} :=\n')
                file.write(f'{df_par[i][0]}\n')
                file.write(';\n')
                file.write('\n')
            file.write('\n')

            file.write(f'set PERIOD :=\n')
            for i in df_timeseries['index']:
                file.write(f'{i} \n')
            file.write(';\n')
            file.write('\n')

            file.write(f'param lmp :=\n')
            for j in df_timeseries['index']:
                file.write(f'{df_timeseries["index"][j]} {df_timeseries["lmp"][j]}\n')
            file.write(';\n')
            file.write('\n')

            if 'solar' in _asset:
                file.write(f'param solar :=\n')
                for j in df_timeseries['index']:
                    file.write(f'{df_timeseries["index"][j]} {df_timeseries["solar"][j]}\n')
                file.write(';\n')
                file.write('\n')

            if 'wind' in _asset:
                file.write(f'param wind :=\n')
                for j in df_timeseries['index']:
                    file.write(f'{df_timeseries["index"][j]} {df_timeseries["wind"][j]}\n')
                file.write(';\n')
                file.write('\n')

        with open(model_file, 'r') as file:
            content = file.read()

        return content
