import pandas as pd
from io import BytesIO


def reader_excel(file_bytes: bytes):
    df = pd.read_excel(BytesIO(file_bytes))
    return df.to_dict(orient="records")
