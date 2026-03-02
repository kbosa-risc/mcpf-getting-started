# Minimalist Configurable Pipeline Framework (MCPF)

Use this repository as a starting point for the MCPF pipelines.

The Minimalist Configurable (Code) Pipeline Framework uses YAML configuration files which defines pipelines, where:
* Each pipeline consists of a list of functions or other pipeline references that are called in the very order specified.
* Each function is a pure python function that can be defined anywhere. It must match the pipeline function signature, and it must be reachable during pipeline execution (i.e. must be loadable via import).
* Each function can have a distinct map of arguments specified along with it in the YAML confiuration file. These arguments are passed as meta data to the function.
* A special loop command executes a specified pipeline as many times as there are loop elements.

Use this repository as a starting point for your own MCPF pipelines. MCPF is built on a modular stack of pipeline functions. Many pipeline functions are provided by add-on packages to MCPF.
* __mcpf-core__ contains the core functionality of the mcpf framework. Its source code is available in:
	* [https://github.com/kbosa-risc/mcpf-core](https://github.com/kbosa-risc/mcpf-core)
* __mcpf-docs__  presents some documentation and tutorial for developers. Its source code is available in
	* [https://github.com/kbosa-risc/mcpf-docs](https://github.com/kbosa-risc/mcpf-docs)
* __mcpf-io__ is for basic input/output functions like listing directories. Its source code is available in
	* [https://github.com/kbosa-risc/mcpf-io](https://github.com/kbosa-risc/mcpf-io)
	* [https://github.com/kbosa-risc/mcpf-io-pandas](https://github.com/kbosa-risc/mcpf-io-pandas)
* __mcpf-xform__ provides versatile transformation functions on Pandas dataframes. Its source code is available in
	* [https://github.com/kbosa-risc/mcpf-xform](https://github.com/kbosa-risc/mcpf-xform)
 	* [https://github.com/kbosa-risc/mcpf-xform-pandas](https://github.com/kbosa-risc/mcpf-xform-pandas)
  	* [https://github.com/kbosa-risc/mcpf-xform-sql](https://github.com/kbosa-risc/mcpf-xform-sql)

A preliminary version of a [DSL schema](https://github.com/kbosa-risc/mcpf-docs/blob/P0-30/dsl_schema/mcpf.schema.json) (in JSON format) is also provided and can be integrated into development environments such as Visual Studio Code or PyCharm. This enables syntax validation, auto-completion, and parameter hints during pipeline authoring. See the [README]([https://github.com/kbosa-risc/mcpf-docs/dsl_schema/](https://github.com/kbosa-risc/mcpf-docs/blob/P0-30/dsl_schema/README) for details.

# Getting Started: Some simple Use Cases

This repository provides some example configuration files for the Minimal Configurable Pipeline Framework along with custom functions and usage instructions.

## Prerequisites

* Python 3.10 or later

## Set up working directory

Install prerequisites for virtual environments. You have to do this only once per computer.

```sh
# (Linux)
sudo apt-get -y update && sudo apt-get -y install python3 python3-venv
```

Firstly, clone the repository.

```sh
# (Linux)
git clone https://gitdma.risc-software.at/risc_de/mcp/mcpf-getting-started.git
cd mcpf-getting-started
```

This repository uses `poetry` as a build system. It is recommended to install poetry in a virtual environment. You have to do this only once per cloned project.

```sh
# (Linux)
python3 -m venv ../mcpf-getting-started-venv
( . ../mcpf-getting-started-venv/bin/activate; pip3 install poetry==1.8.5 )
```

Now make available the executables of the virtual environment. You have to do this every time when you start a new console session or add the commands to your shell startup script (e.g. `$HOME/.bashrc`)

```sh
# (Linux)
export PATH=$(pwd)/../mcpf-getting-started-venv/bin:$PATH
hash -r 2> /dev/null
```

To shut down the virtual environment simply close the console.


## Install dependencies

For this repository we only need to install `mcpf[io]` and `mcpf[xform]` (the core will be installed as a required dependency).

```sh
# (Linux)
poetry add "mcpf[io]"
poetry add "mcpf[xform]"
```

## Overview

The `mcpf-getting-started` repository consists of three pipeline configurations.

`first_use_case.yaml` is the base configuration and 
`first_extension.yaml` and `second_extension_recursive.yaml` are extension configurations to inherit from `first_use_case.yaml`.

## First Use Case

### Description

It uses the generalized implementation of only two python functions.
They are *list_dir* and *print_to_stdout* and they are located in the package `mcpf_io.io`.

This use case simply list of the content of the given input folder (*input_path* in the configuration below) and of its subfolders (see the yaml configuration below). 
For achieving this, 
1. it creates a list about the content of the given input folder and start a loop which go through this list;
1. It print out the current element to stdout, then it creates subsequent list for an embedded loop (if the current element is not a directory it creates an empty list); and
1. In an inner loop, print out the current element of the second list to stdout.
1. Finally, the program prints out the string literal "done." to the stdout (this code part is in the 
codepipeline only because of the third use case, where it will be modified to display the final 
output of the concatenation, see below).

Content of the configuration file:

```yaml
input_path: &base_dir '.'
output_path: *base_dir
entry_point: 'main_p'

further_configuration:   # This part only demonstrates, how to define key value pairs, but its content are not used
   - first_key_value_pair: value1
   - second_key_value_pair: value2
imports:
  - mcpf_io.io
pipelines:
  - main_p:
      - list_dir:
          - { relative_path: True, output_for_iteration: True }
      - loop: list_input_dirs_p
      - final_steps: ~

  - list_input_dirs_p:
      - processing_files_p: ~
      - list_dir:
          - {'output_for_iteration': True }
      - loop: processing_files_p

  - processing_files_p:
      - print_to_stdout: ~

  - final_steps:
      - print_to_stdout:
          - {'input': 'done.', 'is_literal': True}

```

### Requirements

None

### How to Start

Assuming you are in the root of the working directory of `mcpf-getting-started`:

```sh
poetry run python3 -m mcpf_core.run getting_started/first_use_case.yaml
```

## First Pipeline Extension

### Description

This use case "just" extends the previous one (so it cannot be used without 
giving the first pipeline configuration). Besides the content of the given directory and 
its sub-directory, it additionally displays the content of the listed csv files (if there is any).

This use case uses the generalized implementation of an additionaly python functions, which is called 
*read_csv* and is located in the package `mcpf_io.pd`. The *pd* module contains all Pandas dataframe related functions.

Content of the configuration file:

```yaml
input_path: &base_dir '.'
output_path: *base_dir

imports:
  - mcpf_io.pd
pipeline_extension:
  - processing_files_p:
    - print_to_stdout: ~
    - read_csv:
      - {relative_path: True, csv_file_extension_only: True, output: 'csv_output'}
    - print_to_stdout:
      - {input: 'csv_output', output: 'csv_output'}
```

### Requirements

None

### How to Start

Assuming you are in the root of the working directory of `mcpf-getting-started`:

```sh
poetry run python3 -m mcpf_core.run \
    getting_started/first_extension.yaml \
		getting_started/first_use_case.yaml 
```

> **_NOTE:_** The extension configuration is specified *first*.


## Second Pipeline Extension - Recursion

### Description

Unlike the previous two use cases, which are for demonstration purposes only, the current one solves 
a bit more realistic problem. 
Namely, recursively searches for csv files in a given directory structure and concatenates 
their contents.

> **_Recursion:_** MCP supports only a special case of recursion in the yaml configuration files.
Namely, if the child pipeline is used as a loop kernel (e.g.: *loop: child_pipeline*) and directly
or indirectly calls to itself as the kernel of an inner loop. In every other cases (e.g.: if a child 
pipeline, which is not applied as loop kernel, simply calls itself) the mcp runtime framework ignores 
the recursive call and jumps over it.\
**Stop Condition:** The recursive call of the loop stops if no more non-empty list is designated, 
on which the loop can iterate.

This use case extends the previous two use cases (so it cannot be used without the prevous two yaml configuration files).
It applies two additional python functions:
- *create_test_env* is located in [getting_started.prepare_test_env.py](getting_started/prepare_test_env.py).
  It creates a five levels deep directory structure under the given directory (if it does not exist)
  and scatters some generated csv files in it.
- *vertical_concatenation* is located in package `mcpf_xform.pd`
  and appends it appends the given matrix to a pandas dataframe.
           
Content of the configuration file:

```yaml
input_path: &base_dir '.\testDir'
output_path: *base_dir
entry_point: 'preprocessing_p'

imports:
  - mcpf_xform.pd
  - getting_started.prepare_test_env

pipeline_extension:
  - preprocessing_p:
      - create_test_env:
          - {relative_path: True}
      - main_p: ~

  - list_input_dirs_p:
      - print_to_stdout: ~
      - read_csv:
          - {relative_path: True, output: 'for_concatenation' }
      - vertical_concatenation:
          - {input: 'for_concatenation', left_value: 'concatenated_content'}
      - list_dir:
          - {output_for_iteration: True }
      - loop: list_input_dirs_p

  - final_steps:
      - print_to_stdout:
          - {input: 'concatenated_content' }
```

### Requirements

None

### How to Start

Assuming you are in the root of the working directory of `mcpf-getting-started`:

```sh
poetry run python3 -m mcpf_core.run \
		getting_started/second_extension_recursive.yaml \
		getting_started/first_extension.yaml \
		getting_started/first_use_case.yaml
```
