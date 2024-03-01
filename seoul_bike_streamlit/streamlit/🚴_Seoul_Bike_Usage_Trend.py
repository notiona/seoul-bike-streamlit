"""Seoul Bike Usage Trend streamlit page"""
# pylint:disable=invalid-name, non-ascii-file-name
import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly_calplot import calplot
import streamlit as st

from seoul_bike_streamlit.paths import AGG_DAILY_USAGE_PATH

st.set_page_config(
    page_title="Seoul Bike Data Usage Trend",
    page_icon="🚴‍♂️",
)

st.header("🚴‍♂ Seoul Bike Data Usage Trend Visualization")

# Data Acquisition
agg_daily_usage_df = pd.read_parquet(Path(AGG_DAILY_USAGE_PATH) / "agg_daily_usage.parq")

st.write("### Daily Bike Usage Trend")
agg_daily_trend_df = agg_daily_usage_df.copy()
with st.expander("See date selection note"):
    st.info("Note that start date is inclusive, and end date is exclusive.")
col1, col2 = st.columns([1, 1])
with col1:
    start_date = st.date_input("Select start date",
                               datetime.date(2022, 11, 15),
                               key="daily_trend_start")
with col2:
    end_date = st.date_input("Select end date",
                             datetime.date(2023, 11, 15),
                             key="daily_trend_end")
agg_daily_trend_df = agg_daily_trend_df.query("timestamp>=@start_date and timestamp<@end_date")
enable_ols = st.toggle("Show trend line", value=True, key="daily_trend_toggle")
px_chart = px.scatter(agg_daily_trend_df,
                      x="timestamp",
                      y="count",
                      trendline="ols" if enable_ols else None)
st.plotly_chart(px_chart)

st.write("### Daily Bike Usage Heatmap")
agg_daily_heatmap_df = agg_daily_usage_df.copy()
with st.expander("See date selection note"):
    st.info("Note that start date is inclusive, and end date is exclusive.")
col1, col2 = st.columns([1, 1])
with col1:
    start_date = st.date_input("Select start date",
                               datetime.date(2022, 1, 15),
                               key="daily_heatmap_start")
with col2:
    end_date = st.date_input("Select end date",
                             datetime.date(2023, 11, 15),
                             key="daily_heatmap_end")
agg_daily_heatmap_df = agg_daily_heatmap_df.query("timestamp>=@start_date and timestamp<@end_date")
daily_usage_cal_plot = calplot(agg_daily_heatmap_df,
                               x="timestamp",
                               y="count",
                               dark_theme=True,
                               space_between_plots=0.25,
                               month_lines=False,
                               years_title=True,
                               )
st.plotly_chart(daily_usage_cal_plot)

st.write("### Monthly Bike Usage Trend")
with st.expander("See date selection note"):
    st.info("As this is a monthly trend report, the input date field will be ignored.")
    st.info("Note that the months for both start date is inclusive, and end date is exclusive.")
col1, col2 = st.columns([1, 1])
with col1:
    start_date = st.date_input("Select start date",
                               datetime.date(2022, 11, 15),
                               key="monthly_trend_start")
with col2:
    end_date = st.date_input("Select end date",
                             datetime.date(2023, 11, 15),
                             key="monthly_trend_end")

agg_monthly_usage_df = agg_daily_usage_df.query("timestamp>=@start_date and timestamp<@end_date")
agg_monthly_usage_df = agg_monthly_usage_df[["count", "year", "month"]].groupby(
    ["year", "month"]).sum().reset_index()
agg_monthly_usage_df["timestamp"] = \
    (agg_monthly_usage_df["year"].astype("str") + "-" +
     agg_monthly_usage_df["month"].astype("str").str.zfill(2) + "-" + "01")  # for ols fitting
agg_monthly_usage_df["timestamp"] = pd.to_datetime(agg_monthly_usage_df["timestamp"])
fig = go.Figure()
fig.add_trace(px.bar(agg_monthly_usage_df,
                     x="timestamp",
                     y="count")["data"][0])
enable_ols = st.toggle("Show trend line", value=True, key="monthly_trend_toggle")
if enable_ols:
    px_chart = px.scatter(agg_monthly_usage_df,
                          x="timestamp",
                          y="count",
                          trendline="ols" if enable_ols else None)
    x_trend = px_chart["data"][1]['x']
    y_trend = px_chart["data"][1]['y']
    fig.add_trace(go.Scatter(x=x_trend, y=y_trend, mode="lines"))
fig.update_layout(showlegend=False)
st.plotly_chart(fig)
