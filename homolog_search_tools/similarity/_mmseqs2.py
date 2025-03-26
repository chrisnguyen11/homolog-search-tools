"""Sub-module to interact with MMseqs2 via the command-line."""

from typing import Dict
import tempfile
import os
import pandas as pd
from ..utils._utils import SequenceData, cmd_run, handle_sequence_data
from ._similarity_utils import read_transform_tblastout

ClusterDict = Dict[str, str]

class MMseqs2:
    """Class to interact with MMseqs."""

    def __init__(self, path_to_binary="mmseqs"):
        self.path_to_binary = path_to_binary

    def run(self, query_sequences:SequenceData, target_sequences:SequenceData) -> pd.DataFrame:
        """
        Command wrapper for MMseqs2 to compute pairwise alignment on databases.

        Parameters
        ----------
        - query_sequences: SEQUENCE_DATA
        - target_sequences: SEQUENCE_DATA

        Returns
        -------
        - :pd.DataFrame: pairwise alignment.

        Reference
        ---------
        - https://mmseqs.com/latest/userguide.pdf
        """
        # Declare temp files.
        with tempfile.TemporaryDirectory() as temp_dir:
            prefilter_db = os.path.join(temp_dir, "prefilter_db")
            alignment_db = os.path.join(temp_dir, "alignment_db")
            output_file = os.path.join(temp_dir, "output_file")
            query_db = handle_sequence_data(query_sequences,
                                            os.path.join(temp_dir, "query_db"))
            target_db = handle_sequence_data(target_sequences,
                                            os.path.join(temp_dir, "target_db"))

            # Run MMseqs2 commads.
            cmd_run([self.path_to_binary, "prefilter", query_db, target_db, prefilter_db])
            cmd_run([self.path_to_binary, "align", query_db, target_db, prefilter_db, alignment_db])
            cmd_run([self.path_to_binary, "convertalis",
                    query_db, target_db, alignment_db, output_file])

            df = read_transform_tblastout(output_file)
        return df

    def run_allvsall(self, sequences:SequenceData) -> pd.DataFrame:
        """
        Equivalent to MMseqs.run(query_sequences=sequences, target_sequences=sequences).
        """
        return self.run(sequences, sequences)
    
    def run_cluster(self, sequences:SequenceData, algorithm:str="easy-cluster") -> ClusterDict:
        """
        Generic command wrapper for MMseqs2 to cluster databases.
        
        Parameters
        ----------
        - sequences: SEQUENCE_DATA

        Returns
        -------
        - :ClusterDict: maps nodes to representative node

        Reference
        ---------
        - https://mmseqs.com/latest/userguide.pdf
        """
        if algorithm not in ["easy-cluster", "easy-linclust"]:
            raise ValueError("Invalid algorithm value.")

        # Declare temp files.
        with tempfile.TemporaryDirectory() as temp_dir:
            output_prefix = os.path.join(temp_dir, "output")
            adjacency_list = f"{output_prefix}_cluster.tsv"
            inner_temp_dir = os.path.join(temp_dir, "tmp")

            # Run MMseqs2 commads.
            cmd_run([self.path_to_binary, algorithm, sequences, output_prefix, inner_temp_dir])

            mmapper = parse_mmseqs_cluster_adjacency_list(adjacency_list)
        return mmapper

def parse_mmseqs_cluster_adjacency_list(adjacency_list:os.PathLike | str) -> ClusterDict:
    """
    Parses MMseqs easy-cluster and easy-linclust adjacency list outfiles.

    Returns
    -------
    - Dict: maps nodes to representative node
    """
    mapper = {}
    with open(adjacency_list, "r") as f:
        for line in f.readlines():
            line = line.strip().split("\t")
            mapper[line[1]] = line[0]
    return mapper