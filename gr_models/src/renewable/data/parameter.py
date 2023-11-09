# from common.economics.cost_recovery import CRF
# from common.database.caiso.price.query import CAISO_PRICE
# from common.database.caiso.demand.query import CAISO_DEMAND
# from common.database.nrel.resource.query import NREL_RESOURCE
# from common.database.nrel.wind.query import NREL_WIND
# from common.database.nrel.solar.query import NREL_SOLAR
#
# from common.timeseries.datetime import get_timeseries_latlon

import pandas as pd
import numpy as np


class Parametrize:
    def __init__(self, df_ui_timeseries=None, df_ui_input=None):
        self.df_ui_timeseries = df_ui_timeseries
        self.df_ui_input = df_ui_input

    def get_data(self):

        df_par = self.df_ui_input.select_dtypes(exclude='object')
        df_mode = self.df_ui_input.select_dtypes(include='object')
        df_timeseries = None
        # df_timeseries = self.get_timeseries_data(df_par=df_par,
        #                                          df_mode=df_mode,
        #                                          df_ts=self.df_ui_timeseries)

        asset_poi = df_par.filter(items=['info_asset_poi'])
        asset_config = df_mode.filter(items=['info_asset_mode'])
        info_asset, info_poi = self.get_information_data(df_par=asset_poi, df_mode=asset_config)

        _asset = info_asset['info_asset_mode'][0]
        df_solar_data = pd.DataFrame()
        df_wind_data = pd.DataFrame()
        df_battery_data = pd.DataFrame()
        if 'wind' in _asset:
            df_par_wind = df_par.filter(regex='wind')
            df_mode_wind = df_mode.filter(regex='wind')
            df_wind_data = self.get_wind_data(df_par=df_par_wind,
                                              df_mode=df_mode_wind)

        if 'solar' in _asset:
            df_par_solar = df_par.filter(regex='solar')
            df_mode_solar = df_mode.filter(regex='solar')
            df_solar_data = self.get_solar_data(df_par=df_par_solar,
                                                df_mode=df_mode_solar)

        if 'battery' in _asset:
            df_par_battery = df_par.filter(regex='battery')
            df_mode_battery = df_mode.filter(regex='battery')
            df_battery_data = self.get_battery_data(df_par=df_par_battery,
                                                    df_mode=df_mode_battery)

        df_par = pd.concat([
            info_poi,
            df_solar_data,
            df_wind_data,
            df_battery_data,
            ], axis=1)

        return df_mode, df_par, df_timeseries

    def get_information_data(self, df_par=None, df_mode=None):
        info_asset = df_mode
        info_poi = df_par

        return [info_asset, info_poi]

    def get_timeseries_data(self, df_par=None, df_mode=None, df_ts=None):
        # get time series
        lat = df_ts['lat'][0]
        lon = df_ts['lon'][0]
        start = df_ts['date_start'][0]
        end = df_ts['date_end'][0]

        timeseries = get_timeseries_latlon(lat=lat,
                                           lon=lon,
                                           ts_from=start,
                                           ts_to=end)

        _asset = df_mode['info_asset_mode'][0]
        if 'wind' in _asset or 'solar' in _asset:
            df_resource = NREL_RESOURCE(lat=lat,
                                        lon=lon,
                                        ts_from=start,
                                        ts_to=end,
                                        var='ghi,wind_speed').get_resource()


            df_panel = df_par[['solar_panel_area', 'solar_panel_eff', 'solar_panel_degradation']]
            df_turbine = df_par[['wind_turbine_rated_power', 'wind_turbine_rotor_diameter', 'wind_turbine_hub_height',
                                 'wind_turbine_v_cut_in', 'wind_turbine_v_rated', 'wind_turbine_v_cut_out']]

            if 'wind_and_solar' == _asset or 'wind_and_solar_and_battery' == _asset:
                wind = NREL_WIND(df_turbine=df_turbine, df_resource=df_resource).get_wind_factor()
                solar = NREL_SOLAR(df_panel=df_panel, df_resource=df_resource).get_solar_factor()
                renewable = pd.merge(wind, solar, on='local_datetime')

            if 'wind' == _asset or 'wind_and_battery' == _asset:
                wind = NREL_WIND(df_turbine=df_turbine, df_resource=df_resource).get_wind_factor()
                renewable = wind

            if 'solar' == _asset or 'solar_and_battery' == _asset:
                solar = NREL_SOLAR(df_panel=df_panel, df_resource=df_resource).get_solar_factor()
                renewable = solar

        price_market_id = 'DAM'         #TODO: add more options
        price_node_id = df_mode['iso_price_dropdown_var'][0]    ## what are the list of options. check the node reference for teh options

        if price_market_id:
            iso_lmp = CAISO_PRICE().get_lmp(market=price_market_id,
                                            node=price_node_id[0],
                                            ts_from=start,
                                            ts_to=end,
                                            )
        else:
            print("Price market ID is None. Please provide a valid value.")
            raise ValueError("Price market ID is empty. Please provide a valid value.")

        demand_id = df_mode['iso_demand_dropdown_var'][0]
        demand_factor = df_par['iso_demand_size_factor'][0]

        iso_load = pd.DataFrame()
        if demand_id:
            iso_load = CAISO_DEMAND().get_demand(market='ACTUAL',
                                                 ts_from=start,
                                                 ts_to=end,
                                                 execution_type=None)
            if demand_factor:
                iso_load_max = iso_load['load'].max()
                iso_load['load'] = (demand_factor / iso_load_max) * iso_load['load']

            merged_df = pd.merge(iso_lmp, iso_load, on='local_datetime')
        if not demand_id:
            merged_df = iso_lmp

        if 'wind' in _asset or 'solar' in _asset:
            renewable_merged = pd.merge(merged_df, renewable, on='local_datetime')
            df = pd.merge(timeseries, renewable_merged, on='local_datetime')
        else:
            df = pd.merge(timeseries, merged_df, on='local_datetime')

        return df

    def get_solar_data(self, df_par=None, df_mode=None):

        solar_poi_col = ['solar_poi']
        df_solar_poi = df_par[solar_poi_col]

        solar_capex_col = ['solar_cost_panel', 'solar_cost_inverter', 'solar_cost_bos']
        df_capex_cost = self.annualized_cost(df=df_par[solar_capex_col])

        solar_opex_col = ['solar_cost_variable', 'solar_cost_fix']
        df_opex_cost = self.annual_cost(df=df_par[solar_opex_col])

        solar_loss_col = ['solar_panel_degradation', 'solar_inv_eff', 'solar_inv_pre_loss', 'solar_inv_post_loss']
        df_loss_percentage = self.loss_per_unit(df=df_par[solar_loss_col])

        solar_inverter_mode_col = ['solar_inverter_mode']
        solar_inverter_mode_value_col = ['solar_size_fix', 'solar_size_lb_min', 'solar_size_ub_max']
        df_inverter_mode_value = self.mode_fix_range(df_mode=df_mode[solar_inverter_mode_col],
                                                     df_par=df_par[solar_inverter_mode_value_col],)

        solar_ratio_mode_col = ['solar_ratio_mode']
        solar_ratio_mode_value_col = ['solar_ratio_fix', 'solar_ratio_lb_min', 'solar_ratio_ub_max']
        df_ratio_mode_value = self.mode_fix_range(df_mode=df_mode[solar_ratio_mode_col],
                                                  df_par=df_par[solar_ratio_mode_value_col],)
        df = pd.concat([
            df_solar_poi,
            df_capex_cost,
            df_opex_cost,
            df_loss_percentage,
            df_inverter_mode_value,
            df_ratio_mode_value,
            ], axis=1)

        return df

    def get_wind_data(self, df_par=None, df_mode=None, df_resource=None):
        # wind_speed_col = ['datetime', 'wind_speed']
        # df_wind_speed = self.wind_factor_per_unit(df=df_resource[wind_speed_col])

        wind_poi_col = ['wind_poi']
        df_wind_poi = df_par[wind_poi_col]

        wind_capex_col = ['wind_cost', 'wind_cost_inter']
        df_wind_capex = self.annualized_cost(df=df_par[wind_capex_col])

        wind_opex_col = ['wind_cost_fix', 'wind_cost_variable']
        df_wind_opex = self.annual_cost(df=df_par[wind_opex_col])

        wind_loss_col = []
        df_loss_percentage = self.loss_per_unit(df=df_par[wind_loss_col])

        wind_size_mode_col = ['wind_size_mode']
        wind_size_value_col = ['wind_size_fix', 'wind_size_lb_min', 'wind_size_ub_max']
        df_wind_size_mode_value = self.mode_fix_range(df_mode=df_mode[wind_size_mode_col],
                                                      df_par=df_par[wind_size_value_col])

        df = pd.concat([
            df_wind_poi,
            df_wind_capex,
            df_wind_opex,
            df_loss_percentage,
            df_wind_size_mode_value
        ], axis=1)

        return df

    def get_battery_data(self, df_par=None, df_mode=None, df_resource=None):
        #
        # df_datetime = pd.DataFrame()
        # df_datetime['datetime'] = df_resource['datetime']

        battery_capex_col = ['battery_cost_power', 'battery_cost_capacity']
        df_battery_capex = self.annualized_cost(df=df_par[battery_capex_col])

        battery_power_col = ['battery_poi']
        df_battery_poi = df_par[battery_power_col]

        battery_opex_col = ['battery_cost_fix', 'battery_cost_variable']
        df_battery_opex = self.annual_cost(df=df_par[battery_opex_col])

        battery_loss_col = ['battery_rte']
        df_loss_percentage = self.loss_per_unit(df=df_par[battery_loss_col])

        battery_power_mode_col = ['battery_power_mode']
        battery_power_value_col = ['battery_power_fix', 'battery_power_lb_min', 'battery_power_ub_max']
        df_power_mode_value = self.mode_fix_range(df_mode=df_mode[battery_power_mode_col],
                                                  df_par=df_par[battery_power_value_col],)

        battery_dur_mode_col = ['battery_duration_mode']
        battery_dur_value_col = ['battery_duration_fix', 'battery_duration_lb_min', 'battery_duration_ub_max']
        df_duration_mode_value = self.mode_fix_range(df_mode=df_mode[battery_dur_mode_col],
                                                     df_par=df_par[battery_dur_value_col],)

        battery_cycle_mode_col = ['battery_cycle_mode']
        battery_cycle_value_col = ['battery_cycle_lb_min', 'battery_cycle_ub_max']
        df_cycle_mode_value = self.mode_unrestricted_range(df_mode=df_mode[battery_cycle_mode_col],
                                                           df_par=df_par[battery_cycle_value_col],)

        battery_dod_mode_col = ['battery_dod_mode']
        battery_dod_value_col = ['battery_dod_lb_min', 'battery_dod_ub_max']
        df_dummy1 = df_par[battery_dod_value_col] / 100
        df_dod_mode_value = self.mode_unrestricted_range(df_mode=df_mode[battery_dod_mode_col],
                                                         df_par=df_dummy1[battery_dod_value_col],)

        df = pd.concat([
            df_battery_poi,
            df_battery_capex,
            df_battery_opex,
            df_loss_percentage,
            df_power_mode_value,
            df_duration_mode_value,
            df_cycle_mode_value,
            df_dod_mode_value
            ],
            axis=1)

        return df

    def annualized_cost(self, df=None):
        crf = CRF(
            ph=self.df_ui_input['planning_horizon'][0],
            ir=self.df_ui_input['interest_rate'][0]
        )

        df = df * crf.cost_recovery_formula()

        return df

    def annual_cost(self, df):
        return df

    def loss_per_unit(self, df=None):
        df = df / 100
        return df

    def mode_fix_range(self, df_mode=None, df_par=None):
        col_mode = df_mode.columns[0]
        col_fix = df_par.columns[0]
        col_range = df_par.columns[1:3]

        if 'fix' in df_mode[col_mode][0]:
            df = df_par[[col_fix]]
        elif 'range' in df_mode[col_mode][0]:
            df = df_par[col_range]
        else:
            print("ERROR: Invalid value in mode.")

        return df

    def mode_unrestricted_range(self, df_mode=None, df_par=None):
        col_mode = df_mode.columns[0]
        col_range = df_par.columns[0:2]

        if 'unrestricted' in df_mode[col_mode][0]:
            df = None
        elif 'range' in df_mode[col_mode][0]:
            df = df_par[col_range]
        else:
            print("ERROR: Invalid value in mode.")

        return df


