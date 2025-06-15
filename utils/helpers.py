# helpers.py content
import pandas as pd
import os

def read_excel(path, sheet_name=0, cols=None):
    if os.path.exists(path):
        return pd.read_excel(path, sheet_name=sheet_name, usecols=cols, engine="openpyxl")
    return pd.DataFrame()

def write_excel(df, path, sheet_name="Sheet1"):
    df.to_excel(path, sheet_name=sheet_name, index=False, engine="openpyxl")
