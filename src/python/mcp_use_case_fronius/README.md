# Fronius 1st Use Case: Resampling and Merging CSV Data

## Description

It reads the same measured data from csv files recorded with various sampling rates, then resamples and merges them.
This was the first use case ever written for the *minimalist configurable pipeline (mcp) framework*, therefore it does not use generally 
written python libraries, see the yaml configuration file [fronius_use_case1.yaml](fronius_use_case1.yaml)


## Requirements

The input data must be present (see [../../../../data_fronius/input_files](../../../../data_fronius/input_files)) and their location must be given 
in the part *input_path* of the yaml configuration.
The location given in the parts *output_path* and *tmp_path* of the yaml configuration are going to be created on the local disc.

The output is going to be generated into the location given in the part *output_path* of the yaml configuration.

## How to Start

Assuming you are in the directory *mcp_frm*:

```
./pipeline_runtime.py ../mcp_use_case_fronius/fronius_use_case1.yaml
```

# Fronius 1st Use Case 2nd Version: Resampling and Merging CSV Data

## Description

It is a refactored version of the previous use case (see the yaml configuration file [fronius_use_case1b.yaml](fronius_use_case1b.yaml)), 
where some generally written python functions are used to demonstrate code reusability, e.g.:
- *unzip*, it extracts a file given either via the default input stream, as argument in the yaml config file or as loop iterator.
- *list_dir*, it lists the path given either via the default input stream, as argument in the yaml config file or as loop iterator.
- *set_default_input_from_variable*, it sets the default input from the yaml config file.


## Requirements

The input data must be present (see [../../../../data_fronius/input_files](../../../../data_fronius/input_files)) and their location must be given 
in the part *input_path* of the yaml configuration.
The location given in the parts *output_path* and *tmp_path* of the yaml configuration are going to be created on the local disc.

The output is going to be generated into the location given in the part *output_path* of the yaml configuration.

## How to Start

Assuming you are in the directory *mcp_frm*:

```
./pipeline_runtime.py ../mcp_use_case_fronius/fronius_use_case1b.yaml
```

# Fronius 2nd Use Case: Resampling and Merging Parquet Data

## Description

It is a modified version of the previous use case. It overwrites the routine specified in the one of the previous yaml config file (it is even, which one) to 
read the input dat from parquet file, see the yaml configuration file [fronius_use_case2.yaml](fronius_use_case2.yaml):

```
input_path: 'c:\Projects\risc_dse\data_fronius2\input_files\'
output_path: 'c:\Projects\risc_dse\data_fronius2\parquet_files\'
input_file_name: '*.tar.gz'

tmp_paths:
  - 'c:\Projects\he_meta\data_fronius2\unzipped_files\'

pipeline_extension:
  - read_input_data_p:
    - read_parquet_file: ~
```

## Requirements

First of all, since this use case is a pipeline extension, it requires one of the yaml configuration files from the 1st use case 
([fronius_use_case1.yaml](fronius_use_case1.yaml) or [fronius_use_case1b.yaml](fronius_use_case1b.yaml)).

The input data must be present (see [../../../../data_fronius2/input_files](../../../../data_fronius2/input_files)) and their location must be given 
in the part *input_path* of the yaml configuration.
The location given in the parts *output_path* and *tmp_path* of the yaml configuration are going to be created on the local disc.

The output is going to be generated into the location given in the part *output_path* of the yaml configuration.

## How to Start

Assuming you are in the directory *mcp_frm*, you have two options:

```
./pipeline_runtime.py ../mcp_use_case_fronius/fronius_use_case2.yaml ../mcp_use_case_fronius/fronius_use_case1.yaml
```
or
```
./pipeline_runtime.py ../mcp_use_case_fronius/fronius_use_case2.yaml ../mcp_use_case_fronius/fronius_use_case1b.yaml
```
