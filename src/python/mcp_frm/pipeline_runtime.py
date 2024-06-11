# TODO
# config levels
# more and embedded loops (list of loop list and iterator list)

import json
from dataclasses import dataclass
from typing import Any

import lasagna
import lasagna.layer as layer
from typing import Optional, List
from pathlib import Path
from toolz import pipe
import importlib
import pandas as pd
import constants
import sys


dept_of_nested_loops = 0
current_max_dept_of_nested_loops = 0
loop_kernel_pipelines = []    # it contains the child pipeline of loops in the order of execution

@dataclass
class PipelineConfig:
    input_path: str
    output_path: str
    input_file_name: str
    entry_point: str
    imports: list[str]
    pipelines: list[dict[str, list[dict[str, str]]]]
    tmp_paths: list[str] = None
    command_line_args: Optional[str] = None


def load_pipeline_config() -> PipelineConfig:
    # set the environment variable with a prefix
    return lasagna.build(
        PipelineConfig,
        [
            layer.YamlLayer(Path("pipeline_config.yaml")),
            layer.DataClassDefaultLayer(
                PipelineConfig(
                    '.', '.', '', 'default_p', [], [{'default_p': [{'version': '~'}, {'help': '~'}]}], ['.']
                )
            ),
        ],
    )


def increment_dept_of_nested_loops():
    global current_max_dept_of_nested_loops
    global dept_of_nested_loops
    dept_of_nested_loops += 1
    if dept_of_nested_loops > current_max_dept_of_nested_loops:
        current_max_dept_of_nested_loops = dept_of_nested_loops


def init_iterator(data: dict[str, Any]) -> dict[str, Any]:
    global  dept_of_nested_loops
    name_of_list_of_loop_iterators = data[constants.ARG_KEYWORD_LOOP][dept_of_nested_loops - 1]
    iterator = data[name_of_list_of_loop_iterators].pop(0)
    data[constants.ARG_KEYWORD_ITERATOR] = iterator
    return data


def loop_interpreter(data: dict[str, Any]) -> dict[str, Any]:
    global dept_of_nested_loops
    global current_max_dept_of_nested_loops
    global loop_kernel_pipelines
    if len(loop_kernel_pipelines) > 0:
        increment_dept_of_nested_loops()
        kernel = loop_kernel_pipelines[dept_of_nested_loops - 1]
        name_of_list_of_loop_iterators = data[constants.ARG_KEYWORD_LOOP][dept_of_nested_loops - 1]
        while len(data[name_of_list_of_loop_iterators]) > 0:
            data = pipe(data, *kernel)

        del data[name_of_list_of_loop_iterators]
        del data[constants.ARG_KEYWORD_LOOP][dept_of_nested_loops - 1]
        dept_of_nested_loops -= 1
        if dept_of_nested_loops == 0:
            del loop_kernel_pipelines[:current_max_dept_of_nested_loops]
    return data


def validate_pipeline(config: PipelineConfig, current_pipeline: str, modules: dict) -> list:
    global loop_kernel_pipelines
    # preparing available building blocks
    this_module = sys.modules[__name__]
    available_functions = {}
    for module in modules:
        function_list = dir(modules[module])
        available_functions[module] = function_list

    pipeline = []
    for func_const in config.pipelines[0][current_pipeline]:
        for func in func_const:
            if func[:len(constants.ARG_KEYWORD_LOOP)] == constants.ARG_KEYWORD_LOOP:
                child_pipeline = validate_pipeline(config, func_const[func], modules)
                f = getattr(this_module, 'init_iterator')
                child_pipeline.insert(0, f)
                loop_kernel_pipelines.append(child_pipeline)
                pipeline.append(loop_interpreter)
            elif func in config.pipelines:
                child_pipeline = validate_pipeline(config, func, modules)
                pipeline.extend(child_pipeline)
            else:
                not_found = True
                for module in available_functions:
                    if func in available_functions[module]:
                        f = getattr(modules[module], func)
                        pipeline.append(f)
                        not_found = False
                        break
                if not_found:
                    raise NotImplementedError("Error: None of the imported modules contain the function " + func + "!")
    return pipeline


def run_pipeline(config: PipelineConfig, pipeline: list) -> (str, dict[str, pd.DataFrame]):
    config.tmp_paths.insert(0, config.input_path)
    config.tmp_paths.append(config.output_path)
    meta = {constants.TMP_PATH_INDEX : 0}
    meta[constants.TMP_PATHS] = config.tmp_paths
    if config.command_line_args:
        meta[constants.COMMAND_LINE_ARGS] = config.command_line_args
    json_meta = json.dumps(meta)
    data = {constants.ARG_KEYWORD_META: json_meta, constants.ARG_KEYWORD_LOOP: []}
    retval = pipe(data, *pipeline)
    return 0


if __name__ == "__main__":
    c = load_pipeline_config()
    if not c.imports or not c.pipelines or not c.entry_point:
        raise NotImplementedError("Error: Missing 'imports', 'pipeline' or 'entry_point' in the config file.")
    else:
        imported_modules = {}
        for module_name in c.imports:
            i = importlib.import_module(module_name)
            imported_modules[module_name] = i

        pipeline_string = validate_pipeline(c, c.entry_point, imported_modules)
        run_pipeline(c, pipeline_string)
