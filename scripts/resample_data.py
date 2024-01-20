import os

import dotenv
import pathlib
import pandas as pd

dotenv.load_dotenv()

DATA_PROCESSED_PATH = pathlib.Path(os.getenv("PROCESSED_DATA_PATH"))


def main():
    dock_bikes_timeseries = pd.read_csv(
        DATA_PROCESSED_PATH / "stations_timeseries.csv",
        index_col="timestamps",
        parse_dates=True,
    )
    dock_bikes_timeseries = dock_bikes_timeseries.resample("H").mean()
    # Interpolate missing values
    dock_bikes_timeseries.interpolate(method="linear", inplace=True)
    dock_bikes_timeseries.to_csv(
        DATA_PROCESSED_PATH / "stations_timeseries_resampled.csv"
    )


if __name__ == "__main__":
    main()
