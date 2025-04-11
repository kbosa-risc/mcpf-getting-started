from typing import Any

import duckdb
import pandas as pd

import mcp_frm.pipeline_routines as routines
from mcp_general_functions import constants, helper


def vertical_concatenation(data: dict[str, Any]) -> dict[str, Any]:
    """
            It appends its input pandas dataframe to another dataframe.
            Yaml args:
                'input':            it is a label in "data", which identifies the input data
                                    (given in terms of pandas dataframe),
                                    by default it is the value identified with the label
                                    constants.DEFAULT_IO_DATA_LABEL (if it is a string)
            'left_value':           it is a label in "data", which identifies the pandas dataframe
                                    in "data" to which the input dataframe will be appended.
            'reset_index': False

            Returns in data:
                'output':   Not implemented yet!
                            it should be  a label in 'data' which identifies the output
                            (the content of the input pandas dataframe in pandas dataframe),
                            by default it is constants.DEFAULT_IO_DATA_LABEL
    """
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)
    # default_arguments_values
    arg = {
        'input': constants.DEFAULT_IO_DATA_LABEL,
        'left_value': None,
        'reset_index': False
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    if iterator:
        arg['input'] = iterator

    if 'left_value' in arg and 'input' in arg and data[arg['input']] is not None:
        if arg['left_value'] not in data:
            data[arg['left_value']] = data[arg['input']]
        else:
            if arg['reset_index']:
                data[arg['left_value']] = (
                    pd.concat([data[arg['left_value']], data[arg['input']]], ignore_index=False).reset_index(drop=False))
            else:
                data[arg['left_value']] = (
                    pd.concat([data[arg['left_value']], data[arg['input']]], ignore_index=True))

    routines.set_meta_in_data(data, meta)
    return data


def set_default_input_from_variable(data: dict[str, Any]) -> dict[str, Any]:
    """
        It sets the value of the label constants.DEFAULT_IO_DATA_LABEL in "data"
        Yaml args:
                 'input_label': It is a label in "data", whose value will be referenced by
                 the other label constants.DEFAULT_IO_DATA_LABEL as well.
    """
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)
    # default_arguments_values
    arg = {
        'input_label': constants.DEFAULT_IO_DATA_LABEL
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    if iterator:
        arg['input_label'] = iterator

    data[constants.DEFAULT_IO_DATA_LABEL] = data[arg['input_label']]
    routines.set_meta_in_data(data, meta)
    return data


def remove_data(data: dict[str, Any]) -> dict[str, Any]:
    """
        It removes a label (with its referenced value) from "data"
        Yaml args:
                 'input':   It is a label in "data", which will be removed from "data",
                            by default it is constants.DEFAULT_IO_DATA_LABEL.
    """
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)
    # default_arguments_values
    arg = {
        'input': constants.DEFAULT_IO_DATA_LABEL
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    if iterator:
        arg['input'] = iterator
    del data[arg['input']]

    routines.set_meta_in_data(data, meta)
    return data


def interpolate_first_column(data: dict[str, Any]) -> dict[str, Any]:
    """
        Interpolates missing values in spectral response help table.

        Returns:
            pd.DataFrame: DataFrame with missing values interpolated.
    """
    # general code part 2/1
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)
    # default_arguments_values
    arg = {
        'input': constants.DEFAULT_IO_DATA_LABEL,
        'output': constants.DEFAULT_IO_DATA_LABEL,
        'step': 1
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    if iterator:
        arg['input'] = iterator
    last_real_value = 0
    input_table = data[arg['input']]
    columns = input_table.columns
    first_df_value = input_table[columns[0]].iloc[0]
    last_df_value = input_table[columns[0]].iloc[
        len(input_table) - 1
        ]

    # Create new index range
    new_index = range(first_df_value, last_df_value + 1, 5)

    # Create new DataFrame with new index
    new_spectral_response_help_table = pd.DataFrame({columns[0]: new_index})

    # Sort new DataFrame by index in descending order
    new_spectral_response_help_table = new_spectral_response_help_table.sort_values(
        by=[columns[0]], ascending=False
    )

    # Initialize list to store interpolated values
    new_values = []

    # Iterate through rows of new DataFrame
    for row in new_spectral_response_help_table[columns[0]]:
        # Check if row index is greater than 840
        if row > 840:
            new_values.append(0)
            continue

        # Lookup value in original table
        value = helper.vlookup(float(row), input_table, 1, 2)

        # If non-zero value found, append and update last real value
        if value != 0:
            new_values.append(value)
            last_real_value = value
            continue

        # If value is zero, interpolate
        next_real_value = 0
        i = 1
        while next_real_value == 0:
            next_real_value = helper.vlookup(
                float(row - i), input_table, 1, 2
            )
            i += 1
        value = ((next_real_value + (last_real_value / 1000)) / 2) * 1000
        new_values.append(value)
        last_real_value = value

    # Assign interpolated values to new DataFrame
    new_spectral_response_help_table[columns[1]] = new_values

    # Sort new DataFrame by index in ascending order
    new_spectral_response_help_table = new_spectral_response_help_table.sort_values(
        by=[columns[0]], ascending=True
    )

    data[arg['output']] = new_spectral_response_help_table
    routines.set_meta_in_data(data, meta)
    return data

def df_sql_statement(data: dict[str, Any]) -> dict[str, Any]:
    """Executes a SQL query on a given pandas DataFrame and returns the transformed DataFrame.

    This function reads a pandas DataFrame (`df`) and a SQL query (`sql_query`), applies the SQL query 
    on the DataFrame, and returns a new DataFrame containing the results of the query.

    Args:
        data (dict[str, Any]): _description_

    Returns:
        dict[str, Any]: _description_
    """
    # general code part 2/1
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)
    # default_arguments_values
    arg = {
        'input': constants.DEFAULT_IO_DATA_LABEL,
        'output': constants.DEFAULT_IO_DATA_LABEL,
        'SQL_STMT': ''
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    if iterator:
        arg['input'] = iterator

    # create DuckDB connection
    conn = duckdb.connect(database=':memory:')
    conn.register('data', data[arg['input']])

    df = conn.execute(arg['SQL_STMT']).fetchdf()

    data[arg['output']] = df
    routines.set_meta_in_data(data, meta)
    return data