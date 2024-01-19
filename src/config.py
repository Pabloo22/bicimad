from typing import NamedTuple
import pathlib
import os

import dotenv


class Config(NamedTuple):
    RAW_DATA_PATH: pathlib.Path
    PROCESSED_DATA_PATH: pathlib.Path
    NUM_NEIGHBOR_STATIONS: int
    TARGET_STATION_ID: int


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
