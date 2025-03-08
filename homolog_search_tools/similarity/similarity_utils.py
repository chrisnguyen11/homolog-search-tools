"""Helper functions for the similarity sub-module."""

import pandas as pd
import numpy as np

def compute_log_evalue(evalues):
    """
    From E-values, apply log10 transformation. 
    For E-values with value 0, replace with min (not zero) E-value.

    Parameters
    ----------
    - : np.array: float: E-values

    Returns
    -------
    - : np.array: float: log10 E-values
    """
    log_evalue = - np.log10(evalues)
    max_log_evalue = log_evalue[~np.isinf(log_evalue)].max()
    return np.where(np.isinf(log_evalue), max_log_evalue, log_evalue)

def read_tblastout(path_or_buff, sep:str="\t") -> pd.DataFrame:
    """
    Parses blast standard output.

    Parameters
    ----------
    - path_or_buff: path to tblastout file. 
    - sep: str: separator character.

    Returns
    -------
    pd.DataFrame: 
    """
    tblast_columns = [
        "Query_Accession", "Target_Accession", "Percent_Identity", "Alignment_Length",
        "Mismatches", "Gap_Openings", "Query_Start", "Query_End", "Target_Start", "Target_End",
        "E_Value", "Bit_Score"
    ]
    tblast_columns_float = [
        "Percent_Identity","E_Value", "Bit_Score"
    ]
    tblast_columns_int = [
        "Alignment_Length","Mismatches", "Gap_Openings", "Query_Start", "Query_End", 
        "Target_Start", "Target_End"
    ]
    df =  pd.read_csv(path_or_buff, sep=sep, names=tblast_columns)
    df[tblast_columns_float] = df[tblast_columns_float].astype(float)
    df[tblast_columns_int] = df[tblast_columns_int].astype(int)
    df["Log_E_Value"] = compute_log_evalue(df["E_Value"])
    return df.sort_values("Log_E_Value", ascending=False)
