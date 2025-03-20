"""Sub-module to interact with DIAMOND via the command-line."""

import tempfile
import os
import pandas as pd
from ..utils._utils import SequenceData, cmd_run, handle_sequence_data
from ._similarity_utils import read_transform_tblastout

class Diamond:
    """Class to interact with DIAMOND."""

    def __init__(self, path_to_binary="diamond"):
        self.path_to_binary = path_to_binary

    def run(self, query_sequences:SequenceData, target_sequences:SequenceData) -> pd.DataFrame:
        """
        Command wrapper for Diamond to cluster a database, 
        or do an all-against-all pairwise alignment.

        Parameters
        ----------
        - query_sequences: SEQUENCE_DATA
        - target_sequences: SEQUENCE_DATA

        Returns
        -------
        - :pd.DataFrame: pairwise alignment.

        Reference
        ---------
        - https://github.com/bbuchfink/diamond/wiki
        """
        # Declare temp files.
        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = os.path.join(temp_dir.name, "output_file")
            query_db = handle_sequence_data(query_sequences,
                                            os.path.join(temp_dir.name, "query_db"))
            target_db = handle_sequence_data(target_sequences,
                                            os.path.join(temp_dir.name, "target_db"))

            # Run MMseqs2 commads.
            cmd_run([self.path_to_binary, "blastp", "--query", query_db, "--db", target_db, "--out", output_file])

            df = read_transform_tblastout(output_file)
        return df

    def run_allvsall(self, sequences:SequenceData) -> pd.DataFrame:
        """
        Equivalent to Diamond.run where the query and target are the same dataset.
        Diamond.run(query_sequences=sequences, target_sequences=sequences).
        """
        return self.run(sequences, sequences)
