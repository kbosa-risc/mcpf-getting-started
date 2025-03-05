from datetime import datetime, timedelta, timezone
from typing import Any

import pandas as pd

import mcp_frm.pipeline_routines as routines
import mcp_use_case_fronius.constants as constants
from utils.conf import Formats


def resample_df(df: pd.DataFrame, index_value: str, frequency: float) -> pd.DataFrame:
    """This function resamples the Pandas dataframe to a given
    frequency (in this case to n Hz). The index_value becomes
    the index here and therefore must not contain any duplicate values.

    Args:
        df (pd.DataFrame): This data frame must have at least one index column and one value column.
        index_value (str): The index value must appear in the data frame and must not have duplicate values.
        frequency (float): In this case, the frequency is the highest frequency that is available in the list
                                of data frames.

    Returns:
        pd.DataFrame: Resampled data frame at the specified frequency
    """

    resample_value = str(round(frequency * 1000, 3)) + "L"
    df[index_value] = pd.TimedeltaIndex(pd.to_timedelta(df[index_value], unit="S"))
    df.set_index(index_value, inplace=True)
    try:
        if df.dtypes[0] != "float[pyarrow]":
            df = df.resample(resample_value).ffill()
        else:
            df = df.astype("float")
            df = df.resample(resample_value).interpolate(method="linear")
    except Exception:
        df = df.resample(resample_value).ffill()
    return df


def merging_columns(data: dict[str, Any]) -> dict[str, Any]:
    meta = routines.get_meta_data(data)  # code change
    end_date = datetime.strptime(meta["end_date"], Formats.date_time_format_in_CSVs).replace(
        tzinfo=timezone.utc
    )  # code change

    temp_df = pd.DataFrame()
    highest_frequency = min(data["sample_rate_dict"]["srate"])
    main_df = pd.DataFrame()
    for nr, name in enumerate(data["sample_rate_dict"]["name"]):
        temp_df = data["sample_rate_dict"]["df"][nr]
        df = temp_df.copy()
        df = resample_df(df, "time", highest_frequency)
        if nr == 0:
            main_df = df
            nr_of_entries = len(temp_df.index)
            start_date = end_date - timedelta(seconds=temp_df["time"][temp_df["time"].size - 1])
        else:
            main_df[name] = df[name]

    main_df.reset_index(inplace=True)
    main_df["time"] = main_df["time"].dt.total_seconds()  # check seconds
    series_start_epoch = pd.Series(start_date.timestamp(), index=range(nr_of_entries))
    series_end_epoch = pd.Series(end_date.timestamp(), index=range(nr_of_entries))
    main_df[constants.START_EPOCH] = series_start_epoch
    main_df[constants.END_EPOCH] = series_end_epoch
    main_df = main_df.replace("On", True)
    main_df = main_df.replace("Off", False)

    data["main_df"] = main_df  # code change
    routines.set_meta_in_data(data, meta)  # code change
    return data
