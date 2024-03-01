## 🚴‍♂️ Seoul Bike Streamlit

Streamlit project to visualize Seoul Bike (따릉이) related open data.

The app is deployed and accessible at https://seoul-bike.streamlit.app/.

## Quick Start
If you have [poetry](https://python-poetry.org/), run:
```bash
poetry install
```

If not, run:
```bash
pip install -r requirements-pip.txt
```

To run the streamlit app locally:

```bash
streamlit run 'seoul_bike_streamlit/streamlit/🚴_Seoul_Bike_Usage_Trend.py'
```

## Preprocessing
As the raw data is large, it cannot be (and is generally not recommended) uploaded to this repository.

To reproduce the results in `data/aggregate_daily_usage/` folder which is used the app, follow the following steps.

Download raw data from these sources, and copy them as `raw_data/서울시 공공자전거 이용정보(일별)`, `raw_data/서울시 공공자전거 이용정보(월별)`, respectively.
- [서울시 공공자전거 이용정보(일별), daily bike usage data](https://data.seoul.go.kr/dataList/OA-15246/F/1/datasetView.do)
- [서울시 공공자전거 이용정보(월별), monthly bike usage data](https://data.seoul.go.kr/dataList/OA-15248/F/1/datasetView.do)

Run the following script to preprocess and clean the raw data files.

```bash
python seoul_bike_streamlit/preprocessing/preprocessor.py
```

This will populate `data/daily_usage` and `data/monthly_usage` folders with cleaned data, and `data/aggregate_daily_usage` with the aggregated daily usage data.

## Contributing
Feel free to write issues or PRs into this repository at any time.
