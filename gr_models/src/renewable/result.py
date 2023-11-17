import pandas as pd
from pyomo.environ import *
import plotly.graph_objs as go
import plotly.subplots as sp

from gr_models.src.renewable.solve import ModelSolution
from gr_comun.src.renewable.asset.ren_asset import RenewableAsset
from gr_comun.src.timeseries.ts_rot import TimeSeriesROT


from gr_models.src.renewable.asset.nomenclature.wind import WindNomenclature as Wn
from gr_models.src.renewable.asset.nomenclature.solar import SolarNomenclature as Sn
from gr_models.src.renewable.asset.nomenclature.battery import BatteryNomenclature as Bn


class ResultOptimization:

    def __init__(self, 
                 instance: ModelSolution,
                 asset: RenewableAsset,
                 timeseries: TimeSeriesROT = None):
        self.instance = instance
        self.asset = asset
        self.timeseries = timeseries
        
    # def get_result_df(self):
        # TODO : need to review teh modes options in the models
        # TODO : need to review the parallel for teh timeseries

    def get_result_df(self):
        instance = self.instance
        asset = self.asset.config
        ts = self.timeseries

        ts['LMP'] = [value(instance.lmp[j]) for j in instance.PERIOD]

        output_var = pd.DataFrame()
        MILLON = 1e6
        output_var['OBJECTIVE_VALUE'] = round(value(instance.objective()), 2)

        df_ts = pd.DataFrame()
        df_ts['LMP'] = [value(instance.lmp[j]) for j in instance.PERIOD]
        df_ts_dispatch = df_ts.copy()
        df_ts_battery = df_ts.copy()
        ts_bat = None

        df_wind = pd.DataFrame()
        df_wind_eco = pd.DataFrame()
        df_solar = pd.DataFrame()
        df_solar_eco = pd.DataFrame()
        df_battery = pd.DataFrame()
        df_battery_eco = pd.DataFrame()
        if 'wind' in asset:
            ### Economic Analysis
            COST_INV = round(float([value(instance.WIND_INV_COST)][0]) / MILLON, 2)
            COST_PROD = round(float([value(instance.WIND_PROD_COST)][0]) / MILLON, 2)
            REVENUE = round(float([value(instance.WIND_GRID_REVENUE)][0]) / MILLON, 2)
            PROFIT = round(REVENUE - (COST_INV + COST_PROD), 2)
            ### Technical Analysis
            SIZE = float(round([value(instance.WIND_SIZE)][0], 0))
            ### Time Series
            df_ts['WtoA'] = [value(instance.WtoA[j]) for j in instance.PERIOD]
            df_ts['WLoss'] = [value(instance.WLoss[j]) for j in instance.PERIOD]
            df_ts['WIND'] = df_ts['WtoA'] + df_ts['WLoss']
            DELIVERED = round(float(sum(df_ts['WtoA'])), 1)
            LOSS = round(float(sum(df_ts['WLoss'])))
            NCF = round(float(sum(df_ts['WtoA'])) / (len(df_ts['WtoA']) * SIZE), 4)

            #### out information
            df_ts_dispatch['Wind'] = df_ts['WtoA']

            if 'battery' in asset:
                df_ts['WtoB'] = [(-1) * value(instance.WtoB[j]) for j in instance.PERIOD]
                df_ts['Resource Wind'] = df_ts['WtoA'] - df_ts['WtoB']
                STORED = round(float(sum(df_ts['WtoB'])))
                W_STORED = STORED

                #### out information
                df_ts_dispatch['Resource Wind'] = df_ts['Resource Wind']
                df_ts_battery['ChargeWind'] = df_ts['WtoB']

            else:
                W_STORED = None

            table1_wind = \
                {
                    'Description': ['Size [kW]',
                                    'Energy Delivered [kWh]',
                                    'Energy Stored [kWh]',
                                    'Energy Loss [kWh]',
                                    'Capacity Factor [p.u.]'],
                    'Wind': [SIZE,
                             DELIVERED,
                             W_STORED,
                             LOSS,
                             NCF],
                }

            table_eco_wind = \
                {
                    'Description': ['Profit [M$]',
                                    'Revenue [M$]',
                                    'Cost [M$]',
                                    'Cost Inv [M$]',
                                    'Cost Prod [M$]',
                                    'Cost Energy [$/kWh]',
                                    ],
                    'Wind': [PROFIT,
                             REVENUE,
                             "----",
                             COST_INV,
                             COST_PROD,
                             COST_PROD / DELIVERED]

                }

            df_wind = pd.DataFrame(table1_wind).fillna('')
            df_wind_eco = pd.DataFrame(table_eco_wind).fillna('')

        if 'solar' in asset:
            COST_INV = round(float([value(instance.SOLAR_INV_COST)][0]) / MILLON, 2)
            COST_PROD = round(float([value(instance.SOLAR_PROD_COST)][0]) / MILLON, 2)
            REVENUE = round(float([value(instance.SOLAR_GRID_REVENUE)][0]) / MILLON, 2)
            PROFIT = round(REVENUE - (COST_INV + COST_PROD), 2)
            ### Technical Analysis
            SIZE_AC = float(round([value(instance.SOLAR_AC_SIZE)][0], 0))
            SIZE_DC = float(round([value(instance.SOLAR_DC_SIZE)][0], 0))
            RATIO = SIZE_DC / SIZE_AC
            SIZE = '{size_ac}@{ratio}ratio'.format(size_ac=round(SIZE_AC),
                                                   ratio=round(RATIO, 2))
            df_ts['StoA'] = [value(instance.StoA[j]) for j in instance.PERIOD]
            df_ts['Solar'] = df_ts['StoA']  ## output
            df_ts['SOLAR_DC'] = [value(instance.SOLAR_DC_PROD[j]) for j in instance.PERIOD]
            df_ts['SOLAR_DC_INV'] = [value(instance.SOLAR_DC_INV[j]) for j in instance.PERIOD]
            df_ts['SOLAR_AC_INV'] = [value(instance.SOLAR_AC_INV[j]) for j in instance.PERIOD]
            df_ts['SLoss_DC'] = [value(instance.SLoss_DC[j]) for j in instance.PERIOD]
            df_ts['SLoss_AC'] = [value(instance.SLoss_AC[j]) for j in instance.PERIOD]
            df_ts['SLoss'] = df_ts['SLoss_DC'] + df_ts['SLoss_AC']
            df_ts['SOLAR'] = df_ts['StoA'] + df_ts['SLoss_AC']
            DELIVERED = round(float(sum(df_ts['StoA'])), 1)
            LOSS = round(float(sum(df_ts['SLoss'])))
            NCF = round(float(sum(df_ts['StoA'])) / (len(df_ts['StoA']) * SIZE_AC), 4)

            #### out information
            df_ts_dispatch['Solar'] = df_ts['StoA']

            if 'battery' in asset:
                df_ts['StoB'] = [(-1) * value(instance.StoB[j]) for j in instance.PERIOD]
                df_ts['Resource Solar'] = df_ts['StoA'] - df_ts['StoB']
                STORED = round(float(sum(df_ts['StoB'])))
                S_STORED = STORED
                #### out information
                df_ts_dispatch['Resource Solar'] = df_ts[['Resource Solar']]
                df_ts_battery['ChargeSolar'] = df_ts[['StoB']]

            else:
                S_STORED = None

            table1_solar = \
                {
                    'Description': ['Size [kW]',
                                    'Energy Delivered [kWh]',
                                    'Energy Stored [kWh]',
                                    'Energy Loss [kWh]',
                                    'Capacity Factor [p.u.]'],
                    'Solar': [SIZE,
                              DELIVERED,
                              S_STORED,
                              LOSS,
                              NCF],
                }

            table_eco_solar = \
                {
                    'Description': ['Profit [M$]',
                                    'Revenue [M$]',
                                    'Cost [M$]',
                                    'Cost Inv [M$]',
                                    'Cost Prod [M$]',
                                    'Cost Energy [$/kWh]',
                                    ],
                    'Solar': [PROFIT,
                              REVENUE,
                              "----",
                              COST_INV,
                              COST_PROD,
                              COST_PROD / DELIVERED]

                }

            df_solar = pd.DataFrame(table1_solar).fillna('')
            df_solar_eco = pd.DataFrame(table_eco_solar).fillna('')

        if 'battery' in asset:
            ### Economic Analysis
            COST_INV = round(float([value(instance.BATTERY_INV_COST)][0]) / MILLON, 2)
            COST_PROD = round(float([value(instance.BATTERY_PROD_COST)][0]) / MILLON, 2)
            COST = round(float([value(instance.BATTERY_GRID_COST)][0]) / MILLON, 2)
            REVENUE = round(float([value(instance.BATTERY_GRID_REVENUE)][0]) / MILLON, 2)
            PROFIT = round((REVENUE - COST) - (COST_INV + COST_PROD), 2)

            ### Technical Analysis
            POWER = float(round([value(instance.BATTERY_SIZE_POWER)][0], 0))
            CAPACITY = float(round([value(instance.BATTERY_SIZE_CAPACITY)][0], 0))
            DURATION = CAPACITY / POWER
            SIZE = "{size_power}@{dur}hr".format(size_power=POWER, dur=DURATION)

            ### Time Series
            df_ts['GtoB'] = [(-1) * value(instance.GtoB[j]) for j in instance.PERIOD]
            df_ts['B_CHARGE'] = [(-1) * value(instance.B_CHARGE[j]) for j in instance.PERIOD]
            df_ts['B_DISCHARGE'] = [value(instance.B_DISCHARGE[j]) for j in instance.PERIOD]
            df_ts['BATTERY'] = df_ts['B_DISCHARGE'] + df_ts['B_CHARGE']
            df_ts['B_SOC'] = [value(instance.B_SOC[j]) for j in instance.PERIOD]
            df_ts['CYCLES'] = sum(df_ts['B_DISCHARGE']) / CAPACITY
            # round(float(sum(df_ts['WtoA'])), 1)
            DELIVERED = round(float(sum(df_ts['B_DISCHARGE'])), 0)
            B_STORED = round(float(sum(df_ts['B_CHARGE'])))
            LOSS = 100 * round(float((B_STORED - DELIVERED) / B_STORED))
            CYCLES = round(float(sum(df_ts['B_DISCHARGE']) / CAPACITY))

            if 'wind' in asset:
                B_STORED = B_STORED + W_STORED

            if 'solar' in asset:
                B_STORED = B_STORED + S_STORED

            table1_battery = {
                'Description': ['Size [kW]',
                                'Energy Delivered [kWh]',
                                'Energy Stored [kWh]',
                                'Energy Loss [kWh]',
                                'Cycles'],
                'Battery': [SIZE,
                            DELIVERED,
                            B_STORED,
                            LOSS,
                            CYCLES
                            ],
            }

            table_eco_battery = \
                {
                    'Description': ['Profit [M$]',
                                    'Revenue [M$]',
                                    'Cost [M$]',
                                    'Cost Inv [M$]',
                                    'Cost Prod [M$]',
                                    'Cost Energy [$/kWh]',
                                    ],
                    'Battery': [PROFIT,
                                REVENUE,
                                COST,
                                COST_INV,
                                COST_PROD,
                                round((COST_PROD / DELIVERED), 2)]

                }

            df_battery = pd.DataFrame(table1_battery).fillna('')
            df_battery_eco = pd.DataFrame(table_eco_battery).fillna('')

            #### out information
            df_ts_dispatch['Battery'] = df_ts[['BATTERY']]
            df_ts_battery[['SoC', 'ChargeGrid', 'Discharge', 'Battery']] = df_ts[
                ['B_SOC', 'GtoB', 'B_DISCHARGE', 'BATTERY']]

            ts_bat = self.get_fig_battery(df_fig=df_ts_battery)

        ts_dispacth = self.get_fig_dispatch(df_fig=df_ts_dispatch)

        table1 = {
            'Description': ['Size [kW]',
                            'Energy Delivered [kWh]',
                            'Energy Stored [kWh]',
                            'Energy Loss [kWh]',
                            'Capacity Factor [p.u.]',
                            'Cycles'],
        }

        df_final = pd.DataFrame(table1)
        df_final = df_final.merge(df_wind, on='Description', how='left') if 'wind' in asset else df_final
        df_final = df_final.merge(df_solar, on='Description', how='left') if 'solar' in asset else df_final
        df_final = df_final.merge(df_battery, on='Description', how='left') if 'battery' in asset else df_final

        table_economics = {
            'Description': ['Profit [M$]',
                            'Revenue [M$]',
                            'Cost [M$]',
                            'Cost Inv [M$]',
                            'Cost Prod [M$]',
                            'Cost Energy [$/kWh]',
                            ],
        }

        df_eco = pd.DataFrame(table_economics)
        df_eco = df_eco.merge(df_wind_eco, on='Description', how='left') if 'wind' in asset else df_eco
        df_eco = df_eco.merge(df_solar_eco, on='Description', how='left') if 'solar' in asset else df_eco
        df_eco = df_eco.merge(df_battery_eco, on='Description', how='left') if 'battery' in asset else df_eco

        return [df_eco, df_final, ts_dispacth, ts_bat]

    def get_fig_battery(self, df_fig=None):

        if df_fig is not None:
            num_cols = len(df_fig.columns)
            df_fig_index = df_fig.reset_index()
            if num_cols > 1:
                fig = sp.make_subplots(specs=[[{"secondary_y": True}]])
                # Add traces for the 'Battery' column on the primary (left) y-axis
                fig.add_trace(
                    go.Scatter(x=df_fig_index['index'], y=df_fig['SoC'], name='SoC', mode='lines', line_shape='hv'
                               ), secondary_y=True)
                for col in df_fig.columns:
                    if col != 'SoC':
                        fig.add_trace(go.Scatter(x=df_fig_index['index'], y=df_fig[col], name=col,
                                                 mode='lines', line_shape='hv'))

                # Define the layout of the plot
                fig.update_layout(
                    title='Battery Dispatch',
                    height=600,  # Change this value to set the height as needed
                    xaxis=dict(title='time [h]'),
                    yaxis=dict(title='kW'),
                    yaxis2=dict(title='SoC [%]', overlaying='y', side='right')
                )
        else:
            fig = None

        return fig

    def get_fig_dispatch(self, df_fig=None):

        if df_fig is not None:
            df_fig_index = df_fig.reset_index()
            fig = sp.make_subplots(specs=[[{"secondary_y": True}]])
            # Add traces for the 'Battery' column on the primary (left) y-axis

            fig.add_trace(go.Scatter(x=df_fig_index['index'], y=df_fig['Solar'], name='Solar', mode='lines',
                                     )) if 'Solar' in df_fig.columns else None

            fig.add_trace(go.Scatter(x=df_fig_index['index'], y=df_fig['Wind'], name='Wind', mode='lines',
                                     )) if 'Wind' in df_fig.columns else None

            fig.add_trace(go.Scatter(x=df_fig_index['index'], y=df_fig['Battery'], name='Battery', mode='lines',
                                     line_shape='hv')) if 'Battery' in df_fig.columns else None

            fig.add_trace(go.Scatter(x=df_fig_index['index'], y=df_fig['SolarBatt'], name='SolarBatt',
                                     mode='lines', visible='legendonly')) if 'SolarBatt' in df_fig.columns else None

            fig.add_trace(go.Scatter(x=df_fig_index['index'], y=df_fig['WindBatt'], name='WindBatt',
                                     mode='lines',
                                     visible='legendonly', )) if 'WindBatt' in df_fig.columns else None

            # Add traces for the 'LMP' column on the secondary (right) y-axis
            fig.add_trace(go.Scatter(x=df_fig_index['index'], y=df_fig['LMP'], name='LMP', mode='lines',
                                     ), secondary_y=True) if 'LMP' in df_fig.columns else None

            # Define the layout of the plot
            fig.update_layout(
                title='Dispatch',
                height=600,  # Change this value to set the height as needed
                xaxis=dict(title='time [h]'),
                yaxis=dict(title='kW'),
                yaxis2=dict(title='$/kWh', overlaying='y', side='right')
            )

        else:
            fig = None

        return fig

        # return table_1, table2, fig1, fig2