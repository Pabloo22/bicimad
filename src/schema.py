import pandas as pd
import pandera as pa


puerta_madrid_schema = pa.DataFrameSchema(
    index=pa.Index(pa.DateTime, name="timestamp"),
    columns={}
)
