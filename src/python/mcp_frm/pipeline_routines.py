from typing import Any
import constants
import json
import pipeline_singletons as singleton
import inspect
import sys


def get_meta_data(data: dict[str, Any]) -> dict[str, Any]:
    if constants.ARG_KEYWORD_META not in data:
        raise ValueError("Error! No metadata in the arguments")
    json_meta = data[constants.ARG_KEYWORD_META]
    meta = json.loads(json_meta)
    caller_func = inspect.getframeinfo(sys._getframe(1))[2]
    param_singleton = singleton.Arguments()
    meta[constants.ARG_KEYWORD_ARGUMENTS] = param_singleton.get_upcoming_arguments(caller_func)
    return meta


def set_meta_in_data(data: dict[str, Any], meta: dict[str, Any]):
    del meta[constants.ARG_KEYWORD_ARGUMENTS]
    json_meta = json.dumps(meta)
    data[constants.ARG_KEYWORD_META] = json_meta


def register_loop_iterator_list(data: dict[str, Any], list_name):
    data[constants.ARG_KEYWORD_LOOP].append(list_name)


def pop_loop_iterator(data: dict[str, Any]) -> Any:
    return data.pop(constants.ARG_KEYWORD_ITERATOR, None)


def get_current_input_dir(meta: dict[str, Any]) -> str:
    index_of_dirs = meta[constants.TMP_PATH_INDEX]
    input_dir = meta[constants.TMP_PATHS][index_of_dirs]
    return input_dir


def get_current_output_dir(meta: dict[str, Any]) -> str:
    index_of_dirs = next_tmp_dir_index(meta)
    output_dir = meta[constants.TMP_PATHS][index_of_dirs]
    return output_dir


def next_tmp_dir_index(meta: dict[str, Any]) -> int:
    index_of_dirs = meta[constants.TMP_PATH_INDEX]
    if len(meta[constants.TMP_PATHS]) - 1 > index_of_dirs:
        index_of_dirs += 1
    return index_of_dirs


def set_current_output_dir_to_input_dir(meta: dict[str, Any]):
    meta[constants.TMP_PATH_INDEX] = next_tmp_dir_index(meta)
