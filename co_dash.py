import streamlit as st
import pandas as pd
import config as cfg
from datetime import datetime, date
from numpy import insert

from func_lib import (
    get_coord,
    get_data,
    get_county_key,
    get_state_key,
    filter_data_by_county_state,
)
from graphs import (
    draw_tot_cases_graph,
    draw_tot_deaths_graph,
    draw_county_state_cases_graph,
    draw_county_state_deaths_graph,
    draw_daily_cases_graph,
    draw_daily_deaths_graph,
    draw_daily_county_state_cases_graph,
    draw_daily_county_state_deaths_graph,
)


covid_data = get_data()


st.title("Disease Dashboard")

nav_disease_link = st.sidebar.radio("Disease", ("Home", "COVID"))

# main nav
if nav_disease_link == "Home":
    nav_link = 1
    st.header(
        "Exploring Disease in the US. "
    )

elif nav_disease_link == "COVID":
    nav_link = st.sidebar.radio("Navigation", ("Home", "US Trends", "Local Trends"))
    st.header(
        "Exploring COVID-19 in the US. "
    )

elif nav_disease_link == "Zika":
    nav_link = st.sidebar.radio("Navigation", ("Home", "Graphs"))
    st.header(
        "Exploring Zika in the US. "
    )

# covid
if nav_link == "Home":
    st.header(
        "Resources:"
    )

elif nav_link == "US Trends":
    st.header("US Trends")
    draw_tot_cases_graph(covid_data)
    draw_tot_deaths_graph(covid_data)
    draw_daily_cases_graph(covid_data)
    draw_daily_deaths_graph(covid_data)

elif nav_link == "Local Trends":
    cov_coord = get_coord(covid_data)
    st.header("Local Trends")

    state_key = get_state_key(cov_coord)
    # state_key = insert(state_key, 0, "All")
    st.sidebar.header(f"Select a State Below:")
    state = st.sidebar.selectbox("Select a State ", state_key)
    st.sidebar.header(f"Select a County Below:")
    county_key = get_county_key(cov_coord, state)
    county_key = insert(county_key, 0, "All")
    county = st.sidebar.selectbox("Select a County ", county_key)

    st_co_data = filter_data_by_county_state(covid_data, county, state)

    if not st_co_data.empty:
        draw_county_state_cases_graph(st_co_data, county, state)
        draw_county_state_deaths_graph(st_co_data, county, state)
        draw_daily_county_state_cases_graph(st_co_data, county, state)
        draw_daily_county_state_deaths_graph(st_co_data, county, state)
        # date_to_filter = st.date_input(
        #     "Check for date",
        #     datetime.strptime(cfg.default_date_for_map, "%Y-%m-%d").date(),
        # )
    else:
        st.write("This combination will not work")
