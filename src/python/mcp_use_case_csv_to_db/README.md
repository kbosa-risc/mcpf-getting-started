
# Getting Started: A simple Use Case

## Description

This program is designed to efficiently import data from a CSV file into a PostgreSQL database. The program reads the CSV file, processes its contents, and inserts the data into a specified table within the PostgreSQL database.

Content of the configuration file:

```
input_path: &base_dir 'C:\Workspace\mjahn\risc_dse\configurable_pipeline_frm\src\python\mcp_use_case_testing_duckdb'
output_path: *base_dir
entry_point: 'main_p'
imports:
  - mcp_general_functions.mcp_general_io
  - mcp_general_functions.mcp_general_db
  - mcp_use_case_testing_duckdb.create_test_file
pipelines:
  - main_p:
      - create_test_csv_data: ~
      - read_csv: 
          - { 'input_path': '..\mcp_use_case_testing_duckdb', 'file_name': 'testing_csv.csv'}
      - print_to_stdout: ~
      - df_to_filelike_to_postgres: ~
      - print_to_stdout: ~
```

## Requirements

configure your database in constants

## How to Start

Assuming you are in the directory *mcp_frm*:

```
python ./pipeline_runtime.py ..\mcp_use_case_csv_to_db\csv_to_db_use_case.yaml
```
