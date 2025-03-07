import subprocess
import pandas as pd
import numpy as np
from typing import List

def cmd_run(cmd:List[str]):
    """
    Streamlines error handling of subprocess comands.

    Parameters
    ----------
    - cmd: list of str: list of command arguments.

    Returns
    -------
    - : stdout: output of cmd.
    """
    try:
        output = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Status : FAIL", e.returncode, e.output)
    except Exception as e:
        print("Status : FAIL", e)
    return output.stdout

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
    COLUMNS = [
        "Query_Accession", "Target_Accession", "Percent_Identity", "Alignment_Length",
        "Mismatches", "Gap_Openings", "Query_Start", "Query_End", "Target_Start", "Target_End",
        "E_Value", "Bit_Score"
    ]
    COLUMNS_FLOAT = [
        "Percent_Identity","E_Value", "Bit_Score"
    ]
    COLUMNS_INT = [
        "Alignment_Length","Mismatches", "Gap_Openings", "Query_Start", "Query_End", 
        "Target_Start", "Target_End"
    ]
    df =  pd.read_csv(path_or_buff, sep=sep, names=COLUMNS)
    df[COLUMNS_FLOAT] = df[COLUMNS_FLOAT].astype(float)
    df[COLUMNS_INT] = df[COLUMNS_INT].astype(int)
    df["Log_E_Value"] = compute_log_evalue(df["E_Value"])
    return df.sort_values("Log_E_Value", ascending=False)