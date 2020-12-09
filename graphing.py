import streamlit as st
import pandas as pd 
import datetime


# confirmed
def total_confirmed_graph(df):
    confirmed_per_day = df.groupby('date')['confirmed'].sum()
    st.write('Total US Cases:')
    st.line_chart(confirmed_per_day)

def daily_confirmed_graph(df):
    confirmed_per_day = df.groupby('date')['confirmed'].sum().reset_index(name='confirmed')
    shifted = confirmed_per_day['confirmed'].shift(1)
    confirmed_per_day['daily_confirmed'] = confirmed_per_day.confirmed - shifted
    confirmed_per_day.drop(columns=['confirmed'], axis=1, inplace=True)
    confirmed_per_day.set_index('date', inplace=True)
    st.write('Daily US Cases:')
    st.line_chart(confirmed_per_day)

# deaths
def total_deaths_graph(df):
    deaths_per_day = df.groupby('date')['deaths'].sum()
    st.write('Total US Deaths:')
    st.line_chart(deaths_per_day)

def daily_deaths_graph(df):
    deaths_per_day = df.groupby('date')['deaths'].sum().reset_index(name='deaths')
    shifted = deaths_per_day['deaths'].shift(1)
    deaths_per_day['daily_deaths'] = deaths_per_day.deaths - shifted
    deaths_per_day.drop(columns=['deaths'], axis=1, inplace=True)
    deaths_per_day.set_index('date', inplace=True)
    st.write('Daily US Deaths:')
    st.line_chart(deaths_per_day)

# by state confirmed
def state_confirmed_graph(df, county, state):
    state_total_confirmed = df.groupby('date')['confirmed'].sum()
    st.write(f'Total Cases in {county}, {state}:')
    st.line_chart(state_total_confirmed)

def state_daily_confirmed_graph(df, county, state):
    confirmed_per_day = df.groupby('date')['confirmed'].sum().reset_index(name='confirmed')
    shifted = confirmed_per_day['confirmed'].shift(1)
    confirmed_per_day['daily_confirmed'] = confirmed_per_day.confirmed - shifted
    confirmed_per_day.loc[confirmed_per_day.daily_confirmed <0, 'daily_confirmed'] = 0
    confirmed_per_day.drop(columns=['confirmed'], axis=1, inplace=True)
    confirmed_per_day.set_index('date', inplace=True)
    st.write(f'Daily {county}, {state} Cases:')
    st.bar_chart(confirmed_per_day)

# by state deaths
def state_death_graph(df, county, state):
    deaths_per_day = df.groupby('date')['deaths'].sum()
    st.write(f'Total Cases in {county}, {state}:')
    st.line_chart(deaths_per_day)

def state_daily_death_graph(df, county, state):
    deaths_per_day = df.groupby('date')['deaths'].sum().reset_index(name='deaths')
    shifted = deaths_per_day['deaths'].shift(1)
    deaths_per_day['daily_deaths'] = deaths_per_day.deaths - shifted
    deaths_per_day.loc[deaths_per_day.daily_deaths <0, 'daily_deaths'] = 0
    deaths_per_day.drop(columns=['deaths'], axis=1, inplace=True)
    deaths_per_day.set_index('date', inplace=True)
    st.write(f'Daily {county}, {state} Cases:')
    st.bar_chart(deaths_per_day)

# map
def us_map(df, state, county, date):
    #df['date'] = pd.to_datetime(df.date, format='%m/%d/%y')
    state_date = df[df.date.dt.date == date]
    st.subheader(f'Map of COVID-19 Cases on {date} for {state}:')
    st.map(state_date)

# state comparison
def compare_state_confirmed_graph(df, x):
    state_total_confirmed = df.groupby('date')['confirmed'].sum()
    # st.write(f'Total Cases in {state} and {second_state}:')
    st.line_chart(state_total_confirmed)
    # st.line_chart(state_total_confirmed)