"""General (helper) functions for module and sub-modules."""

import subprocess
import os
from io import StringIO
from typing import List, Tuple, Union
import pandas as pd

Fasta = Union[os.PathLike, str, StringIO]
SequenceData = Union[Fasta, pd.DataFrame]

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
        return output.stdout
    except subprocess.CalledProcessError as e:
        print("Status : FAIL", e.returncode, e.output)
        return e.output

def handle_sequence_data(path_or_dataframe:SequenceData, temp_path:Fasta,
                         **kwarg
                        ):
    """
    Function to handle amino acid sequence data formats - both fasta files 
    or DataFrames containing sequence data.
    """
    if isinstance(path_or_dataframe, Fasta):
        return path_or_dataframe
    if isinstance(path_or_dataframe, pd.DataFrame):
        write_fasta(path_or_dataframe, temp_path, **kwarg)
        return temp_path
    raise ValueError(
            "Unrecognized data type, requires either path to fasta file or dataframe."
        )

def write_fasta(df:pd.DataFrame, path_or_buf:Fasta,
                header_col:str='Header', sequence_col:str='Sequence'
                ) -> None:
    """
    Writes fasta file from DataFrame.
    """
    with open(path_or_buf, "w+", encoding="utf-8") as fastafile:
        for _, row in df.iterrows():
            fastafile.write(f">{row[header_col]}\n{row[sequence_col]}\n")

def read_fasta(path_or_buf:Fasta) -> Tuple[List[str], List[str]]:
    """
    Reads fasta file into two list: a headers list and a sequence list.
    """
    headers, seqs = [], []
    with open(path_or_buf, "r", encoding="utf-8") as fastafile:
        seq = []
        for line in fastafile.readlines():
            line = line.strip()
            if line.startswith(">") and not seq:
                headers.append(line[1:])
            elif line.startswith(">"):
                headers.append(line[1:])
                seqs.append(''.join(seq))
                seq = []
            else:
                seq.append(line)
        seqs.append(''.join(seq))
    return headers, seqs
