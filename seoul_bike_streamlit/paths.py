"""List of paths to be imported"""

from pathlib import Path

DAILY_RAW_DATA_PATH = (Path(__file__) / "../../raw_data/서울시 공공자전거 이용정보(일별)").resolve()
DAILY_DATA_USAGE_PATH = (Path(__file__) / "../../data/daily_usage/").resolve()

MONTHLY_RAW_DATA_PATH = (Path(__file__) / "../../raw_data/서울시 공공자전거 이용정보(월별)").resolve()
MONTHLY_DATA_USAGE_PATH = (Path(__file__) / "../../data/monthly_usage/").resolve()

COLUMN_MAPPER_PATH = (Path(__file__) / "../preprocessing/column_mappers").resolve()

AGG_DAILY_USAGE_PATH = (Path(__file__) / "../../data/aggregate_daily_usage/").resolve()

IMAGE_PATH = (Path(__file__) / "../../images/").resolve()

GEOJSON_PATH = (Path(__file__) /
                "../../data/geojson_data/HangJeongDong_ver20230701.geojson").resolve()
