import pandas as pd
from typing import Any
import mcp_frm.pipeline_routines as routines
import mcp_general_functions.constants as constants
from mcp_general_functions.helper import convert_second_to_ms


def get_simulation_id(data: dict[str, Any]) -> dict[str, Any]:
    iterator = routines.pop_loop_iterator(data)
    if iterator:
        data[constants.DEFAULT_IO_DATA_LABEL] = iterator
        data['sim_id'] = iterator.split("_", 1)[1]
    return data


def data_conversions(data: dict[str, Any]) -> dict[str, Any]:
    df = data[constants.DEFAULT_IO_DATA_LABEL]
    df.columns = df.columns.str.replace("#", "")
    df.insert(0, "Id", data['sim_id'], allow_duplicates=True)
    # timescale: format time in unix (microseconds)
    df["Time"] = convert_second_to_ms(df["Time"])
    df = df.astype({"Time": int})  # todo can we transform this to bigint?

    # influx: format time to ts based on microseconds
    # if DatabaseConfig.type is SupportedDatabases.influx:
    #    logger.debug("Influx database detected as active database. Converting unix time to timestamp.")
    df["Time"] = pd.to_datetime(df["Time"], unit="us")
    return data
