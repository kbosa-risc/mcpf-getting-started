import mcp_frm.pipeline_routines as routines
import pandas as pd
from typing import Any
from influxdb_client.client import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import mcp_general_functions.constants as constants
import tarfile


def list_dir(data: dict[str, Any]) -> dict[str, Any]:
    # general code part 2/1
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)

    # default_arguments_values
    default_input_path = '.'
    if constants.DEFAULT_IO_DATA_LABEL in data and isinstance(data[constants.DEFAULT_IO_DATA_LABEL], str):
        default_input_path = data.pop(constants.DEFAULT_IO_DATA_LABEL, '.')
    arg = {
        'output': constants.DEFAULT_IO_DATA_LABEL,
        'input_path': default_input_path,
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
        if arg['input_path'] != '.':
            arg['input_path'] = routines.get_current_input_dir(meta) + '\\' + arg['input_path']
        else:
            arg['input_path'] = routines.get_current_input_dir(meta)
    data[arg['output']] = []
    if len(os.listdir(arg['input_path'])) != 0:
        for file in os.listdir(arg['input_path']):
            if arg['input_path'] != '.':
                data[arg['output']].append(arg['input_path'] + '\\' + file)
            else:
                data[arg['output']].append(file)
    if arg['output_for_iteration']:
        list_dir_for_loop = data[arg['output']].copy()
        routines.register_loop_iterator_list(list_dir_for_loop)
    routines.set_meta_in_data(data, meta)
    return data


def set_next_tmp_dir_as_input_dir(data: dict[str, Any]) -> dict[str, Any]:
    meta = routines.get_meta_data(data)
    routines.set_current_output_dir_to_input_dir(meta)
    routines.set_meta_in_data(data, meta)
    return data


def unzip(data: dict[str, Any]) -> dict[str, Any]:
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)
    # default_arguments_values
    default_input_path = '.'
    if constants.DEFAULT_IO_DATA_LABEL in data and isinstance(data[constants.DEFAULT_IO_DATA_LABEL], str):
        default_input_path = data.pop(constants.DEFAULT_IO_DATA_LABEL, '.')
    arg = {
        'input_path': default_input_path,
        'output_path': '.',
        'output': constants.DEFAULT_IO_DATA_LABEL,
        'file_name': '',
        'relative_path': False,
        'output_into_next_tmp_folder': True
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    if iterator:
        arg['input_path'] = iterator

    # specific code part
    if arg['file_name']:
        arg['input_path'] = arg['input_path'] + '\\' + arg['file_name']

    if arg['relative_path']:
        arg['input_path'] = routines.get_current_input_dir(meta) + '\\' + arg['input_path']
    if arg['output_into_next_tmp_folder']:
        arg['output_path'] = routines.get_current_tmp_dir(meta) + '\\' + arg['output_path']

    # Extract all files to the current directory
    tar = tarfile.open(arg['input_path'], "r:gz")
    # t_info = tar.getmembers()
    tar.extractall(arg['output_path'])
    tar.close()
    data[arg['output']] = arg['output_path']
    routines.set_meta_in_data(data, meta)
    return data


def read_csv(data: dict[str, Any]) -> dict[str, Any]:
    # general code part 2/1
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)

    # default_arguments_values
    default_input_path = '.'
    if constants.DEFAULT_IO_DATA_LABEL in data and isinstance(data[constants.DEFAULT_IO_DATA_LABEL], str):
        default_input_path = data.pop(constants.DEFAULT_IO_DATA_LABEL, '.')
    arg = {
        'output': constants.DEFAULT_IO_DATA_LABEL,
        'input_path': default_input_path,
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
        arg['input_path'] = iterator

    # specific code part
    if arg['file_name']:
        arg['input_path'] = arg['input_path'] + '\\' + arg['file_name']

    if arg['relative_path']:
        arg['input_path'] = routines.get_current_input_dir(meta) + '\\' + arg['input_path']
    data[arg['output']] = pd.read_csv(
                                arg['input_path'],
                                sep=arg['separator'],
                                skiprows=arg['skip_rows'],
                                engine=arg['engine']
    )

    # general code part 2/2
    routines.set_meta_in_data(data, meta)
    return data


def influx_df_write(data: dict[str, Any]) -> dict[str, Any]:
    meta = routines.get_meta_data(data)
    db_conf = routines.get_db_config(meta, 'influx')
    # token: str = os.environ.get("INFLUXDB_TOKEN")
    arg = {
        'input': constants.DEFAULT_IO_DATA_LABEL,
        'measurement_name': ''
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    with influxdb_client.InfluxDBClient(
        url=db_conf['url'], token=arg['token'], org=db_conf['org']
    ) as influx_client:
        write_api = influx_client.write_api(write_options=SYNCHRONOUS)

        # writing entire dataframe into database.
        write_api.write(
            org=db_conf['org'],
            record=data[arg['input']],
            bucket=db_conf['bucket'],
            data_frame_measurement_name=arg['measurement_name']
        )
        # general code part 2/2
    routines.set_meta_in_data(data, meta)
    return data
