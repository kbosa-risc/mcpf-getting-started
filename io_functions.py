import pandas as pd
from typing import Any
import os
import constants
import pipeline_routines as routines
import tarfile


def get_current_input_dir(meta: dict[str, Any], data: dict[str, Any]) -> str:
    index_of_dirs = meta[constants.TMP_PATH_INDEX]
    if constants.ARG_KEYWORD_ITERATOR in data:
        input_dir = meta[constants.TMP_PATHS][index_of_dirs] + data.pop(constants.ARG_KEYWORD_ITERATOR)
    else:
        input_dir = meta[constants.TMP_PATHS][index_of_dirs]
    return input_dir


def get_current_output_dir(meta: dict[str, Any]) -> str:
    index_of_dirs = increment_tmp_dir_index(meta)
    output_dir = meta[constants.TMP_PATHS][index_of_dirs]
    return output_dir


def increment_tmp_dir_index(meta: dict[str, Any]) -> int:
    index_of_dirs = meta[constants.TMP_PATH_INDEX]
    if len(meta[constants.TMP_PATHS]) - 1 > index_of_dirs:
        index_of_dirs += 1
    return index_of_dirs


def unzip_all(data: dict[str, Any]) -> dict[str, Any]:
    meta = routines.get_meta_data(data)
    input_dir = get_current_input_dir(meta, data)
    output_dir = get_current_output_dir(meta)
    meta[constants.TMP_PATH_INDEX] = increment_tmp_dir_index(meta)

    if len(os.listdir(input_dir)) != 0:
        for file in os.listdir(input_dir):
            tar = tarfile.open(input_dir + file, "r:gz")

            # Extract all files to the current directory
            tar.extractall(output_dir)

            # Close the tar file
            tar.close()

    data['dirs_of_csvs'] = list(os.listdir(output_dir))
    routines.register_loop_iterator_list(data, 'dirs_of_csvs')
    routines.set_meta_in_data(data, meta)
    return data


def read_all_csv_files(data: dict[str, Any]) -> dict[str, Any]:
    meta = routines.get_meta_data(data)
    input_dir = get_current_input_dir(meta, data)
    routines.set_meta_in_data(data, meta)
    return data


def print_all(data: dict[str, Any]) -> dict[str, Any]:
    meta = routines.get_meta_data(data)
    input_dir = get_current_input_dir(meta, data)
    for file in os.listdir(input_dir):
        print(file)
    routines.set_meta_in_data(data, meta)
    return data

