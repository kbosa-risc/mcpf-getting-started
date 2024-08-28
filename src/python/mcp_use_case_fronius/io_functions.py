import pandas as pd
from typing import Any
import os
import mcp_frm.pipeline_routines as routines
import mcp_general_functions.constants as constants
import tarfile
import pyarrow.parquet as pq
import pyarrow as pa
import math


def check_sample_rate_quantile(df: pd.DataFrame, time_column: str = "timestamp"):
    quantile = 0.95
    # Ensure the df is sorted by the timestamp column
    df = df.sort_values(by=time_column)

    # Calculate the time difference between consecutive timestamps
    time_diff = df[time_column].diff()

    # Calculate the quantile of time differences
    quantile_value = time_diff.quantile(quantile)

    return quantile_value


def unzip_all(data: dict[str, Any]) -> dict[str, Any]:
    meta = routines.get_meta_data(data)
    input_dir = routines.get_current_input_dir(meta)
    output_dir = routines.get_current_tmp_dir(meta)

    if len(os.listdir(input_dir)) != 0:
        for file in os.listdir(input_dir):
            tar = tarfile.open(os.path.join(input_dir, file), "r:gz")

            # Extract all files to the current directory
            tar.extractall(output_dir)

            # Close the tar file
            tar.close()

    dirs_of_input_files = list(map(lambda x: os.path.join(output_dir, x), os.listdir(output_dir)))
    routines.register_loop_iterator_list(dirs_of_input_files)
    # routines.set_current_output_dir_to_input_dir(meta)
    routines.set_meta_in_data(data, meta)
    return data


def determine_end_date_from_filename(data: dict[str, Any]) -> dict[str, Any]:
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)
    if not iterator:
        iterator = data[constants.DEFAULT_IO_DATA_LABEL]
    else:
        data[constants.DEFAULT_IO_DATA_LABEL] = iterator
    meta['current_folder'] = iterator[iterator.find("Archive"):].replace(".tar.gz", "")
    input_dir = os.path.join(routines.get_current_tmp_dir(meta), meta['current_folder'])
    date_str = meta['current_folder'].replace("Archive_", "").replace("-csv", "").replace("-parquet", "")
    meta['end_date'] = date_str
    data['sample_rate_dict'] = {"name": [], "df": [], "srate": []}
    files = os.listdir(input_dir)
    routines.register_loop_iterator_list(files)
    routines.set_meta_in_data(data, meta)
    return data


def determine_end_date_from_filename_v2(data: dict[str, Any]) -> dict[str, Any]:
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)
    if not iterator:
        iterator = data[constants.DEFAULT_IO_DATA_LABEL]
    else:
        data[constants.DEFAULT_IO_DATA_LABEL] = iterator
    meta['current_folder'] = iterator[iterator.find("Archive"):].replace(".tar.gz", "")
    input_dir = os.path.join(routines.get_current_tmp_dir(meta), meta['current_folder'])
    date_str = meta['current_folder'].replace("Archive_", "").replace("-csv", "").replace("-parquet", "")
    meta['end_date'] = date_str
    data['sample_rate_dict'] = {"name": [], "df": [], "srate": []}

    data['input_dir'] = input_dir
    routines.set_meta_in_data(data, meta)
    return data

def determine_output_filename(data: dict[str, Any]) -> dict[str, Any]:
    meta = routines.get_meta_data(data)
    meta['output_file_name'] = meta['current_folder'].replace("-csv", "").replace("-parquet", "") + ".parquet"
    routines.set_meta_in_data(data, meta)
    return data


def read_parquet_file(data: dict[str, Any]) -> dict[str, Any]:
    file = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)

    tmp_path = os.path.join(routines.get_current_tmp_dir(meta), meta['current_folder'])

    if file.__contains__(".parquet"):
        table = pq.read_table(tmp_path + '/' + file)
        df = table.to_pandas()
        if file.__contains__("10khz"):
            cutTailSize = 0
            while df["time"].iloc[cutTailSize - 1] != math.floor(df["time"].iloc[cutTailSize - 1] * 1000) / 1000:
                cutTailSize -= 1
            if cutTailSize < 0:
                df = df.iloc[:cutTailSize]

        df_timestamp = pd.DataFrame()
        for nr, column_name in enumerate(df.columns):
            if nr == 0:
                df_timestamp[column_name] = df[column_name].astype("float64")
            else:
                temp_df = df_timestamp.copy()
                temp_df[column_name] = df[column_name]
                data['sample_rate_dict']["name"].append(column_name)
                data['sample_rate_dict']["df"].append(temp_df)
                data['sample_rate_dict']["srate"].append(check_sample_rate_quantile(temp_df, "time"))

    routines.set_meta_in_data(data, meta)
    return data


def read_csv_file(data: dict[str, Any]) -> dict[str, Any]:
    file = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)
    input_dir = os.path.join(routines.get_current_tmp_dir(meta), meta['current_folder'])

    if file.__contains__(".csv"):
        filename = file.replace(".csv", "")
        temp_df = pd.read_csv(os.path.join(input_dir, file), usecols=["time", "value"], delimiter=";")
        temp_df = temp_df.rename(columns={"value": filename})
        data['sample_rate_dict']["name"].append(filename)
        data['sample_rate_dict']["df"].append(temp_df)
        data['sample_rate_dict']["srate"].append(check_sample_rate_quantile(temp_df, "time"))

    routines.set_meta_in_data(data, meta)
    return data


def write_to_parquet(data: dict[str, Any]) -> dict[str, Any]:
    meta = routines.get_meta_data(data)
    output_dir = routines.get_final_output_dir(meta)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    pq.write_table(pa.Table.from_pandas(data['main_df']), os.path.join(output_dir, meta['output_file_name']))

    routines.set_meta_in_data(data, meta)
    return data


def print_all(data: dict[str, Any]) -> dict[str, Any]:
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)
    input_dir = routines.get_current_input_dir(meta)
    for file in os.listdir(iterator):
        print(file)
    routines.set_meta_in_data(data, meta)
    return data

