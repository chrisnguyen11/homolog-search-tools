"""Importing submodules."""

# from . import search
# from . import similarity
# from . import utils

# __all__ = [
#     "search",
#     "similarity",
#     "utils"
# ]

from .search.uniprot import UniProtRequest, uniprotrecords_to_dataframe
from .similarity.mmseqs2 import MMseqs2
from .utils.utils import read_fasta, write_fasta