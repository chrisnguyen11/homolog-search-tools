"""Importing submodules."""

<<<<<<< HEAD
# from . import search
# from . import similarity
# from . import utils

# __all__ = [
#     "search",
#     "similarity",
#     "utils"
# ]

# from .search.uniprot import UniProtRequest, uniprotrecords_to_dataframe
# from .similarity.mmseqs2 import MMseqs2
# from .utils.utils import read_fasta, write_fasta
=======
from . import search
from . import similarity
__all__ = ['search', 'similarity']
>>>>>>> baba1cf (pylint)
