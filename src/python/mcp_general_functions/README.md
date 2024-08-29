
# Coding Guidelines, Best Practices

## Basic requirements

If a python function is going to appear in yaml pipeline configuration, its signature and retun value must be the following:

```
from typing import Any
...
def test1(data: dict[str, Any]) -> dict[str, Any]:  
	# specific code part  
	...  
	return data  
``` 

Other functions, which are called only from python code should not fullfil this requirement.

### Best Practice
To facilitate the general re-usability of your code, use a default label (e.g.: see DEFAULT_IO_DATA_LABEL in [constans.py](constants.py) for sotring the actual input data in the passed though dictionary *data*. 

```
from typing import Any
import mcp_general_functions.constants as constants
...
def function_i(data: dict[str, Any]) -> dict[str, Any]:
	input_data = data[constants.DEFAULT_IO_DATA_LABEL]
	# specific code part
	...
	return data
```

## How to Access to the Meta Information

By default the dictionary *data* contains a json string called *meta* which may contain the following elements:
* **input_path**,
* **output_path**,
* **tmp_paths**,
* **db_configs** and
* key-value pairs defined in the part **further_configuration** in the yaml configuration.

Additionally the key value pairs defined by the developer can be also stored here. 

```
from typing import Any
from mcp_general_functions import constants
import mcp_frm.pipeline_routines as routines
...
def func_i(data: dict[str, Any]) -> dict[str, Any]:
	meta = routines.get_meta_data(data)
	value = meta[key]

	# specific code part
	...

	routines.set_meta_in_data(data, meta)
	return data
```

**Important remark**: The content of the meta can be updated by any function, but in such a case the call *routines.set_meta_in_data(data, meta)* must be executed 
before the end of the function, otherwise the changes are not stored. 

## Configurable Arguments

Additional arguments can be defined in the yaml config file for functions, e.g.:

```
	- func_i:
		- {'bool_argument': True }
```

These arguments are added to json string called *meta*, when the corresponding python function called. 
They are stored as a dictionary under the label 'arguments' (use the constants 'ARGUMENTS' defined in [constans.py](constants.py)):

```
	from typing import Any
	from mcp_general_functions import constants
	import mcp_frm.pipeline_routines as routines
	...
	def func_i(data: dict[str, Any]) -> dict[str, Any]:
		meta = routines.get_meta_data(data)
		if meta[constants.ARGUMENTS]:
			arg = meta[constants.ARGUMENTS]
		bool_argument = arg['bool_argument']

		# specific code part
		...

		routines.set_meta_in_data(data, meta)
		return data
```

**Important remark**: Before the end of the function the call *routines.set_meta_in_data(data, meta)* must be executed to clean up the *meta* data from the current arguments. 

## How loops work in the pipeline

### Registering list of data for iterative

You can registered a list of element (let's call it *list of iterators*), on which you would like to execute a loop. 

```
from typing import Any
import mcp_frm.pipeline_routines as routines
...
def function_i(data: dict[str, Any]) -> dict[str, Any]:
	# specific code part
	...

	loop_list = list(range(0,10))
	routines.register_loop_iterator_list(loop_list)
	# or
	routines.register_loop_iterator_list(loop_list, deep_copy = True)
	# specific code part
	...
	
	return data
```

If sooner or later a loop will come in the pipeline configuration after this step above, 
then the loop will go through all the elements of the given lists. The framework will provide each of them 
once for the members of the loop kernel via the function routines.pop_loop_iterator(data), see below.

**Important remark**: The data type of the enumerated iterator data required to be python list (it is planned to relax this constrains with numpy arrays and/or pandas series in the future).

### Loop and loop kernel in the yaml configuration

If the framework finds a loop in the yaml configuration (see [../mcp_frm/README.md](../mcp_frm/README.md)), it executes the specified pipeline sequentially on each element of the list of 
iterators registered at latest.

If there is no registered list of iterators or its is empty, the loop kernel will not be executed at all. The framework allows to define embedded loops in a yaml configuration, for instance lets regard the following hypotetic pipeline which is going to list the contet of the sub folders of the 
input folders given in the **input_path** element.

```
pipelines:
  - main_p:
    - list_dir:
        - { relative_path: True, output_for_iteration: True }
	- loop: list_input_dirs_p

  - list_input_dirs_pL
	- list_dir:
        - { 'only_file_names_return': True, 'output_for_iteration': True }
    - loop: processing_files_p
	
  - processing_files_p:
	- print: ~
```

### Accessing to the current iterator within the loop kernel


```
from typing import Any
import mcp_frm.pipeline_routines as routines
...
def test2_loop_kernel(data: dict[str, Any]) -> dict[str, Any]:
	iterator = routines.pop_loop_iterator()

	# specific code part
	...

	return data
```

**Important remark**: Each iterator is availble only once from the root kernel pipeline (Subsequent cases the *function routines.pop_loop_iterator* returns with 'None' value).

## Generaly Implemented Routines

### Best practice

A python function can be implemented in a general way that they are prepared to use either default input, configurable arguments or iterator, if they are available: 

```
from typing import Any
import mcp_frm.pipeline_routines as routines
from mcp_general_functions import constants
...
def func_with_arguments_given_in_config(data: dict[str, Any]) -> dict[str, Any]:
	iterator = routines.pop_loop_iterator()
	meta = routines.get_meta_data(data)
	# default_arguments_values
	arg = {
		'input': constants.DEFAULT_IO_DATA_LABEL,
		'output': constants.DEFAULT_IO_DATA_LABEL,
	}
	# merging default values with current argument values
	if meta[constants.ARGUMENTS]:
		arg = arg | meta[constants.ARGUMENTS]
	# if the function part of a loop
	if iterator:
		arg['input'] = iterator

	# specific code part
	...

	routines.set_meta_in_data(data, meta)
	return data
```

### Already implemented routines

Some generaly implemented logics (e.g.: reading/writing csv/parquet files or accessing influx/timescale db) have already been available in the following source files:
* [mcp_general_io.py](mcp_general_io.py)
* [mcp_general_db.py](mcp_general_db.py)


