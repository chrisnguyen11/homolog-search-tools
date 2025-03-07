import pandas as pd
import numpy as np
import os
from typing import List, Tuple, Union

FASTA = Union[os.PathLike, str]
SEQUNCE_DATA = Union[FASTA, pd.DataFrame]

def handle_sequence_data(path_or_dataframe:SEQUNCE_DATA, temp_path:FASTA, 
                         **kwarg
                        ):
    """
    Function to handle amino acid sequence data formats - both fasta files or DataFrames containing sequence data.
    """
    if isinstance(path_or_dataframe, FASTA):
        return path_or_dataframe
    elif isinstance(path_or_dataframe, pd.DataFrame):
        write_fasta(path_or_dataframe, temp_path, **kwarg)
        return temp_path
    else:
        raise Exception("Unrecognized data type, requires either path to fasta file or dataframe.")

def write_fasta(df:pd.DataFrame, path_or_buf:FASTA, 
                header_col:str='Accession', sequence_col:str='Sequence'
                ) -> None:
    """
    Writes fasta file from DataFrame.
    """
    with open(path_or_buf, "w+") as fastafile:
        for _, row in df.iterrows():
            fastafile.write(f">{row[header_col]}\n{row[sequence_col]}\n")

def read_fasta(path_or_buf:FASTA) -> Tuple[List[str], List[str]]:
    """
    Reads fasta file into two list: a headers list and a sequence list.
    """
    headers, seqs = [], []
    with open(path_or_buf, "r") as fastafile:
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