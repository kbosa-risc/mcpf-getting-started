import os
import clr
import mcp_general_functions.constants as constants
from typing import Any
import pandas as pd

dll_directory = "c:\\Projects\\risc_dse\\configurable_pipeline_frm\\src\python\\mcp_use_case_dot_net\\"
dll_path = os.path.join(dll_directory, "ITS_West.Base.dll")

# Add the directory to the CLR search path
clr.AddReference(dll_path)
from ITS_West.Algorithms import AnonymizationAlgorithms


def add_new_sensor_id(data: dict[str, Any]) -> dict[str, Any]:
    instance_csharp_class = AnonymizationAlgorithms()
    output = []
    df = data[constants.DEFAULT_IO_DATA_LABEL]
    columns = df.columns
    for nr, row in df.iterrows():
        if str(row.iat[4]) != 'nan':
            row.iat[4] = int(row.iat[4])
        if str(row.iat[5]) != 'nan':
            row.iat[5] = int(row.iat[5])
        if str(row.iat[9]) != 'nan':
            row.iat[9] = int(row.iat[9])
        if str(row.iat[10]) != 'nan':
            row.iat[10] = int(row.iat[10])
        if str(row.iat[0]) == 'nan':
            if str(row.iat[5]) != 'nan':
                sensor_id = row.iat[2] + row.iat[3] + str(row.iat[5])
                row.iat[0] = int(instance_csharp_class.GetHashedDataInInt(sensor_id))
        else:
            row.iat[0] = int(row.iat[0])
        output.append(row.tolist())
    data[constants.DEFAULT_IO_DATA_LABEL] = pd.DataFrame(columns=columns, data=output)
    return data
