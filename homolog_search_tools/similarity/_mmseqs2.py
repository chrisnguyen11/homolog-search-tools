"""Sub-module to interact with MMseqs2 via the command-line."""

import tempfile
import os
import pandas as pd
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD:homolog_search_tools/similarity/_mmseqs2.py
<<<<<<< HEAD:homolog_search_tools/similarity/_mmseqs2.py
from ..utils._utils import cmd_run, handle_sequence_data
from ._similarity_utils import read_tblastout
=======
from .utils.utils import cmd_run, handle_sequence_data
=======
from ..utils.utils import cmd_run, handle_sequence_data
>>>>>>> 9ed310e (Fix import):homolog_search_tools/similarity/mmseqs2.py
from .similarity_utils import read_tblastout
>>>>>>> 6b4b546 (Fix import):homolog_search_tools/similarity/mmseqs2.py
=======
from ..utils._utils import cmd_run, handle_sequence_data
from ._similarity_utils import read_tblastout
>>>>>>> 489da92 (Fix import)
=======
from ..utils._utils import cmd_run, handle_sequence_data
from ._similarity_utils import read_tblastout
>>>>>>> 8e7514b6915c0b1501799d517b9e669392c3594f

class MMseqs2:
    """Class to interact with MMseqs."""

    def __init__(self, path_to_binary='mmseqs'):
        self.path_to_binary = path_to_binary

    def run(self, query_sequences, target_sequences) -> pd.DataFrame:
        """
        Command wrapper for MMseqs2 to cluster a database, 
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
        - https://mmseqs.com/latest/userguide.pdf
        """
        # Declare temp files.
        with tempfile.TemporaryDirectory() as temp_dir:
            prefilter_db = os.path.join(temp_dir.name, "prefilter_db")
            alignment_db = os.path.join(temp_dir.name, "alignment_db")
            output_file = os.path.join(temp_dir.name, "output_file")
            query_db = handle_sequence_data(query_sequences,
                                            os.path.join(temp_dir.name, "query_db"))
            target_db = handle_sequence_data(target_sequences,
                                            os.path.join(temp_dir.name, "target_db"))

            # Run MMseqs2 commads.
            cmd_run([self.path_to_binary, "prefilter", query_db, target_db, prefilter_db])
            cmd_run([self.path_to_binary, "align", query_db, target_db, prefilter_db, alignment_db])
            cmd_run([self.path_to_binary, "convertalis",
                    query_db, target_db, alignment_db, output_file])

            df = read_tblastout(output_file)
        return df

    def run_allvsall(self, sequences) -> pd.DataFrame:
        """
        Equivalent to MMseqs.run(query_sequences=sequences, target_sequences=sequences).
        """
        return self.run(sequences, sequences)
