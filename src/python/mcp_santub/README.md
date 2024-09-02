# SanTub Use Case: Extracting Inspection Report Data of  Bridge and Tunnel Data From Excel Worksheets

## Description

It retrieves some data from a csv file and from many excel worksheets and merge them in parquet files. This configuration uses already as 
many generally usable python function as possible. These are:
- read_csv: it reads the csv file given either via the default input stream, as argument in the yaml config file or as loop iterator.
- list_dir: it lists the path given either via the default input stream, as argument in the yaml config file or as loop iterator.
- set_default_file_name_from_data: it sets the default file name for an upcoming input/output function. The file name can given either via the default input stream, as argument in the yaml config file or as loop iterator.
- write_parquet: it writes data to parquet files. The target file name and location can be specified various ways.
- remove_data: remove some data from the passed through dictionary *data*, which is identified by the label specifiied either via the default input stream, as argument in the yaml config file or as loop iterator.
- read_excel_worksheets: it reads data from an excel file given either via the default input stream, as argument in the yaml config file or as loop iterator.
- vertical_concatenation: it concatenates pandas dataframes stored in the passed through dictionary *data* and identified by either the default input stream, as argument in the yaml config file or as loop iterator.  


## Requirements

The input data must be present in the same directory structure (see [../../../../data_santub](../../../../data_santub)) and their location must be given 
in the part *input_path* of the yaml configuration.
The location given in the part *output_path* of the yaml configuration are going to be created on the local disc.

The output is going to be generated into the location given in the part *output_path* of the yaml configuration.

## How to Start

Assuming you are in the directory ./mcp_frm:

./pipeline_runtime.py ../mcp_santub/santub_use_case1.yaml