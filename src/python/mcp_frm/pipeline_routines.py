from typing import Any
import pipeline_constants as constants
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


def register_loop_iterator_list(iterator_list: list, deep_copy: bool = False):
    loop_singleton = singleton.LoopIterators()
    loop_singleton.register_new_iterator_list(iterator_list, deep_copy)


def pop_loop_iterator() -> Any:
    loop_singleton = singleton.LoopIterators()
    return loop_singleton.pop_iterator()


def get_current_input_dir(meta: dict[str, Any]) -> str:
    index_of_dirs = meta[constants.TMP_PATH_INDEX]
    input_dir = meta[constants.TMP_PATHS][index_of_dirs]
    return input_dir


def get_current_tmp_dir(meta: dict[str, Any]) -> str:
    index_of_dirs = next_tmp_dir_index(meta)
    output_dir = meta[constants.TMP_PATHS][index_of_dirs]
    return output_dir


def get_final_output_dir(meta: dict[str, Any]) -> str:
    index_of_dirs = next_tmp_dir_index(meta)
    output_dir = meta[constants.TMP_PATHS][-1]
    return output_dir


def next_tmp_dir_index(meta: dict[str, Any]) -> int:
    index_of_dirs = meta[constants.TMP_PATH_INDEX]
    if len(meta[constants.TMP_PATHS]) - 1 > index_of_dirs:
        index_of_dirs += 1
    return index_of_dirs


def set_current_output_dir_to_input_dir(meta: dict[str, Any]):
    meta[constants.TMP_PATH_INDEX] = next_tmp_dir_index(meta)


def get_db_config(meta: dict[str, Any], db_type: str) -> dict[str, Any]|None:
    if constants.DB_CONFIG not in meta or len(meta[constants.DB_CONFIG]) == 0:
        return None
    ret_val_dict: dict[str, Any] = meta[constants.DB_CONFIG][0]
    index = 1
    while ret_val_dict['type'] != db_type and index < len(meta[constants.DB_CONFIG]):
        ret_val_dict = meta[constants.DB_CONFIG][index]
        index += 1
    if ret_val_dict['type'] == db_type:
        return ret_val_dict
    else:
        return None
