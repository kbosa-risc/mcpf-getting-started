from typing import Any
import constants
import json


def get_meta_data(data: dict[str, Any]) -> dict[str, Any]:
    if constants.ARG_KEYWORD_META not in data:
        raise ValueError("Error! No metadata in the arguments")
    json_meta = data[constants.ARG_KEYWORD_META]
    meta = json.loads(json_meta)
    return meta


def set_meta_in_data(data: dict[str, Any], meta: dict[str, Any]):
    json_meta = json.dumps(meta)
    data[constants.ARG_KEYWORD_META] = json_meta


def register_loop_iterator_list(data: dict[str, Any], list_name):
    data[constants.ARG_KEYWORD_LOOP].append(list_name)

