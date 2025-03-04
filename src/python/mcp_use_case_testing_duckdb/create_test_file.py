import pandas as pd
import numpy as np
import mcp_frm.pipeline_constants as constants
import mcp_frm.pipeline_routines as routines
import os
from typing import Any

def create_test_csv_data(data: dict[str, Any]) -> dict[str, Any]:
    """generate random csv data

    Args:
        data (dict[str, Any]): _description_

    Returns:
        dict[str, Any]: _description_
    """
    # general code part 2/1
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)
    # default_arguments_values
    arg = {
        'input': constants.DEFAULT_IO_DATA_LABEL,
        'output': constants.DEFAULT_IO_DATA_LABEL,
    }
    # merging default values with current argument values
    if meta[constants.ARG_KEYWORD_ARGUMENTS]:
        arg = arg | meta[constants.ARG_KEYWORD_ARGUMENTS]
    # if the function part of a loop
    if iterator:
        arg['input'] = iterator
    path = constants.CSV_NAME_PATH
    if not os.path.exists(path):
        N = 2_500_000  # row count
        dataframe = pd.DataFrame({
            'id': np.arange(N),
            'value1': np.random.rand(N),
            'value2': np.random.rand(N),
        })

        dataframe.to_csv(path, index=False)
    routines.set_meta_in_data(data, meta)
    return data
