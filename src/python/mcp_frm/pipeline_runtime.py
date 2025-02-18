#! /usr/bin/env python3
# TODO
# config levels
# more and embedded loops (list of loop list and iterator list)

import json
from dataclasses import dataclass, field
from typing import Any

import risc_lasagna as lasagna
import risc_lasagna.layer as layer
from typing import Optional, List
from pathlib import Path
from toolz import pipe
import importlib
import pandas as pd
import pipeline_constants as constants
import pipeline_routines as routines
import pipeline_singletons as singletons
import sys
import os.path
import dataclasses


dept_of_nested_loops = 0
current_max_dept_of_nested_loops = 0
loop_kernel_pipelines = []    # it contains the child pipeline of loops in the order of execution


@dataclass
class DatabaseConfig:
    type: str
    url: str
    user: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = None
    org: Optional[str] = None
    bucket: Optional[str] = None


@dataclass
class PipelineConfig:
    input_path: str
    output_path: str
    entry_point: str
    imports: list[str]
    pipelines: list[dict[str, list[dict[str, str]]]]
    input_file_name: str = field(default=None)
    tmp_paths: list[str] = field(default=None)
    pipeline_extension: list[dict[str, list[dict[str, str]]]] = field(default=None)
    further_configuration: Optional[list[dict[str, str]]] = field(default=None)
    database_configs: Optional[List[DatabaseConfig]] = field(default=None)


def load_pipeline_config(argv: list[str]) -> PipelineConfig:
    """
    It uses the "lasagna" package to load the yaml pipline configuration files and compose a single code pipeline
    configuration from them.
    """
    # set the environment variable with a prefix
    if len(argv) == 1:
        return lasagna.build(
            PipelineConfig,
            [
                layer.DataClassDefaultLayer(
                    PipelineConfig(
                        '.', '.', 'default_p', [], [{'default_p': [{'version': '~'}, {'help': '~'}]}], '', []
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
                        '.', '.', 'default_p', [], [{'default_p': [{'version': '~'}, {'help': '~'}]}], '', []
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

        if l_config.pipeline_extension and len(l_config.pipeline_extension) > 0:
            for extension_element in l_config.pipeline_extension:
                for key in extension_element:
                    l_config.pipelines[0][key] = extension_element[key]
        return l_config


def increment_dept_of_nested_loops():
    """
    This function keeps track the dept of the nested loops.
    """
    global current_max_dept_of_nested_loops
    global dept_of_nested_loops
    dept_of_nested_loops += 1
    if dept_of_nested_loops > current_max_dept_of_nested_loops:
        current_max_dept_of_nested_loops = dept_of_nested_loops


def init_iterator(data: dict[str, Any]) -> dict[str, Any]:
    """
    Each execution of every loop kernel starts with this function. It initializes the current value of the
    loop iterator.
    """
    global dept_of_nested_loops
    loop_singleton = singletons.LoopIterators()
    loop_singleton.init_current_iterator(dept_of_nested_loops - 1)
    return data


def loop_interpreter(data: dict[str, Any]) -> dict[str, Any]:
    """
    This function is used to implement a loop in the code pipeline.
    """
    global dept_of_nested_loops
    global current_max_dept_of_nested_loops
    global loop_kernel_pipelines
    loop_singleton = singletons.LoopIterators()
    param_singleton = singletons.Arguments()
    if len(loop_kernel_pipelines) > 0:
        increment_dept_of_nested_loops()
        kernel = loop_kernel_pipelines[dept_of_nested_loops - 1]
        param_singleton.replace_current_argument_lists()
        while loop_singleton.size_of_an_iterator_list(dept_of_nested_loops - 1) > 0:
            data = pipe(data, *kernel)
            param_singleton.renew_loop_argument_lists()
        param_singleton.restore_last_buffered_argument_list()
        routines.pop_loop_iterator()  # it is needed just in that case if no one used up the iterator
        loop_singleton.remove_an_iterator_list(dept_of_nested_loops - 1)
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
    """
    This function compose the code pipeline and pipeline of the loop kernels according the given yaml configuration,
    stores the function arguments given in the yaml configuration in a structured way and
    validate each pipeline (e.g.: it checks the existence of the given functions in the enumerated python modules).
    """
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
    """
    It initializes the "meta" and execute the code pipeline composed from the given configuration.
    """
    config.tmp_paths.insert(0, config.input_path)
    config.tmp_paths.append(config.output_path)
    tmp_absolut_paths = []
    for path in config.tmp_paths:
        tmp_absolut_paths.append(os.path.abspath(path))
    meta = {constants.TMP_PATH_INDEX: 0}
    meta[constants.TMP_PATHS] = tmp_absolut_paths
    if config.further_configuration:
        for key_value_pair in config.further_configuration:
            for key in key_value_pair:
                meta[key] = key_value_pair[key]
    if config.database_configs:
        db_configs = []
        for config_element in config.database_configs:
            config_dict = {}
            for f in dataclasses.fields(config_element):
                config_dict[f.name] = getattr(config_element, f.name)
            db_configs.append(config_dict)
        meta[constants.DB_CONFIG] = db_configs
    json_meta = json.dumps(meta)
    data = {constants.ARG_KEYWORD_META: json_meta}
    retval = pipe(data, *pipeline)
    return 0

def run(*args: str) -> None:
    """
    Run pipeline programmatically as if called from command line
    """
    for arg in args:
        if not os.path.isfile(arg):
            raise FileNotFoundError("Error: config file " + arg + " does not exist.")
    c = load_pipeline_config(sys.argv)
    if not c.imports or not c.pipelines or not c.entry_point:
        raise NotImplementedError("Error: Missing 'imports', 'pipelines' or 'entry_point' in the config file.")
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

if __name__ == "__main__":
    run(*sys.argv[1:])
