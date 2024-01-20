from src import get_config
from src.data import read_stations_time_series


def main():
    config = get_config()
    dock_bikes_timeseries = read_stations_time_series(
        config.processed_data_path / "stations_timeseries.csv"
    )

    dock_bikes_timeseries = dock_bikes_timeseries.resample("H").mean()

    dock_bikes_timeseries["missing"] = (
        dock_bikes_timeseries[str(config.target_station_id)]
        .isnull()
        .astype(int)
    )

    dock_bikes_timeseries.interpolate(method="linear", inplace=True)
    dock_bikes_timeseries.to_csv(
        config.processed_data_path / "stations_timeseries_resampled.csv"
    )


if __name__ == "__main__":
    main()
