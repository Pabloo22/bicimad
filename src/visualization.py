"""Contains functions for visualizing time series data."""
import pandas as pd
import folium

RED_ICON = {"color": "red", "icon": "fa-bicycle", "prefix": "fa"}
BLUE_ICON = {"color": "blue", "icon": "fa-bicycle", "prefix": "fa"}


def plot_stations_in_map(
    stations: pd.DataFrame,
    target_station_id: str,
    other_stations_ids: list[str],
) -> folium.Map:
    m = folium.Map(location=_get_coordinates(stations, target_station_id))

    folium.Marker(
        location=_get_coordinates(stations, target_station_id),
        popup=stations.loc[target_station_id, "name"],
        icon=folium.Icon(**BLUE_ICON),
    ).add_to(m)

    for other_station_id in other_stations_ids:
        folium.Marker(
            location=_get_coordinates(stations, other_station_id),
            popup=stations.loc[other_station_id, "name"],
            icon=folium.Icon(**RED_ICON),
        ).add_to(m)

    m.fit_bounds(m.get_bounds())

    return m


def _get_coordinates(
    stations: pd.DataFrame, station_id: int
) -> tuple[float, float]:
    return (
        stations.loc[station_id, "latitude"],
        stations.loc[station_id, "longitude"],
    )
