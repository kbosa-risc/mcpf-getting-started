
# sim2influx Use Case

## Description

It reads some csv like data and saves them to a given influx database.

## Requirements

The input data must be present (see [../../../../data_sim](../../../../data_sim)) and their location must be given 
in the part *input_path* of the yaml configuration.

A influx database instance must be available and its access information (url, org, bucket, token etc.) must be entered 
into the part *database_config* as well as arguments of the function *influx_df_write* in the yaml configuration file, see [sim2influx_use_case.yaml](sim2influx_use_case.yaml).

Remark: it is possible, that the retention period is not infinite (0) by default (in this case inserted data older than the retention period will be ignored automatically). 
To avoid this see [https://confluence.risc-software.at/pages/viewpage.action?pageId=129925201](https://confluence.risc-software.at/pages/viewpage.action?pageId=129925201)

## How to Start

Assuming you are in the directory *mcp_frm*:

```
./pipeline_runtime.py ../mcp_use_case_sim2influx/sim2influx_use_case.yaml
```

# sim2timescale Use Case

## Description

It is a modified version of the previous use case. It just overwrites some routines specified 
in the yaml config file of the previous use case to save the data into a timescale database instead of influx.

## Requirements

The input data must be present (see [../../../../data_sim](../../../../data_sim)) and their location must be given 
in the part *input_path* of the yaml configuration.

A timescale database instance must be available and its access information (url,  etc.) must be entered 
into the part *database_config* as well as arguments of the function *timescale_df_write* in the yaml configuration file, see [sim2timescale_use_case.yaml](sim2timescale_use_case.yaml).

Additionally, the following create statement must prior be executed in the database instance:

```
CREATE TABLE simulation_data(
"Id" text NOT NULL,
"Time" bigint NOT NULL,
"T" double precision,
"C" double precision,
"Ux" double precision,
"Uy" double precision,
"Uz" double precision,
p_rgh double precision
);
```

The time stamp is given in terms of unix in microseconds since the start of the simulation.
In terms of the Influx Database, the data schema is the same, but the table does not need to get 
created initially.

It is a modified version of the previous use case. It just overwrites three routines specified 
in the yaml config file of the previous use case to

## How to Start

Assuming you are in the directory *mcp_frm*:

```
./pipeline_runtime.py ../mcp_use_case_sim2influx/sim2timescale_use_case.yaml ../mcp_use_case_sim2influx/sim2influx_use_case.yaml
```
