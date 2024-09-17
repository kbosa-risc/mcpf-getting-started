import mcp_frm.pipeline_routines as routines
import pandas as pd
from typing import Any
import mcp_general_functions.constants as constants
from influxdb_client.client import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from sqlalchemy import create_engine


def influx_df_write(data: dict[str, Any]) -> dict[str, Any]:
    """
            It writes its input pandas dataframe into influx database.
            Yaml args:
                'input':            it is a label in "data", which identifies the input data
                                    (given in terms of pandas dataframe),
                                    by default it is the value identified with the label
                                    constants.DEFAULT_IO_DATA_LABEL (if it is a string)
                'measurement_name':

            Returns in data:
                'output':   Not implemented yet!
                            it should be  a label in 'data' which identifies the output
                            (the content of the input pandas dataframe in pandas dataframe),
                            by default it is constants.DEFAULT_IO_DATA_LABEL
    """
    meta = routines.get_meta_data(data)
    db_conf = routines.get_db_config(meta, 'influx')
    # token: str = os.environ.get("INFLUXDB_TOKEN")
    arg = {
        'input': constants.DEFAULT_IO_DATA_LABEL,
        'measurement_name': ''
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]

    with influxdb_client.InfluxDBClient(
        url=db_conf['url'], token=arg['token'], org=db_conf['org']
    ) as influx_client:
        write_api = influx_client.write_api(write_options=SYNCHRONOUS)

        # writing entire dataframe into database.
        write_api.write(
            org=db_conf['org'],
            record=data[arg['input']],
            bucket=db_conf['bucket'],
            data_frame_measurement_name=arg['measurement_name']
        )
        # general code part 2/2
    routines.set_meta_in_data(data, meta)
    return data


def timescale_df_write(data: dict[str, Any]) -> dict[str, Any]:
    """
            It writes its pandas dataframe input into timescale database.
            Yaml args:
                'input':            it is a label in "data", which identifies the input data
                                    (given in terms of pandas dataframe),
                                    by default it is the value identified with the label
                                    constants.DEFAULT_IO_DATA_LABEL (if it is a string)
                'schema':
                'table':

            Returns in data:
                'output':   Not implemented yet!
                            it should be  a label in 'data' which identifies the output
                            (the content of the input pandas dataframe in pandas dataframe),
                            by default it is constants.DEFAULT_IO_DATA_LABEL
    """
    meta = routines.get_meta_data(data)
    db_conf = routines.get_db_config(meta, 'timescale')
    arg = {
        'input': constants.DEFAULT_IO_DATA_LABEL,
        'schema': 'public',
        'table': ''
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]

    with (create_engine(db_conf['url']).connect() as con):
        data[arg['input']].to_sql(
            name=arg['table'],
            con=con,
            schema=arg['schema'],
            if_exists="append",
            index=False,
        )

    # general code part 2/2
    routines.set_meta_in_data(data, meta)
    return data
