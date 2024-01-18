import pandas as pd
from geopy.distance import geodesic

KEEP_COLS = [
    "id",
    "name",
    "number",
    "address",
    "latitude",
    "longitude",
    "total_bases",
]


def build_stations_dataframe(raw_data: list[dict]) -> pd.DataFrame:
    already_in = []
    stations = pd.DataFrame()
    for data in raw_data:
        for station in data["stations"]:
            if station["id"] in already_in:
                continue
            stations = pd.concat(
                [
                    stations,
                    pd.DataFrame(station, index=[0], columns=KEEP_COLS),
                ],
                ignore_index=True,
            )
            already_in.append(station["id"])

    stations.set_index("id", inplace=True)
    return stations


def get_k_closest_stations(
    target_station_id: int, stations: pd.DataFrame, k: int
) -> pd.DataFrame:
    stations_copy = stations.copy(deep=True)
    target_station = stations_copy.loc[target_station_id]
    stations_copy.drop(target_station_id, inplace=True)
    stations_copy["distance"] = stations_copy.apply(
        _calculate_distance, axis=1, args=(target_station,)
    )
    stations_copy.sort_values(by="distance", inplace=True)
    return stations_copy.iloc[:k]


def _calculate_distance(row, target_station):
    return geodesic(
        (row["latitude"], row["longitude"]),
        (target_station["latitude"], target_station["longitude"]),
    ).km


def build_dock_bikes_timeseries_dataframe(
    data: list[dict], station_ids: list[int]
) -> pd.DataFrame:
    data_list = {id_: [] for id_ in station_ids}
    data_list["timestamps"] = []

    for d in data:
        date = pd.to_datetime(d["_id"])
        data_list["timestamps"].append(date)
        for station in d["stations"]:
            if station["id"] in station_ids:
                data_list[station["id"]].append(station["dock_bikes"])
    
    stations_timeseries = pd.DataFrame(data_list)
    stations_timeseries.set_index("timestamps", inplace=True)
    return stations_timeseries
