"""preprocessor for raw data"""
import logging
from pathlib import Path
from typing import Dict

import pandas as pd
import yaml

from seoul_bike_streamlit.paths import (
    COLUMN_MAPPER_PATH,
    DAILY_DATA_USAGE_PATH,
    DAILY_RAW_DATA_PATH,
    AGG_DAILY_USAGE_PATH,
    MONTHLY_RAW_DATA_PATH,
    MONTHLY_DATA_USAGE_PATH
)
from seoul_bike_streamlit.preprocessing.column_ops import (
    rename_cols,
    split_timestamp_ymd,
    split_timestamp_ym
)

# logging stuff
logging.basicConfig(
    format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def load_yaml(path: Path) -> Dict:
    """loads yaml file as dict"""
    assert path.suffix in (".yaml", ".yml")
    with open(path, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            logger.exception(exc)
    return data


if __name__ == "__main__":
    # Clean daily_usage data
    DATA_NAME = "daily_usage"
    logger.info("Cleaning data for %s...", DATA_NAME)
    rename_mapper = load_yaml(COLUMN_MAPPER_PATH / f"{DATA_NAME}.yaml")
    logger.debug("raw data path: %s", DAILY_RAW_DATA_PATH)
    for csv_path in DAILY_RAW_DATA_PATH.rglob("*.csv"):
        logger.info("Reading raw data %s", csv_path.name)
        df = pd.read_csv(csv_path, encoding="cp949")
        df = (
            df.pipe(rename_cols, columns=rename_mapper)
            .pipe(split_timestamp_ymd)
        )
        logger.debug("df.columns after cleaning: %s", list(df.columns))
        logger.info("Data cleaning successful for data %s", csv_path.name)
        for group, df in df.groupby(["year", "month"]):
            logger.info("Saving cleaned data for group: %s", group)
            year, month = group
            df = df.reset_index(drop=True)
            df.to_parquet(DAILY_DATA_USAGE_PATH / f"{year}_{str(month).zfill(2)}.parq")

    # Clean monthly_usage data
    DATA_NAME = "monthly_usage"
    logger.info("Cleaning data for %s...", DATA_NAME)
    rename_mapper = load_yaml(COLUMN_MAPPER_PATH / f"{DATA_NAME}.yaml")
    logger.debug("raw data path: %s", MONTHLY_RAW_DATA_PATH)
    for csv_path in MONTHLY_RAW_DATA_PATH.rglob("*.csv"):
        logger.info("Reading raw data %s", csv_path.name)
        df = pd.read_csv(csv_path, encoding="cp949")
        df = (
            df.pipe(rename_cols, columns=rename_mapper)
            .pipe(split_timestamp_ym)
        )
        logger.info("df.columns after cleaning: %s", list(df.columns))
        logger.info("Data cleaning successful for data %s", csv_path.name)
        for group, df in df.groupby(["year", "month"]):
            logger.info("Saving cleaned data for group: %s", group)
            year, month = group
            df = df.reset_index(drop=True)
            df.to_parquet(MONTHLY_DATA_USAGE_PATH / f"{year}_{str(month).zfill(2)}.parq")

    # Aggregate daily usage
    logger.info("Aggregating daily usage data...")
    dfs = []
    for daily_usage_path in DAILY_DATA_USAGE_PATH.rglob("*.parq"):
        df = pd.read_parquet(daily_usage_path)
        file_name = daily_usage_path.stem
        year, month = map(int, file_name.split("_"))
        logger.info("Aggregating daily usage data for %s, %s", year, month)
        df = df[["timestamp", "day"]].groupby("day").count().reset_index()
        df = df.rename(columns={"timestamp": "count"})
        df["year"] = year
        df["month"] = month
        df["timestamp"] = (df["year"].astype("str") + "-" +
                           df["month"].astype("str").str.zfill(2) + "-" +
                           df["day"].astype("str").str.zfill(2))
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        dfs.append(df)
    agg_df = pd.concat(dfs).sort_values(by=["year", "month", "day"])
    logger.debug(agg_df)
    agg_df.to_parquet(Path(AGG_DAILY_USAGE_PATH) / "agg_daily_usage.parq")
