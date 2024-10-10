import pandas as pd
import mcp_general_functions.constants as constants
import psycopg2


def vlookup(
    search_value: float, table: pd.DataFrame, index_column: int, target_column: int
):
    """
    Performs a vertical lookup (similar to Excel's VLOOKUP function) to find a value in a DataFrame.

    Args:
        search_value (float): The value to search for in the index column.
        table (pd.DataFrame): The DataFrame containing the data.
        index_column (int): The index (column number) to search within.
        target_column (int): The column number from which to retrieve the value.

    Returns:
        float: The value found in the target column corresponding to the search value.
                If the search value is not found, returns 0.
    """
    # Get column names
    columns = table.columns

    # Get the name of the index column and target column
    index_column_name = columns[index_column - 1]
    target_column_name = columns[target_column - 1]

    # Convert ',' to '.' and convert to float
    table = table.replace(",", ".", regex=True).astype(float)

    # Set index to the index column
    table.set_index(index_column_name, inplace=True)

    try:
        # Lookup the search value in the index column
        result = table.loc[search_value]
        # Retrieve the value from the target column
        value = result[target_column_name]
    except KeyError:
        # If search value not found, return 0
        value = 0

    return value


def convert_second_to_ms(timestamp: int):
    #  0.000625
    return timestamp * 1000 * 1000

def create_db_table_if_not_exists():
    """Creates database table if not exists

    Args:
        data (dict[str, Any]): _description_

    Returns:
        dict[str, Any]: _description_
    """

    datastructure = [i + " " + constants.CSV_FILE_STRUCTURE.columns[i] for i in constants.RUCTUR.columns]
    db_config = constants.DB_CONNECTION
    table_name = constants.FILE_IMPORT.table_name
    conn = psycopg2.connect(
        host=db_config.host,
        database=db_config.database,
        user=db_config.user,
        password=db_config.password,
        port=db_config.port
    )

    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM information_schema.tables where table_name = '{table_name}';")
        if cursor.fetchone()[0] == 0:
            print("Creating Table...")
            cursor.execute(f"CREATE TABLE {table_name} ({', '.join(datastructure)});")
        else:
            print("Table already exists.")
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
