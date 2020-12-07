import pandas as pd
import numpy as numpy
import streamlit as st
import get_csv

def get_state(df):
    return sorted(df.state.unique())

def get_second_state(df):
    return sorted(df.state.unique())

def get_county(df, state):
    return df[df.state == state].county.unique()

def filtered_by_state(df, county, state):
    if (county == 'All') & (state == 'All'):
        return df
    elif county != 'All':
        return df[df.county == county]
    elif state != 'All':
        return df[df.state == state]
    else:
        return df[(df.state == st) & (df.county == county)]
        
def filtered_two_state(df, state, second_state):
    if (state == 'All') & (second_state == 'All'):
        return df
    elif state != 'All':
        return df[df.state == state]
    elif second_state != 'All':
        return df[df.state == second_state]
    else:
        return df[(df.state == state) & (df.state == second_state)]


