
# Getting Started: Some simple Use Cases

## First Use Case

### Description

It uses the generalized implementation of only two python functions.
They are *list_dir* and *print_to_stdout* and they are located in [mcp_general_functions.mcp_general_io.py](../mcp_general_functions/mcp_general_io.py)

This use case simply list of the content of the given input folder (*input_path* in the configuration below) and of its subfolders (see the yaml configuration below). 
For achieving this, 
1. it creates a list about the content of the given input folder and start a loop which go through this list;
1. It print out the current element to stdout, then it creates subsequent list for an embedded loop (if the current element is not a directory it creates an empty list); and
1. In an inner loop, print out the current element of the second list to stdout.
1. Finally, the program prints out the string literal "done." to the stdout (this code part is in the 
codepipeline only because of the third use case, where it will be modified to display the final 
output of the concatenation, see below).

Content of the configuration file:

```
input_path: &base_dir '.'
output_path: *base_dir
entry_point: 'main_p'

further_configuration:   # This part only demonstrates, how to define key value pairs, but its content are not used
   - first_key_value_pair: value1
   - second_key_value_pair: value2
imports:
  - mcp_general_functions.mcp_general_io
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

Assuming you are in the directory *mcp_frm*:

```
./pipeline_runtime.py ../mcp_use_case_getting_started/first_use_case.yaml
```

## First Pipeline Extension

### Description

This use case "just" extends the previous one (so it cannot be used without 
giving the first pipeline configuration). Besides the content of the given directory and 
its sub-directory, it additionally displays the content of the listed csv files (if there is any).

This use case uses the generalized implementation of an additionaly python functions, which is called 
*read_csv* and is located in [mcp_general_functions.mcp_general_io.py](../mcp_general_functions/mcp_general_io.py).

Content of the configuration file:

```
input_path: &base_dir '.'
output_path: *base_dir

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

Assuming you are in the directory *mcp_frm*:

```
./pipeline_runtime.py 
		../mcp_use_case_getting_started/first_extension.yaml
		../mcp_use_case_getting_started/first_use_case.yaml
```

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
- *create_test_env* is located in [mcp_use_case_getting_started.prepare_test_env.py](../mcp_use_case_getting_started/prepare_test_env.py).
  It creates a five levels deep directory structure under the given directory (if it does not exist)
  and scatters some generated csv files in it.
- *vertical_concatenation* is located [mcp_general_functions.mcp_general_transformations.py](../mcp_general_functions/mcp_general_transformations.py)
  and appends it appends the given matrix to a pandas dataframe.
           
Content of the configuration file:

```
input_path: &base_dir '.\testDir'
output_path: *base_dir
entry_point: 'preprocessing_p'

imports:
  - mcp_general_functions.mcp_general_io
  - mcp_general_functions.mcp_general_transformations
  - mcp_use_case_getting_started.prepare_test_env

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

Assuming you are in the directory *mcp_frm*:

```
./pipeline_runtime.py
		../mcp_use_case_getting_started/second_extension_recursive.yaml
		../mcp_use_case_getting_started/first_extension.yaml
		../mcp_use_case_getting_started/first_use_case.yaml
```