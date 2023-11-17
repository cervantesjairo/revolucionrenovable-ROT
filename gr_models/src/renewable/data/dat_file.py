from gr_comun.src.messages.base import TimeSeriesMessage as TSm
from gr_comun.src.timeseries.ts_rot import TimeSeriesROT
from gr_comun.src.timeseries.is_rot import InvariantSeries


class DatFile:
    def __init__(self,
                 time_series: TimeSeriesROT = None,
                 constant_values: InvariantSeries = None,):
        self.time_series = time_series
        self.constant_values = constant_values

    def generate_dat_file(self):
        cv = round(self.constant_values, 4)
        ts = round(self.time_series, 4)
        col_drop = [TSm.DT_UTC, TSm.DT_FROM, TSm.DT_TO]
        ts = ts.drop(columns=col_drop)
        ts = ts.reset_index()

        model_file = r'C:/Users/jhcer/Documents/3. Projects/revolucionrenovable-ROT/gr_models/src/renewable/data/model_data.dat'

        with open(model_file, 'w') as file:
            for i in cv.columns:
                file.write(f"param {i} :=\n")
                file.write(f"{cv[i][0]}\n")
                file.write(';\n')
                file.write('\n')
            file.write('\n')

            file.write(f'set PERIOD :=\n')
            for i in ts['index']:
                file.write(f'{i} \n')
            file.write(';\n')
            file.write('\n')

            for i in ts.columns.drop('index'):
                file.write(f'param {i} :=\n')
                for j in ts['index']:
                    file.write(f'{ts["index"][j]} {ts[i][j]}\n')
                file.write(';\n')
                file.write('\n')

        with open(model_file, 'r') as file:
            content = file.read()

        return content
