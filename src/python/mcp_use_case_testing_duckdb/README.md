# SQL Dataframe editor

Content of the configuration file:

```yaml

input_path: &base_dir 'mcp_use_case_testing_duckdb'
output_path: *base_dir
entry_point: 'main_p'
imports:
  - mcp_general_functions.mcp_general_io
  - mcp_general_functions.mcp_general_transformations
pipelines:
  - main_p:
      - read_csv: 
          - { 'input_path': 'mcp_use_case_testing_duckdb', 'file_name': 'testing_csv.csv'}
      - df_sql_statement:
          - { 'SQL_STMT': 'SELECT * FROM data '}
      - print_to_stdout: ~

```

## Requirements

None

## How to Start

Assuming you are in the directory `configurable_pipeline_frm/src/python`:

```bash
poetry run python mcp_frm/pipeline_runtime.py mcp_use_case_testing_duckdb/testing_duckdb_use_case.yaml
```
