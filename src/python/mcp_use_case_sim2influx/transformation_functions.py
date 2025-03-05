from typing import Any

import pandas as pd

import mcp_frm.pipeline_routines as routines
import mcp_general_functions.constants as constants
from mcp_general_functions.helper import convert_second_to_ms
from mcp_use_case_sim2influx.constants import SupportedDatabases


def get_simulation_id(data: dict[str, Any]) -> dict[str, Any]:
    iterator = routines.pop_loop_iterator()
    if iterator:
        data[constants.DEFAULT_IO_DATA_LABEL] = iterator
        data["sim_id"] = iterator.split("_")[-1]
    return data


def data_conversions(data: dict[str, Any]) -> dict[str, Any]:
    meta = routines.get_meta_data(data)
    df = data[constants.DEFAULT_IO_DATA_LABEL]
    df.columns = df.columns.str.replace(" ", "")
    df.columns = df.columns.str.replace("#", "")
    df.insert(0, "Id", data["sim_id"], allow_duplicates=True)
    # timescale: format time in unix (microseconds)
    df["Time"] = convert_second_to_ms(df["Time"])
    df = df.astype({"Time": int})  # todo can we transform this to bigint?

    # influx: format time to ts based on microseconds
    if meta["output_db"] == SupportedDatabases.influx:
        # logger.debug("Influx database detected as active database. Converting unix time to timestamp.")
        df["Time"] = pd.to_datetime(df["Time"], unit="us")
        data[constants.DEFAULT_IO_DATA_LABEL] = df.set_index("Time")
    else:
        data[constants.DEFAULT_IO_DATA_LABEL] = df
    routines.set_meta_in_data(data, meta)
    return data
