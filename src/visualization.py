"""Contains functions for visualizing time series data."""
from pathlib import Path
from warnings import simplefilter

import numpy as np
import pandas as pd
import folium
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns
from statsmodels.graphics import tsaplots


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


def plot_windows(cv, y, title=""):
    """Plot training and test windows.

    Function obtained from:
    https://github.com/sktime/sktime-tutorial-pydata-global-2021/blob/main/notebooks/utils.py

    Parameters
    ----------
    y : pd.Series
        Time series to split
    cv : temporal cross-validation iterator object
        Temporal cross-validation iterator
    title : str
        Plot title
    """

    simplefilter("ignore", category=UserWarning)

    train_windows, test_windows = _get_windows(cv, y)

    def get_y(length, split):
        # Create a constant vector based on the split for y-axis."""
        return np.ones(length) * split

    n_splits = len(train_windows)
    n_timepoints = len(y)
    len_test = len(test_windows[0])

    train_color, test_color = sns.color_palette("colorblind")[:2]

    fig, ax = plt.subplots(figsize=plt.figaspect(0.3))

    for i in range(n_splits):
        train = train_windows[i]
        test = test_windows[i]

        ax.plot(
            np.arange(n_timepoints),
            get_y(n_timepoints, i),
            marker="o",
            c="lightgray",
        )
        ax.plot(
            train,
            get_y(len(train), i),
            marker="o",
            c=train_color,
            label="Window",
        )
        ax.plot(
            test,
            get_y(len_test, i),
            marker="o",
            c=test_color,
            label="Forecasting horizon",
        )
    ax.invert_yaxis()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set(
        title=title,
        ylabel="Window number",
        xlabel="Time",
        xticklabels=y.index,
    )
    # remove duplicate labels/handles
    handles, labels = [(leg[:2]) for leg in ax.get_legend_handles_labels()]
    ax.legend(handles, labels)


def plot_acf(
    series: pd.Series,
    lags: int,
    title: str = "Función de Autocorrelación",
    figsize: tuple[int, int] = (12, 6),
    use_grid: bool = False,
    add_day_vertical_lines: bool = False,
):
    _plot_auto_correlation(
        tsaplots.plot_acf,
        series,
        lags,
        title,
        figsize,
        use_grid,
        add_day_vertical_lines,
    )


def plot_pacf(
    series: pd.Series,
    lags: int,
    title: str = "Función de Autocorrelación Parcial",
    figsize: tuple[int, int] = (12, 6),
    use_grid: bool = False,
    add_day_vertical_lines: bool = False,
):
    _plot_auto_correlation(
        tsaplots.plot_pacf,
        series,
        lags,
        title,
        figsize,
        use_grid,
        add_day_vertical_lines,
    )


def _plot_auto_correlation(
    autocorrelation_function,
    series,
    lags,
    title,
    figsize,
    use_grid,
    add_day_vertical_lines,
):
    plt.figure(figsize=figsize)
    autocorrelation_function(series, ax=plt.gca(), lags=lags, title=title)
    plt.grid(use_grid)
    if add_day_vertical_lines:
        _add_day_vertical_lines(n_days=lags // 24)
    plt.xlabel("Lags (horas)")
    plt.tight_layout()


def _add_day_vertical_lines(n_days: int):
    for i in range(1, n_days + 1):
        plt.axvline(x=24 * i, color="black", linestyle="--", alpha=0.5)
        plural = "s" if i > 1 else ""
        plt.text(
            24 * i + 1,
            0.95,
            f"{i} día{plural}",
            fontsize=8,
            color="black",
        )


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


def _get_coordinates(
    stations: pd.DataFrame, station_id: int
) -> tuple[float, float]:
    return (
        stations.loc[station_id, "latitude"],
        stations.loc[station_id, "longitude"],
    )


def _get_windows(cv, y):
    """Generate windows"""
    train_windows = []
    test_windows = []
    for train, test in cv.split(y):
        train_windows.append(train)
        test_windows.append(test)
    return train_windows, test_windows


def load_benzene_concentration_sample():
    """Load sample of benzene concentration dataset [1].

    Missing values have been imputed using the mean value.

    Returns
    -------
    X : np.ndarray
        Feature time series data.
    y : np.ndarray
        Target data.

    References
    ----------
    .. [1] https://zenodo.org/record/3902673#.YXqxNy8w3UI
    """
    file = (
        Path(__file__).parent.parent / "data/benzene_concentration_sample.csv"
    )
    df = pd.read_csv(file)
    y = df["target"].to_numpy()
    X = df.drop(columns="target").to_numpy()
    X = np.expand_dims(X, axis=1)
    return X, y
