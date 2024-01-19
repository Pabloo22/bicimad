from typing import NamedTuple
import pathlib
import os

import dotenv


class Config(NamedTuple):
    raw_data_path: pathlib.Path
    processed_data_path: pathlib.Path
    num_neighbor_stations: int
    target_station_id: int


def get_config() -> Config:
    dotenv.load_dotenv()

    RAW_DATA_PATH = pathlib.Path(os.getenv("RAW_DATA_PATH"))
    PROCESSED_DATA_PATH = pathlib.Path(os.getenv("PROCESSED_DATA_PATH"))
    NUM_NEIGHBOR_STATIONS = int(os.getenv("NUM_NEIGHBOR_STATIONS"))
    TARGET_STATION_ID = int(os.getenv("TARGET_STATION_ID"))

    return Config(
        RAW_DATA_PATH,
        PROCESSED_DATA_PATH,
        NUM_NEIGHBOR_STATIONS,
        TARGET_STATION_ID,
    )
