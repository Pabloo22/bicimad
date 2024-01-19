"""Contains functions for visualizing time series data."""
import pandas as pd
import folium
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


RED_ICON = {"color": "red", "icon": "fa-bicycle", "prefix": "fa"}
BLUE_ICON = {"color": "blue", "icon": "fa-bicycle", "prefix": "fa"}


import pandas as pd


def plot_autocorrelation(
    data: pd.DataFrame | pd.Series, figsize=(12, 6), title_prefix=""
):
    series = _extract_series(data)

    plt.figure(figsize=figsize)

    plt.subplot(211)
    plot_acf(
        series, ax=plt.gca(), title=f"{title_prefix}Autocorrelation Function"
    )

    plt.subplot(212)
    plot_pacf(
        series,
        ax=plt.gca(),
        title=f"{title_prefix}Partial Autocorrelation Function",
    )

    plt.tight_layout()
    plt.show()


def _extract_series(data: pd.DataFrame | pd.Series) -> pd.Series:
    if isinstance(data, pd.DataFrame):
        if len(data.columns) != 1:
            raise ValueError("DataFrame must have only one column")
        series = data.iloc[:, 0]
    elif isinstance(data, pd.Series):
        series = data
    else:
        raise TypeError("Input must be a pandas Series or DataFrame")

    return series


def plot_stations_in_map(
    stations: pd.DataFrame,
    target_station_id: str,
    other_stations_ids: list[str],
) -> folium.Map:
    map_ = folium.Map(location=_get_coordinates(stations, target_station_id))

    folium.Marker(
        location=_get_coordinates(stations, target_station_id),
        popup=stations.loc[target_station_id, "name"],
        icon=folium.Icon(**BLUE_ICON),
    ).add_to(map_)

    for other_station_id in other_stations_ids:
        folium.Marker(
            location=_get_coordinates(stations, other_station_id),
            popup=stations.loc[other_station_id, "name"],
            icon=folium.Icon(**RED_ICON),
        ).add_to(map_)

    map_.fit_bounds(map_.get_bounds())

    return map_


def _get_coordinates(
    stations: pd.DataFrame, station_id: int
) -> tuple[float, float]:
    return (
        stations.loc[station_id, "latitude"],
        stations.loc[station_id, "longitude"],
    )
