'''This module contains some general written io functions for the mcp framework

The common in these functions is that they can handle all of the following:
- default input,
- arguments given in yaml configuration and
- loop iterators
'''

import mcp_frm.pipeline_routines as routines
import pandas as pd
from typing import Any
import os
import mcp_general_functions.constants as constants
import tarfile
import pyarrow.parquet as pq
import pyarrow as pa


def print_to_stdout(data: dict[str, Any]) -> dict[str, Any]:
    """
    It prints out the given content of 'data' to the standard out.

    Yaml args:
        'input':    it is a label in 'data' which identifies the input,
                    by default it is constants.DEFAULT_IO_DATA_LABEL

    Returns in data:
        'output':   it is a label in 'data' which identifies the output (the displayed text),
                    by default it is constants.DEFAULT_IO_DATA_LABEL


    """
    # general code part 2/1
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)

    # default_arguments_values
    arg = {
        'input': constants.DEFAULT_IO_DATA_LABEL,
        'output': constants.DEFAULT_IO_DATA_LABEL
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    if iterator:
        data[arg['input']] = iterator
    print(data[arg['input']])
    data[arg['output']] = data[arg['input']]
    routines.set_meta_in_data(data, meta)
    return data


def list_dir(data: dict[str, Any]) -> dict[str, Any]:
    """
        It returns the content of the given directory in a list.
        Yaml args:
            'input_path':       a string containing a directory path, which will be listed,
                                by default it is the value identified with the label
                                constants.DEFAULT_IO_DATA_LABEL (if it is a string)
            'relative_path':    a bool value, if it is 'True' the given 'input_path' is a relative path
                                by default it is 'False'
            'only_file_names_return':   a bool value, if it is 'True' the content of the given directory
                                        is returned without its path,
                                        by default it is 'False'
            'output_for_iteration':     a bool value, if it is 'True' the output (list) of the function is registered
                                        for a subsequent loop,
                                        by default it is 'False'

        Returns in data:
            'output':   it is a label in 'data' which identifies the output
                        (a list containing the content of the given directory),
                        by default it is constants.DEFAULT_IO_DATA_LABEL
        """
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
        'only_file_names_return': False,
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
            arg['input_path'] = os.path.join(routines.get_current_input_dir(meta), arg['input_path'])
        else:
            arg['input_path'] = routines.get_current_input_dir(meta)
    data[arg['output']] = []
    if os.path.isdir(arg['input_path']):
        if len(os.listdir(arg['input_path'])) != 0:
            for file in os.listdir(arg['input_path']):
                if arg['input_path'] != '.' and not arg['only_file_names_return']:
                    data[arg['output']].append(os.path.join(arg['input_path'], file))
                else:
                    data[arg['output']].append(file)
    if arg['output_for_iteration']:
        list_dir_for_loop = data[arg['output']].copy()
        routines.register_loop_iterator_list(list_dir_for_loop)
    routines.set_meta_in_data(data, meta)
    return data


def set_next_tmp_dir_as_input_dir(data: dict[str, Any]) -> dict[str, Any]:
    """
    the given input directory, output directory and temporary directories are stored in a list by the framework
    (first element: input dir, subsequent elements temp dirs and the last element is output dir).
    The function set the upcoming tmp/output dir to the default input dir
    """
    meta = routines.get_meta_data(data)
    routines.set_current_output_dir_to_input_dir(meta)
    routines.set_meta_in_data(data, meta)
    return data


def unzip(data: dict[str, Any]) -> dict[str, Any]:
    """
        It unzip the given input file/ dir.
        Yaml args:
            'input_path':       a string containing a directory path,
                                by default it is the value identified with the label
                                constants.DEFAULT_IO_DATA_LABEL (if it is a string)
            'relative_path':    a bool value, if it is 'True' the given 'input_path' is a relative path
                                by default it is 'False'
            'output_path':
            'file_name':
            'output_into_next_tmp_folder':

        Returns in data:
            'output':   it is a label in 'data' which identifies the output
                        (string describes the path to where the content of the file/dir was unzipped),
                        by default it is constants.DEFAULT_IO_DATA_LABEL
        """
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
        arg['input_path'] = os.path.join(arg['input_path'], arg['file_name'])

    if arg['relative_path']:
        arg['input_path'] = os.path.join(routines.get_current_input_dir(meta), arg['input_path'])
    if arg['output_into_next_tmp_folder']:
        arg['output_path'] = os.path.join(routines.get_current_tmp_dir(meta), arg['output_path'])

    if not os.path.exists(arg['output_path']):
        os.makedirs(arg['output_path'])

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
        arg['input_path'] = os.path.join(arg['input_path'], arg['file_name'])

    if arg['relative_path']:
        arg['input_path'] = os.path.join(routines.get_current_input_dir(meta), arg['input_path'])
    data[arg['output']] = pd.read_csv(
                                arg['input_path'],
                                sep=arg['separator'],
                                skiprows=arg['skip_rows'],
                                engine=arg['engine']
    )

    # general code part 2/2
    routines.set_meta_in_data(data, meta)
    return data


def set_default_file_name_from_data(data: dict[str, Any]) -> dict[str, Any]:
    # general code part 2/1
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)

    # default_arguments_values
    default_input = ''
    if constants.DEFAULT_IO_DATA_LABEL in data and isinstance(data[constants.DEFAULT_IO_DATA_LABEL], str):
        default_input = data.pop(constants.DEFAULT_IO_DATA_LABEL, '')
    arg = {
        'input': default_input,
        'output': constants.DEFAULT_OUTPUT_FILE,
        'extension': ''
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    if iterator:
        arg['input'] = iterator

    # specific code part
    data[arg['output']] = data[arg['input']] + arg['extension']
    return data


def read_excel_worksheets(data: dict[str, Any]) -> dict[str, Any]:
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
        'skip_rows': 0,
        'skip_worksheets': [],
        'engine': 'openpyxl'
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    if iterator:
        arg['input_path'] = iterator

    # specific code part
    if arg['file_name']:
        arg['input_path'] = os.path.join(arg['input_path'], arg['file_name'])

    if arg['relative_path']:
        arg['input_path'] = os.path.join(routines.get_current_input_dir(meta), arg['input_path'])
    xls = pd.ExcelFile(arg['input_path'], engine=arg['engine'])
    data[arg['output']] = {}
    for nr, sheet_name in enumerate(xls.sheet_names):
        if nr in arg['skip_worksheets']:
            continue
        data[arg['output']][sheet_name] = xls.parse(sheet_name, skiprows=arg['skip_rows'])

    # general code part 2/2
    routines.set_meta_in_data(data, meta)
    return data


def write_parquet(data: dict[str, Any]) -> dict[str, Any]:
    # general code part 2/1
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)

    # default_arguments_values
    default_output_path = '.'
    arg = {
        'input': constants.DEFAULT_IO_DATA_LABEL,
        'output': constants.DEFAULT_IO_DATA_LABEL,
        'output_path': default_output_path,
        'file_name': data.pop(constants.DEFAULT_OUTPUT_FILE, ''),
        'relative_path': False,
        'preserve_index': None
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    # if iterator:
    #    arg['output_path'] = iterator

    # specific code part
    if arg['file_name']:
        arg['output_path'] = os.path.join(arg['output_path'], arg['file_name'])

    if arg['relative_path']:
        arg['output_path'] = os.path.join(routines.get_current_tmp_dir(meta), arg['output_path'])

    if not os.path.exists(os.path.dirname(arg['output_path'])):
        os.makedirs(os.path.dirname(arg['output_path']))

    pq.write_table(pa.Table.from_pandas(data[arg['input']], preserve_index=arg['preserve_index']), arg['output_path'])
    if arg['input'] != arg['output']:
        data[arg['output']] = data[arg['input']]
    # general code part 2/2
    routines.set_meta_in_data(data, meta)
    return data


def write_csv(data: dict[str, Any]) -> dict[str, Any]:
    # general code part 2/1
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)

    # default_arguments_values
    default_output_path = '.'
    arg = {
        'input': constants.DEFAULT_IO_DATA_LABEL,
        'output': constants.DEFAULT_IO_DATA_LABEL,
        'output_path': default_output_path,
        'file_name': data.pop(constants.DEFAULT_OUTPUT_FILE, ''),
        'relative_path': False,
        'separator': ','
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    # if the function part of a loop
    # if iterator:
    #    arg['output_path'] = iterator

    # specific code part
    if arg['file_name']:
        arg['output_path'] = os.path.join(arg['output_path'], arg['file_name'])

    if arg['relative_path']:
        arg['output_path'] = os.path.join(routines.get_current_tmp_dir(meta), arg['output_path'])

    if not os.path.exists(os.path.dirname(arg['output_path'])):
        os.makedirs(os.path.dirname(arg['output_path']))

    data[arg['input']].to_csv(
                                arg['output_path'],
                                sep=arg['separator'],
                                index=False
    )
    if arg['input'] != arg['output']:
        data[arg['output']] = data[arg['input']]
    # general code part 2/2
    routines.set_meta_in_data(data, meta)
    return data

