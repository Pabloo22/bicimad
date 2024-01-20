import os

import dotenv
import pathlib

from src.data import (
    build_stations_dataframe,
    get_k_closest_stations,
    load_json_data_in_date_range,
    build_dock_bikes_timeseries_dataframe,
)

dotenv.load_dotenv()

DATA_RAW_PATH = pathlib.Path(os.getenv("RAW_DATA_PATH"))
DATA_PROCESSED_PATH = pathlib.Path(os.getenv("PROCESSED_DATA_PATH"))
NUM_NEIGHBOR_STATIONS = int(os.getenv("NUM_NEIGHBOR_STATIONS"))
TARGET_STATION_ID = int(os.getenv("TARGET_STATION_ID"))


def main():
    raw_data = load_json_data_in_date_range(DATA_RAW_PATH)
    stations = build_stations_dataframe(raw_data)
    neighbor_selected_stations = get_k_closest_stations(
        target_station_id=TARGET_STATION_ID,
        stations=stations,
        k=NUM_NEIGHBOR_STATIONS,
    )
    selected_stations_ids = [TARGET_STATION_ID]
    selected_stations_ids.extend(neighbor_selected_stations.index.to_list())
    dock_bikes_timeseries = build_dock_bikes_timeseries_dataframe(
        data=raw_data,
        station_ids=selected_stations_ids,
    )
    stations.to_csv(DATA_PROCESSED_PATH / "stations_metadata.csv")
    dock_bikes_timeseries.to_csv(
        DATA_PROCESSED_PATH / "stations_timeseries.csv"
    )


if __name__ == "__main__":
    main()
