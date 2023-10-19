import pandas as pd
from datetime import datetime, timedelta
from muiscaenergy_comun.src.timeseries.base import get_timeseries
from muiscaenergy_comun.src.messages.base import TimeSeriesMessage as TSm
from timezonefinder import TimezoneFinder
from dateutil import tz
import pytz


class NREL_RESOURCE:
    """
    This Class Object is a child class of NrelPSM that has the API information to pull NREL data. The class has
    a special method named __init__ and function definition.
    - The especial method includes var, lat, lon, period_range_from, period_range_to
    - The definition pulls data from database and cleans it to return a dataframe
    :param var: Variables, e.g., 'ghi,dhi,dni,clearsky_ghi,wind_direction,wind_speed,air_temperature,total_precipitable_water,solar_zenith_angle,surface_albedo'
    :param lat: Latitud, e.g., 4.6095
    :param lon: Longitud, e.g., -74.0685
    :param period_range_from: datetime(2020, 1, 1)
    :param period_range_to: datetime(2020, 12, 31)

    :returns df: dataframe with the set of solar and meteorological data fields from NREL
    #################################################################################
    # # https://developer.nrel.gov/docs/solar/nsrdb/psm3-download/
    # # https://developer.nrel.gov/docs/solar/nsrdb/python-examples/
    # # https://docs.python.org/3/library/string.html#format-string-syntax
    """

    def __init__(self, ts_from=None, ts_to=None):
        self.ts_from = ts_from
        self.ts_to = ts_to
        #1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020
        self.api_key = 'FVltdchrxzBCHiSNF6M7R4ua6BFe4j81fbPp8dDP'
        self.variables = 'ghi,dhi,dni,clearsky_ghi,wind_direction,wind_speed,air_temperature,total_precipitable_water,solar_zenith_angle,surface_albedo'
        self.mailing_list = 'false'
        self.your_name = 'Jairo+Cervantes'
        self.reason_for_use = 'research'
        self.your_affiliation = 'UNL'
        self.your_email = 'jairo.cervantes@huskers.unl.edu'
        self.leap_year = 'true'  # Set leap year to true or false. True will return leap day data if present, false will not.
        self.interval_data_base = '60'  # Set time interval in minutes, i.e., '30' is half hour intervals. Valid intervals are 30 & 60.
        self.utc = 'true'

    def get_resource(self, var=None, lat=None, lon=None):

        timeseries = get_timeseries(lat=lat,
                                    lon=lon,
                                    ts_from=self.ts_from,
                                    ts_to=self.ts_to)
        df_ts = timeseries.df
        years = pd.unique(pd.DatetimeIndex(df_ts[TSm.DT_UTC]).year)
        #2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024
        years_minus_4 = [year - 4 for year in years] # Since data stop in 2020 and we need more, it was shifted 4 years. The shift must be common to 4

        df0 = None
        for year in years_minus_4:
            url = 'https://developer.nrel.gov/api/nsrdb/v2/solar/psm3-download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(
                year=year, lat=lat, lon=lon, leap=self.leap_year, interval=self.interval_data_base, utc=self.utc,
                name=self.your_name, email=self.your_email, mailing_list=self.mailing_list, affiliation=self.your_affiliation,
                reason=self.reason_for_use, api=self.api_key, attr=var)

            pp = 60*8760  # 525600
            if year == 2000 or year == 2004 or year == 2008 or year == 2012 or year == 2016 or year == 2020:
                pp = 60 * 8784

            if year == years_minus_4[0]:
                # df0 = pd.read_csv(url) ### only to check units
                df0 = pd.read_csv(url, skiprows=2)
                df0 = df0.set_index(pd.date_range('1/1/{yr}'.format(yr=year), freq=self.interval_data_base + 'Min', periods=pp / int(self.interval_data_base)))
                info = pd.read_csv(url, nrows=1)
                # timezone, elevation = info['Local Time Zone'], info['Elevation']
            else:
                df1 = pd.read_csv(url, skiprows=2)
                df1 = df1.set_index(pd.date_range('1/1/{yr}'.format(yr=year), freq=self.interval_data_base + 'Min', periods=pp / int(self.interval_data_base)))
                df0 = pd.concat([df0, df1])
                del df1

        df0['Year'] = df0['Year'] + 4   # Since data stop in 2020 and we need more, it was shifted 4 years. The shift must be common to 4
        df0['datetime_lead_4_years'] = pd.to_datetime(df0[['Year', 'Month', 'Day', 'Hour']])
        df0['datetime_lead_4_years'] = df0['datetime_lead_4_years'].dt.tz_localize('UTC')

        df = df_ts.merge(df0, how='inner', left_on=TSm.DT_UTC, right_on='datetime_lead_4_years') #TODO: this datetime name should be part of a msg

        new_column_name = {'GHI': 'ghi',
                           'DHI': 'dhi',
                           'DNI': 'dni',
                           'Clearsky GHI': 'clearsky_ghi',
                           'Wind Speed': 'wind_speed',
                           'Wind Direction': 'wind_direction',
                           'Temperature': 'air_temperature',
                           'Precipitable Water': 'total_precipitable_water',
                           'Surface Albedo': 'surface_albedo',
                           'Solar Zenith Angle': 'solar_zenith_angle'}

        df = df.rename(columns=new_column_name)
        df = df.drop(columns=['Year', 'Month', 'Day', 'Hour', 'Minute', 'datetime_lead_4_years'])

        return df
