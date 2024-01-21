import pandas as pd

from src.config import get_config
from src.data import get_weather_data, get_holidays


def main():
    config = get_config()
    dock_bikes_timeseries = pd.read_csv(
        config.processed_data_path / "stations_timeseries_resampled.csv",
        index_col=0,
        parse_dates=True,
    )

    stations_metadata = pd.read_csv(
        config.processed_data_path / "stations_metadata.csv"
    )

    start_date = dock_bikes_timeseries.index.min() - pd.Timedelta("1D")
    end_date = dock_bikes_timeseries.index.max() + pd.Timedelta("1D")

    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    target_station = stations_metadata.loc[
        stations_metadata["id"] == config.target_station_id
    ]

    weather = get_weather_data(
        target_station.latitude.values[0],
        target_station.longitude.values[0],
        start_date,
        end_date,
    )

    holidays_raw = pd.read_csv(
        config.raw_data_path / "calendario.csv",
        sep=";",
        parse_dates=True,
        index_col="Dia",
        dayfirst=True,
    )

    holidays = get_holidays(
        start_date,
        end_date,
        holidays_raw,
    )

    dock_bikes_with_exogenous = dock_bikes_timeseries.merge(
        weather,
        how="left",
        left_index=True,
        right_index=True,
    )
    dock_bikes_with_exogenous = dock_bikes_with_exogenous.merge(
        holidays,
        how="left",
        left_index=True,
        right_index=True,
    )

    dock_bikes_with_exogenous.to_csv(
        config.processed_data_path
        / "stations_timeseries_resampled_with_exogenous.csv"
    )


if __name__ == "__main__":
    main()
