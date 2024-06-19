# TODO
# config levels
# more and embedded loops (list of loop list and iterator list)

import json
from dataclasses import dataclass, field
from typing import Any

import lasagna
import lasagna.layer as layer
from typing import Optional, List
from pathlib import Path
from toolz import pipe
import importlib
import pandas as pd
import pipeline_constants as constants
import pipeline_routines as routines
import pipeline_singletons as singletons
import sys


dept_of_nested_loops = 0
current_max_dept_of_nested_loops = 0
loop_kernel_pipelines = []    # it contains the child pipeline of loops in the order of execution


@dataclass
class PipelineConfig:
    input_path: str
    output_path: str
    entry_point: str
    imports: list[str]
    pipelines: list[dict[str, list[dict[str, str]]]]
    input_file_name: str = field(default=None)
    pipeline_extension: list[dict[str, list[dict[str, str]]]] = field(default=None)
    tmp_paths: list[str] = field(default=None)
    further_configuration: Optional[list[dict[str, str]]] = field(default=None)


def load_pipeline_config(argv: list[str]) -> PipelineConfig:
    # set the environment variable with a prefix
    if len(argv) == 1:
        return lasagna.build(
            PipelineConfig,
            [
                layer.DataClassDefaultLayer(
                    PipelineConfig(
                        '.', '.', 'default_p', [], [{'default_p': [{'version': '~'}, {'help': '~'}]}]
                    )
                ),
            ],
        )
    else:
        converted_list = map(Path, argv[1:])
        yaml_layers = map(layer.YamlLayer, converted_list)
        l_config = lasagna.build(
            PipelineConfig,
            [
                *yaml_layers,
                layer.DataClassDefaultLayer(
                    PipelineConfig(
                        '.', '.', '', 'default_p', [], [{'default_p': [{'version': '~'}, {'help': '~'}]}], [], ['.']
                    )
                ),
            ]
        )
        first_element = True
        for sub_pipeline in l_config.pipelines:
            if first_element:
                first_element = False
            else:
                for key in sub_pipeline:
                    l_config.pipelines[0][key] = sub_pipeline[key]

        del l_config.pipelines[1:]

        if len(l_config.pipeline_extension) > 0:
            for extension_element in l_config.pipeline_extension:
                for key in extension_element:
                    l_config.pipelines[0][key] = extension_element[key]
        return l_config


def increment_dept_of_nested_loops():
    global current_max_dept_of_nested_loops
    global dept_of_nested_loops
    dept_of_nested_loops += 1
    if dept_of_nested_loops > current_max_dept_of_nested_loops:
        current_max_dept_of_nested_loops = dept_of_nested_loops


def init_iterator(data: dict[str, Any]) -> dict[str, Any]:
    global dept_of_nested_loops
    name_of_list_of_loop_iterators = data[constants.ARG_KEYWORD_LOOP][dept_of_nested_loops - 1]
    iterator = data[name_of_list_of_loop_iterators].pop(0)
    data[constants.ARG_KEYWORD_ITERATOR] = iterator
    return data


def loop_interpreter(data: dict[str, Any]) -> dict[str, Any]:
    global dept_of_nested_loops
    global current_max_dept_of_nested_loops
    global loop_kernel_pipelines
    param_singleton = singletons.Arguments()
    if len(loop_kernel_pipelines) > 0:
        increment_dept_of_nested_loops()
        kernel = loop_kernel_pipelines[dept_of_nested_loops - 1]
        name_of_list_of_loop_iterators = data[constants.ARG_KEYWORD_LOOP][dept_of_nested_loops - 1]
        param_singleton.replace_current_argument_lists()
        while len(data[name_of_list_of_loop_iterators]) > 0:
            data = pipe(data, *kernel)
            param_singleton.renew_loop_argument_lists()
        param_singleton.restore_last_buffered_argument_list()
        routines.pop_loop_iterator(data)   # it is needed just in that case if no one used up the iterator
        del data[name_of_list_of_loop_iterators]
        del data[constants.ARG_KEYWORD_LOOP][dept_of_nested_loops - 1]
        dept_of_nested_loops -= 1
        if dept_of_nested_loops == 0:
            del loop_kernel_pipelines[:current_max_dept_of_nested_loops]
            current_max_dept_of_nested_loops = 0
    return data


def validate_pipeline(
            config: PipelineConfig,
            current_pipeline: str,
            modules: dict,
            current_param_lists: list,
            param_lists_of_loops: list[list]) -> list:
    global loop_kernel_pipelines
    # preparing available building blocks
    # this_module = sys.modules[__name__]
    available_functions = {}
    for module in modules:
        function_list = dir(modules[module])
        available_functions[module] = function_list

    pipeline = []
    for func_const in config.pipelines[0][current_pipeline]:
        for func in func_const:
            if func[:len(constants.ARG_KEYWORD_LOOP)] == constants.ARG_KEYWORD_LOOP:
                child_pipeline = [init_iterator]
                kernel_arguments_lists = []
                param_lists_of_loops.append(kernel_arguments_lists)
                loop_kernel_pipelines.append(child_pipeline)
                pipeline.append(loop_interpreter)
                child_pipeline.extend(validate_pipeline(
                        config,
                        func_const[func],
                        modules,
                        kernel_arguments_lists,
                        param_lists_of_loops))
                # f = getattr(this_module, 'init_iterator')
            elif func in config.pipelines[0]:
                sub_pipeline = validate_pipeline(config, func, modules, current_param_lists, param_lists_of_loops)
                pipeline.extend(sub_pipeline.copy())
            else:
                not_found = True
                for module in available_functions:
                    if func in available_functions[module]:
                        f = getattr(modules[module], func)
                        pipeline.append(f)
                        current_param_lists.append(func_const)
                        not_found = False
                        break
                if not_found:
                    raise NotImplementedError("Error: None of the imported modules contain the function " + func + "!")
    return pipeline


def run_pipeline(config: PipelineConfig, pipeline: list, current_param_lists: list) -> (str, dict[str, pd.DataFrame]):
    config.tmp_paths.insert(0, config.input_path)
    config.tmp_paths.append(config.output_path)
    meta = {constants.TMP_PATH_INDEX : 0}
    meta[constants.TMP_PATHS] = config.tmp_paths
    if config.further_configuration:
        for key_value_pair in config.further_configuration:
            for key in key_value_pair:
                meta[key] = key_value_pair[key]
    json_meta = json.dumps(meta)
    data = {constants.ARG_KEYWORD_LOOP: []}
    data[constants.ARG_KEYWORD_META] = json_meta
    # data[constants.ARG_KEYWORD_ARGUMENTS] = current_param_lists
    retval = pipe(data, *pipeline)
    return 0


if __name__ == "__main__":
    c = load_pipeline_config(sys.argv)
    if not c.imports or not c.pipelines or not c.entry_point:
        raise NotImplementedError("Error: Missing 'imports', 'pipeline' or 'entry_point' in the config file.")
    else:
        imported_modules = {}
        for module_name in c.imports:
            i = importlib.import_module(module_name)
            imported_modules[module_name] = i

        param_lists = []
        arguments_of_sub_pipelines = []
        pipeline_string = validate_pipeline(c, c.entry_point, imported_modules, param_lists, arguments_of_sub_pipelines)
        p = singletons.Arguments()
        p.current_param_lists = param_lists
        p.param_lists_of_loops = arguments_of_sub_pipelines
        run_pipeline(c, pipeline_string, param_lists)
