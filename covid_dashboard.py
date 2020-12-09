# packages
import streamlit as st
import pandas as pd
import datetime
import get_csv
from numpy import insert

# importing packages I made
from my_functions import (
    get_state,
    get_second_state,
    get_county,
    filtered_by_state,
    filtered_two_state,
)
from graphing import (
    total_confirmed_graph,
    daily_confirmed_graph,
    total_deaths_graph,
    daily_deaths_graph,
    state_confirmed_graph,
    state_daily_confirmed_graph,
    state_death_graph,
    state_daily_death_graph,
    us_map,
    compare_state_confirmed_graph,
)

# read in data
data = get_csv.us_covid

# title
st.title('US COVID-19 Dashboard')

# navigation
nav_bar = st.sidebar.radio('Navigation', ('Home', 'Local Trends', 'Comparing States'))

# us trends page
if nav_bar == 'Home':
    st.header('This app is created from open COVID-19 provided by John Hopkins on GitHub')
    st.header('US Trends')
    total_confirmed_graph(data)
    daily_confirmed_graph(data)
    total_deaths_graph(data)
    daily_deaths_graph(data)

# local trends
elif nav_bar == 'Local Trends':
    map_coordinates = data[['lat', 'lon', 'county', 'state', 'date', 'confirmed', 'deaths']].copy()
    st.header('Local Trends')

    state_key = get_state(map_coordinates)
    state_key = insert(state_key, 0, "All")
    st.sidebar.header(f'Choose your county and state below:')
    state = st.sidebar.selectbox('Select your state ', state_key)
    county_key = get_county(map_coordinates, state)
    county_key = insert(county_key, 0, 'All')
    county = st.sidebar.selectbox('Select your county ', county_key)

    st_co_data = filtered_by_state(data, county, state)

    if not st_co_data.empty:
        state_confirmed_graph(st_co_data, county, state)
        state_daily_confirmed_graph(st_co_data, county, state)
        state_death_graph(st_co_data, county, state)
        state_daily_death_graph(st_co_data, county, state)
        
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        data['date'] = pd.to_datetime(data.date, format='%m/%d/%y')
        date_to_filter = st.date_input('Check for date', yesterday)
        map_st_co_data = filtered_by_state(map_coordinates, county, state)
        us_map(map_st_co_data, state, county, date_to_filter)
    else:
        st.write('This combination does not work.')

elif nav_bar == "Comparing States":
    st.header('Comparing States')

    state_key = get_state(data)
    state_key = insert(state_key, 0, "All")
    st.sidebar.header(f'Choose your state below:')
    first_state = st.sidebar.selectbox('Select a state ', state_key, key='1')
    second_state = st.sidebar.selectbox('Select a second state ', state_key, key='2')

    
    # st_co_data = filtered_two_state(data, first_state, second_state)

    # if not st_co_data.empty:
    #     compare_state_confirmed_graph(st_co_data, first_state)

    # else:
    #     st.write('This combination does not work.')
    
