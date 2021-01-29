from simpledbf import Dbf5
import config as cfg
import pandas as pd
import streamlit as st


def get_county_key(df, state):
    return df[df.state == state].county.unique()


def get_state_key(df):
    return sorted(df.state.unique())


def get_fips():
    dbf = Dbf5(cfg.dbf)
    fips_df = dbf.to_dataframe()
    fips_df["FIPS"] = fips_df["FIPS"].astype(float)
    return fips_df.loc[:, ["FIPS", "LON", "LAT"]]


def df_left_merge(left_df, right_df):
    return left_df.merge(right_df, left_on="fips", right_on="FIPS", how="left")


def df_clean(ff):
    ff1 = ff.rename(columns={"LON": "lon", "LAT": "lat"})
    return ff1.dropna()


@st.cache
def get_coord(df):
    df1 = get_fips()
    merged_df = df_left_merge(df, df1)
    clean_df = df_clean(merged_df)
    return clean_df


@st.cache
def get_data():
    df = pd.read_csv(cfg.db)
    df["date"] = pd.to_datetime(df["date"])
    return df


def filter_data_by_county_state(df, co, st):
    if (co == "All") & (st == "All"):
        return df
    elif co == "All":
        return df[df.state == st]
    elif st == "All":
        return df[df.county == co]
    else:
        return df[(df.state == st) & (df.county == co)]
