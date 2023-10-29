
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