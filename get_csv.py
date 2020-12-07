import numpy as np
import pandas as pd

#loading the data
raw_us_deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv', index_col=0)
raw_us_confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv', index_col=0)

#cleaning the deaths dataframe:

raw_us_deaths.rename(columns={'Admin2':'county', 'Province_State':'state', 'iso2':'country', 'Long_':'lon' }, inplace=True)
raw_us_deaths = raw_us_deaths.drop(columns=['Combined_Key', 'iso3', 'code3', 'FIPS', 'Country_Region', 'Combined_Key' ])
raw_us_deaths.columns = raw_us_deaths.columns.str.lower()

# cleaning the cases dataframe:
raw_us_confirmed.rename(columns={'Admin2':'county', 'Province_State':'state', 'iso2':'country', 'Long_':'lon' }, inplace=True)
raw_us_confirmed = raw_us_confirmed.drop(columns=['Combined_Key', 'iso3', 'code3', 'FIPS', 'Country_Region', 'Combined_Key' ])
raw_us_confirmed.columns = raw_us_confirmed.columns.str.lower()

# Transposing the Data and Merging into 1 DataFrame

dates = raw_us_deaths.columns[6:].copy()
deaths_transposed = raw_us_deaths.melt(
    id_vars=['country', 'state', 'county', 'lat', 'lon'],
    value_vars=dates,
    var_name='date', 
    value_name='deaths')
confirmed_transposed = raw_us_confirmed.melt(
    id_vars=['country', 'state', 'county', 'lat', 'lon'],
    value_vars=dates,
    var_name='date', 
    value_name='confirmed')
#merging
us_covid = deaths_transposed.merge(
    confirmed_transposed, how='right', 
    on=['country', 'state', 'county', 'lat', 'lon', 'date'])
#clean NaN
us_covid.deaths = us_covid.deaths.fillna(0)

# creating new dataframe for states:
state_grouped = us_covid.groupby(['date', 'state'])[['confirmed','deaths']].sum().reset_index().copy()


#parsing dates
import datetime
#need to convert date to datetime
us_covid['date'] = pd.to_datetime(us_covid.date, format='%m/%d/%y')
us_covid['month_num'] = pd.DatetimeIndex(us_covid['date']).month
us_covid['month'] = pd.to_datetime(us_covid['month_num'], format='%m').dt.month_name().str.slice(stop=3)

#dataframe grouped by month
state_grouped_month = us_covid.groupby(['month', 'month_num', 'state'])[['confirmed','deaths', 'month' ]].sum().reset_index().copy()
state_grouped_month.head()

#dataframe of single state
texas = state_grouped_month[state_grouped_month.state =='Texas'].sort_values(by='month_num')
