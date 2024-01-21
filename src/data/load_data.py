import os
import json
import pandas as pd
import requests_cache
from retry_requests import retry
import openmeteo_requests

PathLike = os.PathLike | str | bytes


def load_train_test(
    path: PathLike,
    train_filename: str = "train.csv",
    test_filename: str = "test.csv",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    train = pd.read_csv(
        os.path.join(path, train_filename),
        index_col=0,
        parse_dates=True,
    )
    test = pd.read_csv(
        os.path.join(path, test_filename),
        index_col=0,
        parse_dates=True,
    )
    return train, test


def load_stations_time_series(path: PathLike) -> pd.DataFrame:
    dock_bikes_timeseries = pd.read_csv(
        path,
        index_col="timestamps",
        parse_dates=True,
    )
    dock_bikes_timeseries.columns.astype(str)

    return dock_bikes_timeseries


def load_holidays_calendar(path: PathLike) -> pd.DataFrame:
    holidays = pd.read_csv(
        path,
        sep=";",
        parse_dates=True,
        index_col="Dia",
        dayfirst=True,
    )

    holidays.drop(holidays.columns[-2:], inplace=True, axis=1)
    return holidays


def load_json_data_in_date_range(
    data_path: PathLike, start_date: str = "2022-01", end_date: str = "2022-12"
) -> list[dict]:
    data_files = find_json_files_in_directory(data_path)
    data_files = sorted(data_files, key=lambda x: int(remove_extension(x)))
    data_files = filter(
        lambda x: is_file_in_date_range(x, start_date, end_date), data_files
    )
    raw_data = load_json_files(data_path, data_files)
    return raw_data


def find_json_files_in_directory(directory: PathLike) -> list[str]:
    files = []
    for file in os.listdir(directory):
        if file.endswith(".json"):
            files.append(file)
    return files


def load_json_files(
    directory: PathLike, json_files: list[str], encoding="utf-8"
) -> list[dict]:
    json_objects = []
    for file in json_files:
        file_path = os.path.join(directory, file)
        json_objects.extend(load_json_objects(file_path, encoding))
    return json_objects


def load_json_objects(file_path, encoding="utf-8") -> list[dict]:
    with open(file_path, "r", encoding=encoding) as file:
        for line in file:
            yield json.loads(line)


def is_file_in_date_range(
    filename: str, start_date: str = "2022-01", end_date: str = "2022-12"
) -> bool:
    start_date = pd.to_datetime(start_date, format="%Y-%m")
    end_date = pd.to_datetime(end_date, format="%Y-%m")
    date = pd.to_datetime(remove_extension(filename), format="%Y%m")
    return date >= start_date and date <= end_date


def remove_extension(filename: str) -> str:
    return filename.split(".")[0]


def load_json_files_per_month(
    directory: PathLike, start_date: str, end_date: str, encoding="utf-8"
) -> list[dict]:
    """Deprecated: Use get_raw_data instead"""
    start_date = pd.to_datetime(start_date, format="%Y%m")
    end_date = pd.to_datetime(end_date, format="%Y%m")
    json_objects = []
    files = find_json_files_in_directory(directory)
    for file in files:
        file_path = os.path.join(directory, file)
        date = pd.to_datetime(file.split(".")[0], format="%Y%m")
        if date >= start_date and date <= end_date:
            json_objects.extend(load_json_objects(file_path, encoding))
    return json_objects


def get_weather_data(
    latitude: float,
    longitude: float,
    start_date: str = "2022-01-01",
    end_date: str = "2022-12-31",
) -> pd.DataFrame:
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(".cache", expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them
    # correctly below
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "precipitation",
        "timezone": "Europe/Berlin",
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]
    # Process hourly data. The order of variables needs to be the same as 
    # requested.
    hourly = response.Hourly()
    hourly_precipitation = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s"),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )
    }
    hourly_data["precipitation"] = hourly_precipitation

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    hourly_dataframe.set_index("date", inplace=True)

    return hourly_dataframe
