
# <ins>M</ins>inimalist <ins>C</ins>onfigurable (Code) <ins>P</ins>ipeline  *(mcp)* Framework

---

The main purpose of the mcp framework is to minimize the effort to re-implement the similar issues over and over again for various use cases. To achieve this it provides the following:
 - A framework which is able to execute specified python functions in a pipeline/workflow defined in a yaml configuration file. 
	- The composed code pipeline can be decomposed to child-pipelines, 
which may in turn include further child-pipelines or python functions.
 	- A child-pipeline may be executed repetitively in loops.
   - For given python functions maybe some sort of additional function arguments can be specified in the yaml configuration.
   - A (child-)pipeline can be refactored in another yaml file and adapted to another use case.
 - Some general logic is already implemented in order to facilitate the usage of the mcp framework.
 - Some coding templates and best practices are presented as well in order to support the user to be able entirely use the capability of this tiny tool.

This directory contains the following:
- the source of mcp framework, see the directory [**mcp_frm**](mcp_frm/README.md);
- some coding guidelines/templates, see the directory as well as 
a tiny collection of some generaly (re-)usable functions (read/write csv/parquet etc.),
see the directory [**mcp_general_functions**](mcp_general_functions/README.md);
- a very simple pipeline configuration for getting started, see the directory [**mcp_use_case_getting_started**](mcp_use_case_getting_started/README.md);
- re-implemented fronius use case (re-sampling csv/parquet data and write into parquet), see the directory [**mcp_use_case_fronious**](mcp_use_case_fronious/README.md);
- re-implemented UPO use case, see the directory [**mcp_use_case_UPO**](mcp_use_case_UPO/README.md);
- re-implemented sim2influx use case (writing csv data into influx/timescale db), see the directory [**mcp_use_case_sim2infux**](mcp_use_case_sim2influx/README.md);
- the source of the santub use case (converting data on excel worksheet to parquet), see the directory [**mcp_use_santub**](mcp_use_case_santub/README.md); and
- the source tiny dotnet use case to demonstrate how to wrapped and re-use c# code (e.g.: from the EVIS project), see the directory [**mcp_use_dot_net**](mcp_use_case_dot_net/README.md)

# Synopsis

>      pipeline_runtime.py  
>         [addapted_use_case_config_n.yaml ... addapted_use_case_config_n.yaml] 
>         basic_use_case_configuration.yaml

### Examples

       ./pipeline_runtime.py ../mcp_use_case_fronius/fronius_use_case1.yaml
	   or
	   ./pipeline_runtime.py  
	        ../mcp_use_case_fronius/fronius_use_case2.yaml  
            ../mcp_use_case_fronius/fronius_use_case1.yaml
	
## Getting Started

Execute your first pipeline from the directory *mcp_frm*, which will list the content of the parent directory on the standard output:
```
	./pipeline_runtime.py ../mcp_use_case_getting_started/first_use_case.yaml	
```

For particular yaml configuration examples, see the use cases. For coding guldelines and best practices, see [../mcp_general_functions/README.md](../mcp_general_functions/README.md)