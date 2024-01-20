.PHONY: build_csv_data resample_data

build_csv_data: data/processed/stations_metadata.csv \
data/processed/stations_timeseries.csv

data/processed/stations_metadata.csv \
data/processed/stations_timeseries.csv: scripts/build_csv_data.py
	python scripts/build_csv_data.py

resample_data: data/processed/stations_timeseries_resampled.csv

data/processed/stations_timeseries_resampled.csv: data/processed/stations_metadata.csv \
data/processed/stations_timeseries.csv
	python scripts/resample_data.py
