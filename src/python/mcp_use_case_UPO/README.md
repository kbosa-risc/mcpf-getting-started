
# UPO 1st Use Case, Output I: Calc. EQE Percentage and Ingegral Current Density

## Description
It reads some csv data, performs some calculation and provide the outcome in a well defined output format

## Requirements

The input data must be present locally in the same directory structures (see [data](data)) and their location must be given 
in the part *input_path* of the yaml configuration.
The location given in the part *output_path* of the yaml configuration are going to be created on the local disc.

The output is going to be generated into the location given in the part *output_path* of the yaml configuration.

## How to Start

Assuming you are in the directory ./mcp_frm:

./pipeline_runtime.py ../mcp_use_case_UPO/upo_use_case1.yaml


# UPO 2nd Use case, Output II: Calc. EQE Percentage

## Description

It is a modified version of the previous use case. It just overwrites three routines specidied 
in the yaml config file of the previous use case to modify the calculation as well as the output format, 
see the yaml configuration file [upo_use_case2.yaml](upo_use_case2.yaml):

```
further_configuration:
  - output_filename: 'testcsvsugg2'

pipeline_extension:
  - initialization_p:
      - init_calc_eqe_perc: ~

  - calculation_core_p:
      - calculate_eqe_perc: ~
      - feedback_on_std_out: ~

  - compose_output_p:
      - compose_output: ~
      - write_eqe_sol2: ~
```

## Requirements

First of all, since this use case is a pipeline extension, it requires one of the yaml configuration files from the 1st use case 
([upo_use_case1.yaml](upo_use_case1.yaml).

The input data must be present locally in the same directory structures (see [data](data)) and their location must be given 
in the part *input_path* of the yaml configuration.
The location given in the part *output_path* of the yaml configuration are going to be created on the local disc.

The output is going to be generated into the location given in the part *output_path* of the yaml configuration.


## How to Start

./pipeline_runtime.py ../mcp_use_case_UPO/upo_use_case2.yaml ../mcp_use_case_UPO/upo_use_case1.yaml