import os

import dotenv
import pathlib

from src.data import (
    build_stations_dataframe,
    get_k_closest_stations,
    load_json_files,
    find_json_files_in_directory,
)

dotenv.load_dotenv()

DATA_RAW_PATH = pathlib.Path(os.getenv("DATA_RAW_PATH"))
DATA_PROCESSED_PATH = pathlib.Path(os.getenv("DATA_PROCESSED_PATH"))
NUM_NEIGHBOR_STATIONS = int(os.getenv("NUM_NEIGHBOR_STATIONS"))


def main():
    raw_data = get_raw_data()
    stations = build_stations_dataframe()
    stations = get_k_closest_stations(stations, k=5)

    stations.to_csv("data/processed/stations.csv", index=False)


def get_raw_data() -> list[dict]:
    data_files = find_json_files_in_directory(DATA_RAW_PATH)
    data_files = sorted(data_files, key=lambda x: int(remove_extension(x)))
    raw_data = load_json_files(DATA_RAW_PATH, data_files)
    return raw_data


def remove_extension(filename: str) -> str:
    return filename.split(".")[0]


if __name__ == "__main__":
    main()
