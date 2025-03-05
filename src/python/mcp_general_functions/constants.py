from mcp_frm.pipeline_constants import ARG_KEYWORD_ARGUMENTS as ARGUMENTS # noqa: F401

DEFAULT_IO_DATA_LABEL = 'LAST'
DEFAULT_OUTPUT_FILE = 'FILE_OUTPUT'

class DB_CONNECTION:
    host = "127.0.0.1"
    database = "postgres"
    user = "postgres"
    password = "postgres"
    port = 5444

class FILE_IMPORT:
    table_name = "csv_file"
    
class CSV_FILE_STRUCTURE:
    columns = {
        "id": "int",
        "value1": "float",
        "value2": "float",
    }