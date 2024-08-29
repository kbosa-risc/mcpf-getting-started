
# A simple Use Case

## Description

It uses the generalised implementation of only two python functions.
They are *list_dir* and *print_to_stdout* and they are located in [mcp_general_io.py](../mcp_general_functions/mcp_general_io.py)

This use case simply list of the content of the given input folder (*input_path* in the configuration below) and of its subfolders (see the yaml configuration below). 
For achieving this, 
1. it creates a list about the content of the given input folder and start a loop which go through this list;
1. It print out the current element, then it create subsequent list for an embedded loop (if the current element is not a directory it cretes an empty list); and
1. In an inner loop, print out the current element of the second list.

Content of the configuration file:

```
input_path: &base_dir '..'
output_path: *base_dir
entry_point: 'main_p'
imports:
  - mcp_general_functions.mcp_general_io
pipelines:
  - main_p:
      - list_dir:
          - { relative_path: True, output_for_iteration: True }
      - loop: list_input_dirs_p

  - list_input_dirs_p:
      - processing_files_p: ~
      - list_dir:
          - { 'only_file_names_return': True, 'output_for_iteration': True }
      - loop: processing_files_p

  - processing_files_p:
      - print_to_stdout: ~

```

## Requirements

None

## How to Start

Assuming you are in the directory ./mcp_frm:

```
./pipeline_runtime.py ../mcp_use_case_getting_started/first_use_case.yaml
```
