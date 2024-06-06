from dataclasses import dataclass

import lasagna
import lasagna.layer as layer
from typing import Optional, List
from pathlib import Path
from toolz import pipe
import importlib
import pandas as pd


@dataclass
class PipelineConfig:
    input_path: str
    output_path: str
    tmp_path: str
    imports: List[str]
    pipeline: List[str]
    command_line_args: Optional[str] = None


def load_pipeline_config() -> PipelineConfig:
    # set the environment variable with a prefix
    return lasagna.build(
        PipelineConfig,
        [
            layer.YamlLayer(Path("pipeline_config.yaml")),
            layer.DataClassDefaultLayer(
                PipelineConfig(
                    '.', '.', '.', [], ["version", "help"]
                )
            ),
        ],
    )


def validate_pipeline(config: PipelineConfig, modules: dict) -> list:
    # preparing available building blocks
    available_functions = {}
    for module in modules:
        function_list = dir(modules[module])
        available_functions[module] = function_list

    pipeline = []
    for func in config.pipeline:
        not_found = True
        for module in available_functions:
            if func in available_functions[module]:
                f = getattr(modules[module], func)
                pipeline.append(lambda x: f(*x))
                not_found = False
                break
        if not_found:
            raise NotImplementedError("Error: None of the imported modules contain the function " + func + "!")
    return pipeline


def run_pipeline(config: PipelineConfig, pipeline: list) -> (str, dict[str, pd.DataFrame]):
    retval = pipe((config.input_path, config.command_line_args), *pipeline)
    return 0


if __name__ == "__main__":
    c = load_pipeline_config()
    imported_modules = {}
    for module_name in c.imports:
        i = importlib.import_module(module_name)
        imported_modules[module_name] = i

    pipeline_string = validate_pipeline(c, imported_modules)
    run_pipeline(c, pipeline_string)
