import mcp_frm.pipeline_routines as routines
import pandas as pd
from typing import Any
import mcp_general_functions.constants as constants
import mcp_general_functions.helper as helper
from influxdb_client.client import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

from sqlalchemy import create_engine
import psycopg2
from io import StringIO


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


def postgres_csv_write(data: dict[str, Any]) -> dict[str, Any]:
    """
    Copy a CSV file into a PostgreSQL table using the COPY command.
    Yaml args:
                'input':            it is a label in "data", which identifies the input data
                                    (given in terms of pandas dataframe),
                                    by default it is the value identified with the label
                                    constants.DEFAULT_IO_DATA_LABEL (if it is a string)

            Returns in data:
                'output':   Not implemented yet!
                            it should be  a label in 'data' which identifies the output
                            (the content of the input pandas dataframe in pandas dataframe),
                            by default it is constants.DEFAULT_IO_DATA_LABEL
    """
    meta = routines.get_meta_data(data)
    arg = {
        'input': constants.DEFAULT_IO_DATA_LABEL,
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]

    # Establishing the connection to the database
    
    table_name = constants.FILE_IMPORT.table_name
    db_config = constants.DB_CONNECTION
    csv_file_path = constants.FILE_IMPORT.csv_file_path

    conn = psycopg2.connect(
        host=db_config.host,
        database=db_config.database,
        user=db_config.user,
        password=db_config.password,
        port=db_config.port
    )
    
    # Create a cursor object
    cursor = conn.cursor()
    
    try:  
        with open(csv_file_path, "r") as f:
            cursor.copy_expert(f'COPY {table_name} FROM STDIN WITH CSV HEADER', f)
        # Commit the transaction to make sure the changes are saved
        conn.commit()
        print(f"Data from {csv_file_path} has been copied to {table_name}")
    
    except Exception as e:
        # If something goes wrong, roll back the transaction
        conn.rollback()
        print(f"Error occurred: {e}")
    
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

def df_to_filelike_to_postgres(data: dict[str, Any]) -> dict[str, Any]:
    """
    Copy a df via a Filelike object into a PostgreSQL table using the COPY command.
    Yaml args:
                'input':            it is a label in "data", which identifies the input data
                                    (given in terms of pandas dataframe),
                                    by default it is the value identified with the label
                                    constants.DEFAULT_IO_DATA_LABEL (if it is a string)

            Returns in data:
                'output':   Not implemented yet!
                            it should be  a label in 'data' which identifies the output
                            (the content of the input pandas dataframe in pandas dataframe),
                            by default it is constants.DEFAULT_IO_DATA_LABEL
    """
    meta = routines.get_meta_data(data)
    arg = {
        'input': constants.DEFAULT_IO_DATA_LABEL
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]

    helper.create_db_table_if_not_exists()
    temp_csv_obejct = StringIO()
    df = data[arg['input']]
    df.to_csv(temp_csv_obejct, index=False)
    temp_csv_obejct.seek(0)
    csv_file_path = constants.FILE_IMPORT.csv_file_path
    table_name = constants.FILE_IMPORT.table_name
    db_config = constants.DB_CONNECTION


    conn = psycopg2.connect(
        host=db_config.host,
        database=db_config.database,
        user=db_config.user,
        password=db_config.password,
        port=db_config.port
    )
    
    # Create a cursor object
    cursor = conn.cursor()
    
    try:
        cursor.copy_expert(f'COPY {table_name} FROM STDIN WITH CSV HEADER', temp_csv_obejct)
        
        # Commit the transaction to make sure the changes are saved
        conn.commit()
        print(f"Data from {csv_file_path} has been copied to {table_name}")
        
    except Exception as e:
        # If something goes wrong, roll back the transaction
        conn.rollback()
        print(f"Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

        
    routines.set_meta_in_data(data, meta)
    return data
