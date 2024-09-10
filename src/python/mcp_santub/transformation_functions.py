import math
import os
import sys

import numpy as np
import pandas

import mcp_frm.pipeline_routines as routines
from typing import Any
import mcp_general_functions.constants as constants
import pandas as pd


def extract_overall_grades(df: pd.DataFrame) -> dict[str, int]:
    ret_val = {}
    is_grade_column_identified = False
    grade_column_index = -1
    is_year_column_identified = False
    for nr, row in df.iterrows():
        if nr == 0:
            if str(row.iat[8]).lower().startswith('overall'):
                grade_column_index = 8
                is_grade_column_identified = True
            elif str(row.iat[9]).lower().startswith('overall'):
                grade_column_index = 9
                is_grade_column_identified = True
        elif is_grade_column_identified and str(row.iat[1]).lower().endswith('jahr'):
            is_year_column_identified = True
        elif is_year_column_identified and str(row.iat[1]) != 'nan' and str(row.iat[grade_column_index]) != 'nan':
            ret_val[str(row.iat[1])[:4]] = row.iat[grade_column_index]
        elif str(row.iat[1]) == 'nan':
            break
    return ret_val



def get_object_name(data: dict[str, Any]) -> dict[str, Any]:
    meta = routines.get_meta_data(data)
    iterator = routines.pop_loop_iterator()
    if iterator:
        data[constants.DEFAULT_IO_DATA_LABEL] = iterator
        tmp_str = iterator.removesuffix(".xlsx").removesuffix("_neu")
        data['object_name'] = " ".join(tmp_str.split("InspB_")[-1].split("_")[0:-1])
        data[constants.DEFAULT_OUTPUT_FILE] = data['object_name'] + ".parquet"
        data['dir_name'] = iterator.split('\\')[-2]
        # df[(df == 'banana').any(axis=1)]
        y = data['coordinates'][data['coordinates']['object_name'] == data['object_name']].iloc[0]['Y']
        x = data['coordinates'][data['coordinates']['object_name'] == data['object_name']].iloc[0]['X']
        year = data['coordinates'][data['coordinates']['object_name'] == data['object_name']].iloc[0]['Baujahr']
        data['coords'] = [y, x]
        data['year_of_building'] = year
    return data


def creating_list_of_build_parts(data: dict[str, Any]) -> dict[str, Any]:
    meta = routines.get_meta_data(data)
    df: pandas.DataFrame = data[constants.DEFAULT_IO_DATA_LABEL]
    list_of_build_parts = list(dict.fromkeys(df[meta['header'][4]]))
    routines.register_loop_iterator_list(list_of_build_parts)
    routines.set_meta_in_data(data, meta)
    return data


def selecting_data_of_build_parts(data: dict[str, Any]) -> dict[str, Any]:
    meta = routines.get_meta_data(data)
    iterator = routines.pop_loop_iterator()
    if iterator:
        df: pandas.DataFrame = data[constants.DEFAULT_IO_DATA_LABEL]
        build_part_data = df[df[meta['header'][4]] == iterator]
        output = build_part_data[
            [meta['header'][1],
             meta['header'][0],
             meta['header'][2],
             meta['header'][3],
             meta['header'][5],
             meta['header'][6],
             meta['header'][7],
             meta['header'][11],
             meta['header'][13]]]
        data['current_build_part_data'] = output # .set_index(
        #    [meta['header'][1],
        #     meta['header'][0],
        #     meta['header'][3],
        #     meta['header'][5],
        #     meta['header'][6]]
        #)
        filename = (str(output[meta['header'][3]].iat[0]) + "_" + iterator + ".parquet")
        data['dir_name'] = data['object_name']
        data[constants.DEFAULT_OUTPUT_FILE] = ((os.path.join(
            data['object_name'],
            filename)).lower().replace(" ","_").replace("ä","ae").replace("ö","oe").replace("ü","ue"))
        # print(data['current_build_part_data'])
    return data


def process_worksheet_data(data: dict[str, Any]) -> dict[str, Any]:
    meta = routines.get_meta_data(data)
    columns: list = meta['header']
    default_note = meta['default_value_note']
    all_sheet_data = []
    first = True
    overall_grades = {}
    for sheet_name in data[constants.DEFAULT_IO_DATA_LABEL]:
        current_overall_grade = np.nan
        df: pd.DataFrame = data[constants.DEFAULT_IO_DATA_LABEL][sheet_name]
        if first:
            overall_grades = extract_overall_grades(df)
            first = False
            continue
        year = df.columns[0]
        if str(year)[:4] in overall_grades:
            current_overall_grade = overall_grades[str(year)[:4]]
        df.reset_index()
        current_pos = 0
        current_build_part = ''
        current_sum_note = 0
        current_location = ''
        is_single_row_was_written = False
        for nr, row in df.iterrows():
            if nr == 0 or nr == 1 or nr == 2:
                continue
            elif not math.isnan(row.iat[0]):
                current_pos = row.iat[0]
                current_build_part = row.iat[1]
                current_sum_note = row.iat[8]
                if current_sum_note == '..' or current_sum_note == '…':  # fix some typos
                    current_sum_note = 0
                is_single_row_was_written = False
                continue
            else:
                counter = 0
                output_entry = [year, data['object_name'], data['year_of_building'], current_pos, current_build_part]
                # if not current_sum_note:    # Correct the typo in the sum note from the next line
                #    current_sum_note = row.iat[8]
                nr_of_injuries = row.iat[4]
                if nr_of_injuries == 0:         # if the nr of injuries 0, then the note is 0
                    row.iat[8] = default_note
                if not current_location or str(row.iat[2]) != 'nan':  # use the location value from the previous line
                    current_location = row.iat[2]
                else:
                    row.iat[2] = current_location
                if str(row.iat[8]) == 'nan':   # if the note does not exist, use the overall note
                    row.iat[8] = current_sum_note
                for index in range(row.size):
                    if counter > 1:
                        output_entry.append(row.iat[index])
                    else:
                        counter += 1
                output_entry.append(current_sum_note)
                output_entry.append(data['coords'][0])
                output_entry.append(data['coords'][1])
                output_entry.append(current_overall_grade)
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






