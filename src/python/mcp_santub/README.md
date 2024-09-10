# SanTub Use Case 1: Extracting Data of Inspection Report related to bridges and Tunnels From Excel Worksheets

## Description

It retrieves some data from a csv file and from many excel worksheets and merges them in parquet files. This configuration uses already many generally usable python functions. These are:
- read_csv: it reads the csv file given either via the default input stream, as argument in the yaml config file or as loop iterator.
- list_dir: it lists the path given either via the default input stream, as argument in the yaml config file or as loop iterator.
- set_default_file_name_from_data: it sets the default file name for an upcoming input/output function. The file name can given either via the default input stream, as argument in the yaml config file or as loop iterator.
- write_parquet: it writes data to parquet files. The target file name and location can be specified in various ways.
- remove_data: remove some data from the passed through dictionary *data*, which is identified by the label specifiied either via the default input stream, as argument in the yaml config file or as loop iterator.
- read_excel_worksheets: it reads data from an excel file given either via the default input stream, as argument in the yaml config file or as loop iterator.
- vertical_concatenation: it concatenates pandas dataframes stored in the passed through dictionary *data* and identified by either the default input stream, as argument in the yaml config file or as loop iterator.  


## Requirements

The input data must be present in the same directory structure (see [../../../../data_santub](../../../../data_santub)) and their location must be given 
in the part *input_path* of the yaml configuration.
The location given in the part *output_path* of the yaml configuration are going to be created on the local disc.

The output is going to be generated into the location given in the part *output_path* of the yaml configuration.

## How to Start

Assuming you are in the directory *mcp_frm*:

```
./pipeline_runtime.py ../mcp_santub/santub_use_case1.yaml
```

# SanTub Use Case 2: Convert Data of Excel Worksheets into parquet files (one file per bridge per build part)

## Description

It retrieves some data from a csv file and from many excel worksheets and merges them in parquet files. The code will generate many parquet file for every bridges/tunnes (one file per build part).
Each file is placed into directory named after the object name.

## Requirements

The input data must be present in the same directory structure (see [../../../../data_santub](../../../../data_santub)) and their location must be given 
in the part *input_path* of the yaml configuration.
The location given in the part *output_path* of the yaml configuration are going to be created on the local disc.

The output is going to be generated into the location given in the part *output_path* of the yaml configuration.

## How to Start

Assuming you are in the directory *mcp_frm*:

```
./pipeline_runtime.py ../mcp_santub/santub_use_case2.yaml ../mcp_santub/santub_use_case1.yaml
```