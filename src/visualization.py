"""Contains functions for visualizing time series data."""
import pandas as pd
import folium
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


RED_ICON = {"color": "red", "icon": "fa-bicycle", "prefix": "fa"}
BLUE_ICON = {"color": "blue", "icon": "fa-bicycle", "prefix": "fa"}
MONTH_NAMES = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]
SEASONAL_COLORS = {
    1: "lightblue",  # January (Winter)
    2: "deepskyblue",  # February (Winter)
    3: "lightgreen",  # March (Spring)
    4: "mediumseagreen",  # April (Spring)
    5: "greenyellow",  # May (Spring)
    6: "gold",  # June (Summer)
    7: "darkorange",  # July (Summer)
    8: "orangered",  # August (Summer)
    9: "sienna",  # September (Autumn)
    10: "peru",  # October (Autumn)
    11: "goldenrod",  # November (Autumn)
    12: "royalblue",  # December (Winter)
}


def plot_mean_values_by_hour_for_each_month(
    series: pd.Series | pd.DataFrame,
    figsize=(12, 6),
    title="Valores promedio por hora para cada mes",
    xlabel="Hora",
    ylabel="Bicicletas ancladas",
):
    series = _extract_series(series)

    monthly_hourly_means = series.groupby(
        [series.index.month, series.index.hour]
    ).mean()

    plt.figure(figsize=figsize)

    months = monthly_hourly_means.index.get_level_values(0).unique()

    for month in months:
        monthly_data = monthly_hourly_means.xs(month, level=0)
        plt.plot(
            monthly_data.index,
            monthly_data.values,
            label=MONTH_NAMES[month - 1],
            color=SEASONAL_COLORS[month],
        )
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    hours = monthly_hourly_means.index.get_level_values(1).unique()
    plt.xticks(hours, hours)
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_autocorrelation(
    data: pd.DataFrame | pd.Series,
    lags=24 * 7,
    figsize=(12, 6),
    title_prefix="",
):
    series = _extract_series(data)
    plt.figure(figsize=figsize)
    plt.subplot(211)
    plot_acf(
        series,
        ax=plt.gca(),
        lags=lags,
        title=f"{title_prefix}Función de Autocorrelación",
    )
    plt.subplot(212)
    plot_pacf(
        series,
        ax=plt.gca(),
        lags=lags,
        title=f"{title_prefix}Función de Autocorrelación Parcial",
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
