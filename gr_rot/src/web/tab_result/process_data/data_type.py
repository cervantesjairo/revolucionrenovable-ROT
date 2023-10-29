from gr_comun.src.renewable.asset.ren_asset import RenewableAsset


class DataFormat:

    def __init__(self,
                 ts_wind=None,
                 ts_solar=None,
                 ts_price=None,
                 ts_demand=None,
                 asset=None):
        self.ts_wind = ts_wind
        self.ts_solar = ts_solar
        self.ts_price = ts_price
        self.ts_demand = ts_demand
        self.asset = asset

    def get_data_type(self):


        return None


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
                                                     df_par=df_par[solar_inverter_mode_value_col], )

        solar_ratio_mode_col = ['solar_ratio_mode']
        solar_ratio_mode_value_col = ['solar_ratio_fix', 'solar_ratio_lb_min', 'solar_ratio_ub_max']
        df_ratio_mode_value = self.mode_fix_range(df_mode=df_mode[solar_ratio_mode_col],
                                                  df_par=df_par[solar_ratio_mode_value_col], )
        df = pd.concat([
            df_solar_poi,
            df_capex_cost,
            df_opex_cost,
            df_loss_percentage,
            df_inverter_mode_value,
            df_ratio_mode_value,
        ], axis=1)