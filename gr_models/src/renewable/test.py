import pandas as pd
from gr_models.src.renewable.run import SolveModel


data1 = {
    'date_start': ['2021-01-01T00:00:00'],
    'date_end': ['2021-01-10T00:00:00'],
    'lat': [34],
    'lon': [-120]
}
df1 = pd.DataFrame(data1)


data2 = {
    'solar_poi': 100,
    'solar_inverter_mode': ['fix'],
    'solar_ratio_mode': ['fix'],
    'solar_cost_panel': 300,
    'solar_cost_bos': 260,
    'solar_cost_inverter': 215,
    'solar_cost_variable': 0.0025,
    'solar_cost_fix': 10,
    'solar_size_fix': 100,
    'solar_size_lb_min': 0,
    'solar_size_ub_max': 200,
    'solar_ratio_fix': 1.25,
    'solar_ratio_lb_min': 1,
    'solar_ratio_ub_max': 1.5,
    'solar_panel_area': 1.92,
    'solar_panel_eff': 20,
    'solar_panel_degradation': 3,
    'solar_inv_eff': 95,
    'solar_inv_pre_loss': 2,
    'solar_inv_post_loss': 5,
    'wind_poi': 85,
    'wind_size_mode': ['fix'],
    'wind_cost': 1500,
    'wind_cost_inter': 0,
    'wind_cost_fix': 1.3,
    'wind_cost_variable': 0.00008,
    'wind_size_fix': 100,
    'wind_size_lb_min': 10,
    'wind_size_ub_max': 500,
    'wind_turbine_rated_power': 2500,
    'wind_turbine_rotor_diameter': 96,
    'wind_turbine_hub_height': 80,
    'wind_turbine_v_rated': 15,
    'wind_turbine_v_cut_in': 3.5,
    'wind_turbine_v_cut_out': 25,
    'battery_poi': 85,
    'battery_power_mode': ['fix'],
    'battery_duration_mode': ['fix'],
    'battery_cycle_mode': ['unrestricted'],
    'battery_dod_mode': ['unrestricted'],
    'battery_power_fix': 100,
    'battery_power_lb_min': 0,
    'battery_power_ub_max': 500,
    'battery_duration_fix': 4,
    'battery_duration_lb_min': 0,
    'battery_duration_ub_max': 8,
    'battery_cost_power': 300,
    'battery_cost_capacity': 215,
    'battery_cost_fix': 0.0025,
    'battery_cost_variable': 10,
    'battery_rte': 85,
    'battery_dod_lb_min': 0,
    'battery_dod_ub_max': 100,
    'battery_cycle_lb_min': 0,
    'battery_cycle_ub_max': 365,
    'info_asset_mode': 'wind_and_solar_and_battery',
    'info_asset_poi': 150,
    'planning_horizon': 10,
    'interest_rate': 7,
    'iso_price_dropdown_var': ['TH_NP15_GEN-APND'],
    'iso_demand_dropdown_var': None,
    'iso_demand_size_factor': 1
}
df2 = pd.DataFrame(data2)

model = SolveModel(df1, df2)
r1, r2, r3, r4 = model.get_results()

print(r1)
print(r2)
print(r3)
print(r4)




