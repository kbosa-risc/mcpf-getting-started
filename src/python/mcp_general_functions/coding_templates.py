import mcp_frm.pipeline_routines as routines
from mcp_general_functions import constants   # default dir
import pandas as pd
from typing import Any


def test1(data: dict[str, Any]) -> dict[str, Any]:

    # specific code part
    pass

    return data


def test2_loop_kernel(data: dict[str, Any]) -> dict[str, Any]:
    iterator = routines.pop_loop_iterator()

    # specific code part
    pass

    return data


def test3_loop_data_preparation(data: dict[str, Any]) -> dict[str, Any]:

    # specific code part
    pass

    loop_list = list(range(0,10))
    routines.register_loop_iterator_list(loop_list)
    # or
    routines.register_loop_iterator_list(loop_list, deep_copy = True)
    # If sooner or later a loop will come in the pipeline after this step above,
    # then the loop will go through all the elements of the given lists and will
    # provide each of them once for the members of the loop kernel
    # via the function routines.pop_loop_iterator(data)
    return data


def test3_meta_data_with_arguments(data: dict[str, Any]) -> dict[str, Any]:
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)
    # default_arguments_values
    arg = {
        'input': constants.DEFAULT_IO_DATA_LABEL,
        'output': constants.DEFAULT_IO_DATA_LABEL,
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    if iterator:
        arg['input'] = iterator

    # specific code part
    pass

    routines.set_meta_in_data(data, meta)
    return data
