import os
import json

PathLike = os.PathLike | str | bytes


def get_raw_data(data_path: PathLike) -> list[dict]:
    data_files = find_json_files_in_directory(data_path)
    data_files = sorted(data_files, key=lambda x: int(remove_extension(x)))
    raw_data = load_json_files(data_path, data_files)
    return raw_data


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


def find_json_files_in_directory(directory: PathLike) -> list[str]:
    files = []
    for file in os.listdir(directory):
        if file.endswith(".json"):
            files.append(file)
    return files


def remove_extension(filename: str) -> str:
    return filename.split(".")[0]
