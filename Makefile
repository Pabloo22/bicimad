.PHONY: preprocess_data

preprocess_data: data/processed/stations_metadata.csv \
data/processed/stations_timeseries.csv

data/processed/stations_metadata.csv \
data/processed/stations_timeseries.csv: scripts/preprocess_data.py
	python scripts/preprocess_data.py
