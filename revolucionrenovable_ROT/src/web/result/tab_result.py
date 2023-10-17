from dash.dependencies import Input, Output, State
from dash import dash_table
import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go
import plotly.subplots as sp
from revolucionrenovable_ROT.src.msg.user_interface.inputs_ui import UserInterface

# from model.user_interface.inputs_ui import UserInterface
# from model.run import SolveModel


class TabResult:
    def __init__(self):
        self.layout = html.Div([
            html.Button('Run', id='run-btn'),
            html.Hr(),
            html.Div(id='result-table1'),
            html.Div(id='result-table2'),
            html.Div(id='result-figure'),
            html.Div(id='result-figure2'),
        ])

    def setup_callbacks(self, app, tab_asset):
        call = UserInterface()
        ui_wind = call.ui_input_wind()
        ui_battery = call.ui_input_battery()
        ui_solar = call.ui_input_solar()
        ui_info = call.ui_input_info()
        ui_iso = call.ui_input_iso()

        ui_input = ui_solar.copy()
        ui_input.update(ui_wind)
        ui_input.update(ui_battery)
        ui_input.update(ui_info)
        ui_input.update(ui_iso)
        
        @app.callback(
            [Output('result-table1', 'children'),
             Output('result-table2', 'children'),
             Output('result-figure', 'children'),
             Output('result-figure2', 'children')],
            [Input('run-btn', 'n_clicks')],
            State('date_range', 'start_date'),
            State('date_range', 'end_date'),
            State('lat', 'value'),
            State('lon', 'value'),
            *(State(input_id, 'value') for input_id in ui_input.keys()),
        )
        def update_result(n_clicks, start_date, end_date, lat, lon, *args):
            if n_clicks is None:
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update
            else:
                df_ui_input = pd.DataFrame({
                    key: [value] for key, value in zip(ui_input.values(), args)
                })

                df_ui_timeseries = pd.DataFrame()
                df_ui_timeseries['date_start'] = [start_date]
                df_ui_timeseries['date_end'] = [end_date]
                df_ui_timeseries['lat'] = [lat]
                df_ui_timeseries['lon'] = [lon]

                x = 1
                return x

                # model_ = SolveModel(df_ui_timeseries=df_ui_timeseries, df_ui_input=df_ui_input)
                # result_t1, result_t2, result_fig1, result_fig2 = model_.get_results()

                # table_eco = dash_table.DataTable(
                #     id='table',
                #     columns=[{'name': f'{col}', 'id': f'{col}'} for col in result_t1.columns],
                #     data=result_t1.to_dict('records'),
                #     style_table={'height': '300px', 'overflowY': 'auto', 'border': 'thin lightgrey solid'},
                #     style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                #     style_cell={
                #         'textAlign': 'left',
                #         'padding': '8px',  # Adjust cell padding
                #         'minWidth': '100px',  # Minimum column width
                #         'width': '150px',  # Default column width
                #         'maxWidth': '300px',  # Maximum column width
                #         'whiteSpace': 'normal',  # Wrap cell content
                #         'border': '1px solid grey',  # Border around cells
                #     },
                # )
                #
                # table_dispatch = dash_table.DataTable(
                #     id='table',
                #     columns=[{'name': f'{col}', 'id': f'{col}'} for col in result_t2.columns],
                #     data=result_t2.to_dict('records'),
                #     style_table={'height': '300px', 'overflowY': 'auto', 'border': 'thin lightgrey solid'},
                #     style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                #     style_cell={
                #         'textAlign': 'left',
                #         'padding': '8px',  # Adjust cell padding
                #         'minWidth': '100px',  # Minimum column width
                #         'width': '150px',  # Default column width
                #         'maxWidth': '300px',  # Maximum column width
                #         'whiteSpace': 'normal',  # Wrap cell content
                #         'border': '1px solid grey',  # Border around cells
                #     },
                # )
                #
                #
                # if result_fig1:
                #     fig_dispatch = dcc.Graph(figure=result_fig1)
                # else:
                #     fig_dispatch = html.Div()
                #
                # if result_fig2:
                #     fig_battery = dcc.Graph(figure=result_fig2)
                # else:
                #     fig_battery = html.Div()
                #
                # return table_eco, table_dispatch, fig_dispatch, fig_battery
