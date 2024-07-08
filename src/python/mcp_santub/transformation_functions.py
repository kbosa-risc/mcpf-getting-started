import math
import numpy as np
import mcp_frm.pipeline_routines as routines
from typing import Any
import mcp_general_functions.constants as constants
import pandas as pd


def get_object_name(data: dict[str, Any]) -> dict[str, Any]:
    meta = routines.get_meta_data(data)
    iterator = routines.pop_loop_iterator()
    if iterator:
        data[constants.DEFAULT_IO_DATA_LABEL] = iterator
        data['object_name'] = " ".join(iterator.split("InspB_")[-1].split("_")[0:-1])
        data[constants.DEFAULT_OUTPUT_FILE] = data['object_name'] + ".parquet"
        data['dir_name'] = iterator.split('\\')[-2]
        # df[(df == 'banana').any(axis=1)]
        y = data['coordinates'][data['coordinates']['object_name'] == data['object_name']].iloc[0]['Y']
        x = data['coordinates'][data['coordinates']['object_name'] == data['object_name']].iloc[0]['X']
        data['coords'] = [y, x]
    return data


def process_worksheet_data(data: dict[str, Any]) -> dict[str, Any]:
    meta = routines.get_meta_data(data)
    columns: list = meta['header']
    default_note = meta['default_value_note']
    all_sheet_data = []
    for sheet_name in data[constants.DEFAULT_IO_DATA_LABEL]:
        df: pd.DataFrame = data[constants.DEFAULT_IO_DATA_LABEL][sheet_name]
        year = df.columns[0]
        df.reset_index()
        current_pos = 0
        current_build_part = ''
        current_overall_note = 0
        current_location = ''
        is_single_row_was_written = False
        for nr, row in df.iterrows():
            if nr == 0 or nr == 1 or nr == 2:
                continue
            elif not math.isnan(row.iat[0]):
                current_pos = row.iat[0]
                current_build_part = row.iat[1]
                current_overall_note = row.iat[8]
                if current_overall_note == '..' or current_overall_note == '…':  # fix some typos
                    current_overall_note = 0
                is_single_row_was_written = False
                continue
            else:
                counter = 0
                output_entry = [year, data['object_name'], current_pos, current_build_part]
                # if not current_overall_note:    # Correct the typo in the overall note from the next line
                #    current_overall_note = row.iat[8]
                nr_of_injuries = row.iat[4]
                if nr_of_injuries == 0:         # if the nr of injuries 0, then the note is 0
                    row.iat[8] = default_note
                if not current_location or str(row.iat[2]) != 'nan':  # use the location value from the previous line
                    current_location = row.iat[2]
                else:
                    row.iat[2] = current_location
                if str(row.iat[8]) == 'nan':   # if the note does not exist, use the overall note
                    row.iat[8] = current_overall_note
                for index in range(row.size):
                    if counter > 1:
                        output_entry.append(row.iat[index])
                    else:
                        counter += 1
                output_entry.append(current_overall_note)
                output_entry.append(data['coords'][0])
                output_entry.append(data['coords'][1])
                if output_entry.count(np.nan) < 6:
                    all_sheet_data.append(output_entry)
                    is_single_row_was_written = True
                elif not is_single_row_was_written:
                    output_entry[10] = math.nan
                    all_sheet_data.append(output_entry)
                    is_single_row_was_written = True
    data[constants.DEFAULT_IO_DATA_LABEL] = pd.DataFrame(columns=columns, data=all_sheet_data)
    routines.set_meta_in_data(data, meta)
    return data





