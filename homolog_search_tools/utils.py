import pandas as pd
import numpy as np

def write_fasta(df:pd,DataFrame, path_or_buf, header_col='Accession', sequence_col='Sequence'):
    with open(path_or_buf, "w+") as fastafile:
        for _, row in df.iterrows():
            fastafile.write(f">{row[header_col]}\n{row[sequence_col]}\n")

def read_fasta(path_or_buf):
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