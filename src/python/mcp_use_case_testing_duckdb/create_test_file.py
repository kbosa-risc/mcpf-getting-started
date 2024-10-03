import pandas as pd
import numpy as np

N = 5_000_000  # Anzahl der Zeilen
data = pd.DataFrame({
    'id': np.arange(N),
    'value1': np.random.rand(N),
    'value2': np.random.rand(N)
})

data.to_csv(r"C:\Workspace\mjahn\risc_dse\configurable_pipeline_frm\src\python\mcp_use_case_testing_duckdb\testing_csv.csv")