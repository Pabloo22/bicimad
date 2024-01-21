import pandas as pd

from src import get_config


def main():
    config = get_config()

    dock_bikes_with_exogenous = pd.read_csv(
        config.processed_data_path
        / "stations_timeseries_resampled_with_exogenous.csv",
        index_col=0,
        parse_dates=True,
    )
    train = dock_bikes_with_exogenous.loc[
        dock_bikes_with_exogenous.index < config.train_test_split_date
    ]
    test = dock_bikes_with_exogenous.loc[
        dock_bikes_with_exogenous.index >= config.train_test_split_date
    ]

    train.to_csv(config.processed_data_path / "train.csv")
    test.to_csv(config.processed_data_path / "test.csv")


if __name__ == "__main__":
    main()
