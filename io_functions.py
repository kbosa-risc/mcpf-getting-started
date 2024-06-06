import pandas as pd
import json


def unzip (input_path: str, args: str) -> (str, dict[str, pd.DataFrame]):
    meta = '{output_filename = "dir"}'
    data = {"name": pd.DataFrame()}
    return (meta, data)


def read_all_csv_files(input_path: str, args: str) -> (str, dict[str, pd.DataFrame]):
    meta = '{output_filename = "dir"}'
    data = {"name": pd.DataFrame()}
    return (meta, data)


