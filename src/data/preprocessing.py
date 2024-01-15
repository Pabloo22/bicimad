import pandas as pd


def build_stations_dataframe(raw_data: pd.DataFrame):
    raise NotImplementedError


def get_k_closest_stations(
    target_station_name: str, stations: pd.DataFrame, k: int
) -> pd.DataFrame:
    raise NotImplementedError


def build_dock_bikes_timeseries_dataframe(
    data: pd.DataFrame, station_names: list[str]
) -> pd.DataFrame:
    raise NotImplementedError
