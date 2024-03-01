"""Functions for pandas DataFrame column operations"""

import pandas as pd


def rename_cols(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """Wrapper of df.rename() to be used inside df.pipe()"""
    return df.rename(**kwargs)


def split_timestamp_ymd(df: pd.DataFrame) -> pd.DataFrame:
    """split timestamp column into year, month, day columns"""
    df["timestamp"] = df["timestamp"].astype("str")
    df["year"] = df["timestamp"].str.slice(start=0, stop=4).astype("int32")
    df["month"] = df["timestamp"].str.slice(start=5, stop=7).astype("int32")
    df["day"] = df["timestamp"].str.slice(start=8).astype("int32")
    return df


def split_timestamp_ym(df: pd.DataFrame) -> pd.DataFrame:
    """split timestamp column into year, month columns"""
    df["timestamp"] = df["timestamp"].astype("str")
    if df["timestamp"].str.contains("-").any():
        df["year"] = df["timestamp"].str.slice(start=0, stop=4).astype("int32")
        df["month"] = df["timestamp"].str.slice(start=5, stop=7).astype("int32")
    else:
        df["year"] = df["timestamp"].str.slice(start=0, stop=4).astype("int32")
        df["month"] = df["timestamp"].str.slice(start=4, stop=6).astype("int32")
    return df
