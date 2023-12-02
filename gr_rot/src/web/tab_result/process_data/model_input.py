import pandas as pd

from gr_comun.src.timeseries.ts_rot import TimeSeriesROT
from gr_comun.src.timeseries.object.simulation import Simulation
from gr_comun.src.timeseries.object.project import ProjectRenewable
from gr_comun.src.eng_economy.cashflow import CashFlowMeasures
from gr_comun.src.renewable.asset.ren_asset import RenewableAsset
from gr_comun.src.renewable.wind.object.elements import WindTurbine, WindCost, WindMode
from gr_comun.src.renewable.wind.windfarm import WindFarm
from gr_comun.src.renewable.wind.object.msg import WindMSG as Wmsg
from gr_comun.src.renewable.solar.object.elements import PanelInv, SolarCost, SolarMode
from gr_comun.src.renewable.solar.solarpark import SolarPark
from gr_comun.src.renewable.solar.object.msg import SolarMSG as Smsg
from gr_comun.src.renewable.storage.object.elements import Battery, BatteryCost, BatteryMode
from gr_comun.src.renewable.storage.battery import BES
from gr_comun.src.load.object.load import Load
from gr_comun.src.price.object.price import Price
from gr_comun.src.timeseries.is_rot import InvariantSeries
from gr_models.src.renewable.data.dat_file import DatFile
from gr_models.src.renewable.solve import ModelSolution
from gr_models.src.renewable.result import ResultOptimization
from gr_models.src.renewable.display import Figures
import pandas as pd


class ProblemSolution:

    def __init__(self, 
                 df_input: pd.DataFrame(),
                 ):
        self.df_input = df_input

    def get_results(self):

        df_par = self.df_input.select_dtypes(exclude='object')

        sim = Simulation(ts_from=self.df_input['date_start'][0],
                         ts_to=self.df_input['date_end'][0],
                         lat=self.df_input['lat'][0],
                         lon=self.df_input['lon'][0],
                         tz=None,
                         freq='H'
                         )

        cashflow = CashFlowMeasures(eco_lifetime=self.df_input['planning_horizon'][0],
                                    interest_rate=self.df_input['interest_rate'][0],
                                    compounding='Y'
                                    )

        project = ProjectRenewable(name='project',
                                   config='wind_solar_battery',
                                   simulation=None,
                                   financial=None,
                                   )
        #
        wind_farm = WindFarm(
            poi=100,
            loss=0,
            turbine=WindTurbine(
                rated_power=df_par[Wmsg.WT_RP][0],
                v_rated=df_par[Wmsg.WT_VR][0],
                v_cut_in=df_par[Wmsg.WT_VI][0],
                v_cut_out=df_par[Wmsg.WT_VO][0],
                hub_height=df_par[Wmsg.WT_HH][0],
                rotor_diameter=df_par[Wmsg.WT_RD][0],
            ),
            cost=WindCost(
                capex_wind=10,
                capex_inter=20,
                opex_fix=30,
                opex_variable=40,
            ),
            mode=WindMode(
                size_conf='fix',  ##fix, range, optimize
                size_fix=10,
                size_lb_min=20,
                size_ub_max=30,
            ),
        )

        solar_park = SolarPark(
            poi=100,
            loss=None,
            panel_inv=PanelInv(
                panel_power_nominal=535,
                panel_area=df_par[Smsg.P_AREA][0],
                panel_eff=df_par[Smsg.P_EFF][0],
                panel_deg=df_par[Smsg.P_DEG][0],
                inv_eff=df_par[Smsg.I_EFF][0],
                inv_dc_loss=df_par[Smsg.I_DC_LOSS][0],
                inv_ac_loss=df_par[Smsg.I_AC_LOSS][0],
            ),
            cost=SolarCost(
                capex_panel=10,
                capex_bos=20,
                capex_inv=30,
                opex_var=40,
                opex_fix=50,
            ),
            mode=SolarMode(
                inv_conf='fix',
                inv_fix=10,
                inv_lb_min=20,
                inv_ub_max=30,
                ratio_conf='fix',
                ratio_fix=10,
                ratio_lb_min=20,
                ratio_ub_max=30,
            ),

        )
        bes = BES(
            poi=100,
            loss=None,
            battery=Battery(
                rte=90),
            cost=BatteryCost(
                capex_power=10,
                capex_capacity=20,
                opex_fix=30,
                opex_var=40,
            ),
            mode=BatteryMode(
                power_conf='fix',
                power_fix=10,
                power_lb_min=20,
                power_ub_max=30,
                dur_conf='fix',
                dur_fix=10,
                dur_lb_min=20,
                dur_ub_max=30,
                dod_conf='unrestricted',
                dod_fix=10,
                dod_lb_min=20,
                dod_ub_max=30,
                cycle_conf='range',
                cycle_fix=10,
                cycle_lb_min=0,
                cycle_ub_max=30,
            ),
        )

        load_caiso = Load(
            demand_id='ACTUAL',
            demand_factor=1,
            area='CA ISO-TAC',
        )

        price_caiso = Price(
            price_market_id='DAM',
            price_node_id='TH_NP15_GEN-APND' #df_mode['iso_price_dropdown_var'][0],
        )

        timeseries = TimeSeriesROT(
            simulation=sim,
            wind=wind_farm,
            solar=solar_park,
            storage=bes,
            load=load_caiso,
            price=price_caiso,
        )

        x = timeseries.get_timeseries_data()

        asset = RenewableAsset(name='project',
                               config='wind_solar_battery',
                               poi=100,
                               loss=None,
                               mode=None,
                               wind=wind_farm,
                               solar=solar_park,
                               storage=bes,)

        invariant_series = InvariantSeries(asset=asset,
                                           financial=cashflow,)

        y = invariant_series.get_invariant_series()

        # file = DatFile(time_series=x,
        #                constant_values=y).generate_dat_file()

        solution = ModelSolution(asset=asset,).solve()

        df_cv, df_ts = ResultOptimization(instance=solution,
                                          asset=asset,
                                          timeseries=x,
                                          ).get_result_df()

        rot_display = Figures(df_ts=df_ts,
                              df_cv=df_cv,)

        fig_dispatch = rot_display.get_fig_dispatch()
        fig_battery_dispatch = rot_display.get_fig_battery()
        tbl_summary = rot_display.get_table_summary()
        tbl_economics = rot_display.get_table_econ()

        return [tbl_economics, tbl_summary, fig_dispatch, fig_battery_dispatch]
