import mcp_frm.pipeline_routines as routines
import pandas as pd
from typing import Any

import os
import mcp_general_functions.constants as constants
import tarfile


def list_dir(data: dict[str, Any]) -> dict[str, Any]:
    # general code part 2/1
    iterator = routines.pop_loop_iterator(data)
    meta = routines.get_meta_data(data)
    # default_arguments_values
    arg = {
        'output': constants.DEFAULT_IO_DATA_LABEL,
        'input_path': '.',
        'relative_path': False,
        'output_for_iteration': False
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    if iterator:
        arg['input_path'] = iterator

    # specific code part
    if arg['relative_path']:
        arg['input_path'] = routines.get_current_input_dir(meta) + '\\' + arg['input_path'] + '\\'
    data[arg['output']] = []
    if len(os.listdir(arg['input_path'])) != 0:
        for file in os.listdir(arg['input_path']):
            data[arg['output']].append(file)
    if arg['output_for_iteration']:
        data['list_dir_for_loop'] = data[arg['output']].copy()
        routines.register_loop_iterator_list(data, 'list_dir_for_loop')
    routines.set_meta_in_data(data, meta)
    return data


def set_next_tmp_dir_as_input_dir(data: dict[str, Any]) -> dict[str, Any]:
    meta = routines.get_meta_data(data)
    routines.set_current_output_dir_to_input_dir(meta)
    routines.set_meta_in_data(data, meta)
    return data


def unzip(data: dict[str, Any]) -> dict[str, Any]:
    iterator = routines.pop_loop_iterator(data)
    meta = routines.get_meta_data(data)
    # default_arguments_values
    arg = {
        'input_path': '.',
        'output_path': '.',
        'output': constants.DEFAULT_IO_DATA_LABEL,
        'file_name': '',
        'relative_path': False,
        'output_for_iteration': False,
        'output_into_next_tmp_folder': True
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    if iterator:
        arg['file_name'] = iterator

    # specific code part
    if arg['file_name']:
        data[arg['output']] = arg['file_name'].replace(".tar.gz", "")
        if arg['relative_path']:
            arg['input_path'] = routines.get_current_input_dir(meta) + '\\' + arg['input_path'] + '\\' + arg['file_name']
            if arg['output_into_next_tmp_folder']:
                arg['output_path'] = routines.get_current_tmp_dir(meta) + '\\' + arg['output_path'] + '\\'
            else:
                arg['output_path'] = routines.get_current_input_dir(meta) + '\\' + arg['output_path'] + '\\'

        tar = tarfile.open(arg['input_path'], "r:gz")
        # t_info = tar.getmembers()
        # Extract all files to the current directory
        tar.extractall(arg['output_path'])

        # Close the tar file
        tar.close()

        if arg['output_for_iteration']:
            data['unzipped_files_for_loop'] = list(os.listdir(arg['output_path']))
            routines.register_loop_iterator_list(data, 'unzipped_files_for_loop')
    routines.set_meta_in_data(data, meta)
    return data


def read_csv(data: dict[str, Any]) -> dict[str, Any]:
    # general code part 2/1
    iterator = routines.pop_loop_iterator(data)
    meta = routines.get_meta_data(data)
    # default_arguments_values
    arg = {
        'output': constants.DEFAULT_IO_DATA_LABEL,
        'input_path': '.',
        'file_name': '',
        'relative_path': False,
        'separator': ',',
        'skip_rows': 0,
        'engine': 'c'
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    if iterator:
        arg['file_name'] = iterator

    # specific code part
    if arg['file_name']:
        if arg['relative_path']:
            arg['input_path'] = routines.get_current_input_dir(meta) + '\\' + arg['input_path'] + '\\' + arg['file_name']
        data[arg['output']] = pd.read_csv(
                                    arg['input_path'],
                                    sep=arg['separator'],
                                    skiprows=arg['skip_rows'],
                                    engine=arg['engine']
        )

    # general code part 2/2
    routines.set_meta_in_data(data, meta)
    return data
