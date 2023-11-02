s = Simulation(ts_from=self.df_ui_timeseries['date_start'][0],
               ts_to=self.df_ui_timeseries['date_end'][0],
               lat=self.df_ui_timeseries['lat'][0],
               lon=self.df_ui_timeseries['lon'][0],
               tz=None)

asset = RenewableAsset(
            poi=100,
            loss=None,
            mode=None,
            wind=wind_farm,
            solar=solar_park,
            storage=bes,
        )

wind_farm = WindFarm(
    poi=100,
    loss=None,
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

wind = Wind(ts_from=self.df_ui_timeseries['date_start'][0],
            ts_to=self.df_ui_timeseries['date_end'][0],
            lat=self.df_ui_timeseries['lat'][0],
            lon=self.df_ui_timeseries['lon'][0],
            wind_farm=wind_farm
            )
df_wind = wind.get_wind_cap_factor()

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

solar = Solar(ts_from=self.df_ui_timeseries['date_start'][0],
              ts_to=self.df_ui_timeseries['date_end'][0],
              lat=self.df_ui_timeseries['lat'][0],
              lon=self.df_ui_timeseries['lon'][0],
              solar_park=solar_park
              )

df_solar = solar.get_solar_cap_factor()

bes = BES(
    poi=100,
    loss=None,
    battery=Battery(
        rte=0.9),
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
        dod_conf='fix',
        dod_fix=10,
        dod_lb_min=20,
        dod_ub_max=30,
        cycle_conf='fix',
        cycle_fix=10,
        cycle_lb_min=20,
        cycle_ub_max=30,
    ),
)


load_caiso = Load(
    demand_id='ACTUAL',
    demand_factor=1,
    area='CA ISO-TAC',
)