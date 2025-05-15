import csv
import os
import random
from typing import Any

import mcpf_core.core.routines as routines
import mcpf_core.func.constants as constants


def create_test_env(data: dict[str, Any]) -> dict[str, Any]:
    """
    It creates a test environment for the recursive use case (second_extension_recursive.yaml)
    under the given directory, if it does not exist:
        - it creates a five levels deep directory structure and
        - scatters some generated csv files in it (the content of these files are going to be concatenated).

    Yaml args:
        'input_path':       a string containing a directory path, under which the mentioned test environment
                            will be created,
                            by default it is the value identified with the label
                            constants.DEFAULT_IO_DATA_LABEL (if it is a string)
        'relative_path':    a bool value, if it is 'True' the given 'input_path' is a relative path
                            by default it is 'False'

    Returns in data:
        'output':   it is a label in 'data' which identifies the output
                    (the absolute path of the created directory structure),
                    by default it is constants.DEFAULT_IO_DATA_LABEL
    """
    # general code part 2/1
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)

    # default_arguments_values
    default_input_path = "."
    if constants.DEFAULT_IO_DATA_LABEL in data and isinstance(data[constants.DEFAULT_IO_DATA_LABEL], str):
        default_input_path = data[constants.DEFAULT_IO_DATA_LABEL]
    arg = {"output": constants.DEFAULT_IO_DATA_LABEL, "input_path": default_input_path, "relative_path": False}
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    if iterator:
        arg["input_path"] = iterator

    # specific code part
    if arg["relative_path"]:
        if arg["input_path"] != ".":
            arg["input_path"] = os.path.join(routines.get_current_input_dir(meta), arg["input_path"])
        else:
            arg["input_path"] = routines.get_current_input_dir(meta)
    data[arg["output"]] = arg["input_path"]
    if not os.path.isdir(arg["input_path"]):
        list_dir = [
            arg["input_path"],
            arg["input_path"] + "/testDir1",
            arg["input_path"] + "/testDir1/testDir11/testDir111/testDir1111",
            arg["input_path"] + "/testDir1/testDir11/testDir112",
            arg["input_path"] + "/testDir1/testDir11/testDir113",
            arg["input_path"] + "/testDir1/testDir12/testDir121",
            arg["input_path"] + "/testDir1/testDir12/testDir122",
            arg["input_path"] + "/testDir1/testDir12/testDir123/testDir1231",
            arg["input_path"] + "/testDir1/testDir13",
            arg["input_path"] + "/testDir1/testDir13/testDir131",
            arg["input_path"] + "/testDir2/testDir21/testDir211",
            arg["input_path"] + "/testDir2/testDir22/testDir221/testDir2211",
            arg["input_path"] + "/testDir2/testDir22/testDir222",
        ]
        random.seed(0)
        for current_dir in list_dir:
            os.makedirs(current_dir)
            with open(current_dir + "/test.csv", "w", newline="") as my_file:
                wr = csv.writer(my_file)
                wr.writerow(["a", "b", "c", "d", "e", "f"])
                for _ in range(5):
                    wr.writerow([random.randint(1, 1000) for _ in range(6)])
    routines.set_meta_in_data(data, meta)
    return data
