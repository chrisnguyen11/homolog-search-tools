"""Importing submodules."""

# from . import search
# from . import similarity
# from . import utils

# __all__ = [
#     "search",
#     "similarity",
#     "utils"
# ]

from search import UniProtRequest, uniprotrecords_to_dataframe
from similarity import MMseqs2
from utils import read_fasta, write_fasta