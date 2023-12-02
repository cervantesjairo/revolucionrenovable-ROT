import pandas as pd
from pyomo.environ import *
import dash
from dash import dcc, html
import pandas as pd
import time
import datetime
import plotly.graph_objs as go
import plotly.subplots as sp
from gr_models.src.renewable.asset.nomenclature.asset import AssetNomenclature as An
from gr_models.src.renewable.asset.nomenclature.wind import WindNomenclature as Wn
from gr_models.src.renewable.asset.nomenclature.solar import SolarNomenclature as Sn
from gr_models.src.renewable.asset.nomenclature.battery import BatteryNomenclature as Bn


class Figures:
    def __init__(self,
                 df_ts: pd.DataFrame = None,
                 df_cv: pd.DataFrame = None,):
        self.df_ts = df_ts
        self.df_cv = df_cv

    def get_fig_dispatch(self):
        
        df_ts = self.df_ts

        df_ts_index = df_ts.reset_index()
        fig = sp.make_subplots(specs=[[{"secondary_y": True}]])

        # first y-axis
        fig.add_trace(go.Scatter(x=df_ts_index[An.DT_FROM], y=df_ts[Sn.vStoA], name='Solar', mode='lines',
                                 )) if Sn.vStoA in df_ts.columns else None

        fig.add_trace(go.Scatter(x=df_ts_index[An.DT_FROM], y=df_ts[Sn.vInvAC], name='SolarDC', mode='lines',
                                 )) if Sn.vInvAC in df_ts.columns else None

        fig.add_trace(go.Scatter(x=df_ts_index[An.DT_FROM], y=(df_ts[Sn.vStoA] + df_ts[Bn.vStoB]), name='SolarAC', mode='lines',
                                 )) if Sn.vStoA and Bn.vStoB in df_ts.columns else None

        fig.add_trace(go.Scatter(x=df_ts_index[An.DT_FROM], y=df_ts[Wn.vWtoA], name='Wind', mode='lines',
                                 )) if Wn.vWtoA in df_ts.columns else None

        fig.add_trace(go.Scatter(x=df_ts_index[An.DT_FROM], y=(df_ts[Wn.vWtoA] + df_ts[Bn.vWtoB]), name='Wind-Bat', mode='lines',
                                 )) if Wn.vWtoA and Bn.vWtoB in df_ts.columns else None

        fig.add_trace(go.Scatter(x=df_ts_index[An.DT_FROM], y=df_ts[Bn.vDisp], name='Battery', mode='lines',
                                 )) if Bn.vDisp in df_ts.columns else None

        # Add traces for the 'LMP' column on the secondary (right) y-axis
        fig.add_trace(go.Scatter(x=df_ts_index[An.DT_FROM], y=df_ts[An.pLMP], name='LMP', mode='lines',
                                 ), secondary_y=True) if An.pLMP in df_ts.columns else None

        # Define the layout of the plot
        fig.update_layout(
            title='Dispatch',
            height=600,  # Change this value to set the height as needed
            xaxis=dict(title='time [h]'),
            yaxis=dict(title='kW'),
            yaxis2=dict(title='$/kWh', overlaying='y', side='right')
        )

        return fig

    def get_fig_battery(self):

        df_ts = self.df_ts

        df_ts_index = df_ts.reset_index()
        fig = sp.make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Scatter(x=df_ts_index[An.DT_FROM], y=df_ts[Bn.vDisp], name='Battery', mode='lines',
                                 )) if Bn.vDisp in df_ts.columns else None

        fig.add_trace(go.Scatter(x=df_ts_index[An.DT_FROM], y=df_ts[Bn.vStoB], name='Solar', mode='lines',
                                 )) if Bn.vStoB in df_ts.columns else None

        fig.add_trace(go.Scatter(x=df_ts_index[An.DT_FROM], y=df_ts[Bn.vWtoB], name='Wind', mode='lines',
                                 )) if Bn.vWtoB in df_ts.columns else None

        fig.add_trace(go.Scatter(x=df_ts_index[An.DT_FROM], y=df_ts[Bn.vGtoB], name='Grid', mode='lines',
                                 )) if Bn.vGtoB in df_ts.columns else None

        fig.add_trace(go.Scatter(x=df_ts_index[An.DT_FROM], y=df_ts[Bn.vBtoA], name='Discharge', mode='lines',
                                 )) if Bn.vBtoA in df_ts.columns else None

        fig.add_trace(go.Scatter(x=df_ts_index[An.DT_FROM], y=df_ts[Bn.vSOC], name='SoC', mode='lines',
                                 ), secondary_y=True) if Bn.vSOC in df_ts.columns else None

        fig.update_layout(
            title='Dispatch',
            height=600,  # Change this value to set the height as needed
            xaxis=dict(title='time [h]'),
            yaxis=dict(title='kW'),
            yaxis2=dict(title='%', overlaying='y', side='right')
        )

        return fig

    def get_table_summary(self):
        df_cv = self.df_cv

        cv_wind = df_cv[0]
        cv_solar = df_cv[1]
        cv_battery = df_cv[2]

        df = pd.DataFrame({
            'Description':
                ['Size [kW]',
                 'Energy Delivered [kWh]',
                 'Energy Stored [kWh]',
                 'Energy Loss [kWh]',
                 'Capacity Factor [p.u.]',
                 'Cycles'],
             }
        )

        df_wind = pd.DataFrame({
            'Description':
                ['Size [kW]',
                 'Energy Delivered [kWh]',
                 'Energy Stored [kWh]',
                 'Energy Loss [kWh]',
                 'Capacity Factor [p.u.]'
                 ],
            'Wind':
                [cv_wind['Size [kW]'][0],
                 cv_wind['Energy Delivered [kWh]'][0],
                 cv_wind['Energy Stored [kWh]'][0],
                 cv_wind['Energy Loss [kWh]'][0],
                 cv_wind['NCF [p.u.]'][0],
                 ],
        }
        )

        df_solar = pd.DataFrame({
            'Description':
                ['Size [kW]',
                 'Energy Delivered [kWh]',
                 'Energy Stored [kWh]',
                 'Energy Loss [kWh]',
                 'NCF [p.u.]',
                 ],
            'Solar':
                [cv_solar['Size [kW/ratio]'][0],
                 cv_solar['Energy Delivered [kWh]'][0],
                 cv_solar['Energy Stored [kWh]'][0],
                 cv_solar['Energy Loss [kWh]'][0],
                 cv_solar['NCF [p.u.]'][0],
                 ],
        }
        )

        df_battery = pd.DataFrame({
            'Description':
                ['Size [kW]',
                 'Energy Delivered [kWh]',
                 'Energy Stored [kWh]',
                 'Energy Loss [kWh]',
                 'Cycles',
                 ],
            'Battery':
                [cv_battery['Size [kW/dur]'][0],
                 cv_battery['Energy Delivered [kWh]'][0],
                 cv_battery['Energy Stored [kWh]'][0],
                 cv_battery['Energy Loss [kWh]'][0],
                 cv_battery['Cycles'][0],
                 ],
        }
        )

        df = df.merge(df_wind, on='Description', how='left')
        df = df.merge(df_solar, on='Description', how='left')
        df = df.merge(df_battery, on='Description', how='left')

        return df

    def get_table_econ(self):
        df_cv = self.df_cv

        cv_wind = df_cv[0]
        cv_solar = df_cv[1]
        cv_battery = df_cv[2]

        df = pd.DataFrame({
            'Description':
                ['Profit [M$]',
                 'Revenue [M$]',
                 'Cost [M$]',
                 'Cost Inv [M$]',
                 'Cost Prod [M$]',
                 'Cost Energy [$/kWh]',
                 ],
        }
        )

        df_wind = pd.DataFrame({
            'Description':
                ['Profit [M$]',
                 'Revenue [M$]',
                 'Cost [M$]',
                 'Cost Inv [M$]',
                 'Cost Prod [M$]',
                 'Cost Energy [$/kWh]',
                 ],
            'Wind':
                [cv_wind['Profit [M$]'][0],
                 cv_wind['Revenue [M$]'][0],
                 "----",
                 cv_wind['Cost Inv [M$]'][0],
                 cv_wind['Cost Prod [M$]'][0],
                 cv_wind['Cost Prod [M$]'][0]/cv_wind['Energy Delivered [kWh]'][0],
                 ],
        }
        )

        df_solar = pd.DataFrame({
            'Description':
                ['Profit [M$]',
                 'Revenue [M$]',
                 'Cost [M$]',
                 'Cost Inv [M$]',
                 'Cost Prod [M$]',
                 'Cost Energy [$/kWh]',
                 ],
            'Solar':
                [cv_solar['Profit [M$]'][0],
                 cv_solar['Revenue [M$]'][0],
                 "----",
                 cv_solar['Cost Inv [M$]'][0],
                 cv_solar['Cost Prod [M$]'][0],
                 cv_solar['Cost Prod [M$]'][0]/cv_solar['Energy Delivered [kWh]'][0],
                 ],
        }
        )

        df_battery = pd.DataFrame({
            'Description':
                ['Profit [M$]',
                 'Revenue [M$]',
                 'Cost [M$]',
                 'Cost Inv [M$]',
                 'Cost Prod [M$]',
                 'Cost Energy [$/kWh]',
                 ],
            'Battery':
                [cv_battery['Profit [M$]'][0],
                 cv_battery['Revenue [M$]'][0],
                 cv_battery['Cost Grid [M$]'][0],
                 cv_battery['Cost Inv [M$]'][0],
                 cv_battery['Cost Prod [M$]'][0],
                 cv_battery['Cost Prod [M$]'][0]/cv_battery['Energy Delivered [kWh]'][0],
                 ],
        }
        )

        df = df.merge(df_wind, on='Description', how='left')
        df = df.merge(df_solar, on='Description', how='left')
        df = df.merge(df_battery, on='Description', how='left')

        return df
