.PHONY: build_csv_data resample_data add_exogenuous

build_csv_data: data/processed/stations_metadata.csv \
data/processed/stations_timeseries.csv

data/processed/stations_metadata.csv \
data/processed/stations_timeseries.csv: scripts/build_csv_data.py
	python scripts/build_csv_data.py

resample_data: data/processed/stations_timeseries_resampled.csv

data/processed/stations_timeseries_resampled.csv: data/processed/stations_metadata.csv \
data/processed/stations_timeseries.csv
	python scripts/resample_data.py

add_exogenuous: data/processed/stations_timeseries_with_exog.csv

data/processed/stations_timeseries_with_exog.csv: data/processed/stations_timeseries_resampled.csv
	python scripts/add_exogenuous.py