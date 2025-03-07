import tempfile
import os
from ..utils import handle_sequence_data
from similarity_utils import cmd_run, read_tblastout

class MMseqs:
    path_to_binary = 'mmseqs'

    def __init__(self, path_to_binary=''):
        if path_to_binary:
            self.path_to_binary = path_to_binary

    def run(self, query_sequences, target_sequences) -> None:
        """
        Command wrapper for MMseqs2 all-vs-all pairwise alignment.

        Parameters
        ----------
        Returns
        -------
        - 
        Reference
        ---------
        - https://mmseqs.com/latest/userguide.pdf
        """
        # Declare temp files.
        temp_dir = tempfile.TemporaryDirectory()
        prefilter_db = os.path.join(temp_dir.name, "prefilter_db")
        alignment_db = os.path.join(temp_dir.name, "alignment_db")
        output_file = os.path.join(temp_dir.name, "output_file")
        query_db = handle_sequence_data(query_sequences, os.path.join(temp_dir.name, "query_db"))
        target_db = handle_sequence_data(target_sequences, os.path.join(temp_dir.name, "target_db"))

        # Run MMseqs2 commads.
        cmd_run([self.path_to_binary, "prefilter", query_db, target_db, prefilter_db])
        cmd_run([self.path_to_binary, "align", query_db, target_db, prefilter_db, alignment_db])
        cmd_run([self.path_to_binary, "convertalis", query_db, target_db, alignment_db, output_file])

        df = read_tblastout(output_file)
        temp_dir.cleanup()
        return df
