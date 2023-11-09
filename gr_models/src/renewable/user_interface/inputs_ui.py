from datetime import datetime


class UserInterface:
    def ui_input_lat_lon(self):
        ui_lat_lon = {
            'lat': 'latitude',
            'lon': 'longitude'}
        return ui_lat_lon

    def ui_input_date_range(self):
        ui_date_range = {
            'date_range': 'start_date',
            'date_range': 'end_date'}
        return ui_date_range

    def ui_input_info(self):
        ui_input_info = {
            'info_asset_mode': 'info_asset_mode',
            'info_asset_poi': 'info_asset_poi',
            'planning_horizon': 'planning_horizon',
            'interest_rate': 'interest_rate',
        }
        return ui_input_info

    def ui_input_iso(self):
        ui_input_iso = {
            'iso_price_dropdown_var': 'iso_price_dropdown_var',
            'iso_demand_dropdown_var': 'iso_demand_dropdown_var',
            'iso_demand_size_factor': 'iso_demand_size_factor',
        }
        return ui_input_iso

    def ui_input_wind(self):
        ui_input_wind = {
            'wind_poi': 'wind_poi',

            'wind_size_mode': 'wind_size_mode',

            'wind_cost': 'wind_cost',
            'wind_cost_inter': 'wind_cost_inter',
            'wind_cost_fix': 'wind_cost_fix',
            'wind_cost_variable': 'wind_cost_variable',
            'wind_size_fix': 'wind_size_fix',
            'wind_size_lb_min': 'wind_size_lb_min',
            'wind_size_ub_max': 'wind_size_ub_max',
            'wind_turbine_rated_power': 'wind_turbine_rated_power',
            'wind_turbine_rotor_diameter': 'wind_turbine_rotor_diameter',
            'wind_turbine_hub_height': 'wind_turbine_hub_height',
            'wind_turbine_v_rated': 'wind_turbine_v_rated',
            'wind_turbine_v_cut_in': 'wind_turbine_v_cut_in',
            'wind_turbine_v_cut_out': 'wind_turbine_v_cut_out'}

        return ui_input_wind

    def ui_input_solar(self):
        ui_input_solar = {
            'solar_poi': 'solar_poi',

            'solar_inverter_mode': 'solar_inverter_mode',
            'solar_ratio_mode': 'solar_ratio_mode',

            'solar_cost_panel': 'solar_cost_panel',
            'solar_cost_bos': 'solar_cost_bos',
            'solar_cost_inverter': 'solar_cost_inverter',
            'solar_cost_variable': 'solar_cost_variable',
            'solar_cost_fix': 'solar_cost_fix',

            'solar_size_fix': 'solar_size_fix',
            'solar_size_lb_min': 'solar_size_lb_min',
            'solar_size_ub_max': 'solar_size_ub_max',

            'solar_ratio_fix': 'solar_ratio_fix',
            'solar_ratio_lb_min': 'solar_ratio_lb_min',
            'solar_ratio_ub_max': 'solar_ratio_ub_max',

            'solar_panel_area': 'solar_panel_area',
            'solar_panel_eff': 'solar_panel_eff',
            'solar_panel_degradation': 'solar_panel_degradation',
            'solar_inv_eff': 'solar_inv_eff',
            'solar_inv_pre_loss': 'solar_inv_pre_loss',
            'solar_inv_post_loss': 'solar_inv_post_loss',
        }

        return ui_input_solar

    def ui_input_battery(self):
        ui_input_battery = {
            'battery_poi': 'battery_poi',

            'battery_power_mode': 'battery_power_mode',
            'battery_duration_mode': 'battery_duration_mode',
            'battery_cycle_mode': 'battery_cycle_mode',
            'battery_dod_mode': 'battery_dod_mode',

            'battery_power_fix': 'battery_power_fix',
            'battery_power_lb_min': 'battery_power_lb_min',
            'battery_power_ub_max': 'battery_power_ub_max',
            'battery_duration_fix': 'battery_duration_fix',
            'battery_duration_lb_min': 'battery_duration_lb_min',
            'battery_duration_ub_max': 'battery_duration_ub_max',
            'battery_cost_power': 'battery_cost_power',
            'battery_cost_capacity': 'battery_cost_capacity',
            'battery_cost_fix': 'battery_cost_fix',
            'battery_cost_variable': 'battery_cost_variable',
            'battery_rte': 'battery_rte',
            'battery_dod_lb_min': 'battery_dod_lb_min',
            'battery_dod_ub_max': 'battery_dod_ub_max',
            'battery_cycle_lb_min': 'battery_cycle_lb_min',
            'battery_cycle_ub_max': 'battery_cycle_ub_max',
        }

        return ui_input_battery
