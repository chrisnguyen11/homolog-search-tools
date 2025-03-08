"""Helper functions for the search sub-module."""

from typing import Callable, Dict, List, Union

AccessionId = str
AccessionIds = List[AccessionId]
Accession = Union[AccessionIds, AccessionIds]
UniProtRecord = Dict

UniProtRequestFields = [
    # Names & Taxonomy
    'accession', 'id', 'gene_names', 'gene_primary', 'gene_synonym',
    'organism_name', 'organism_id', 'protein_name',
    # Sequences
    'organelle', 'length', 'mass', 'sequence', 'sequence_version',
    # Function
    'ft_act_site', 'ft_binding', 'cc_catalytic_activity', 'cc_cofactor',
    'ec', 'rhea', 'temp_dependence',
    # Miscellaneous
    'annotation_score', 'protein_existence', 'reviewed', 'uniparc_id',
    # Interaction
    'cc_interaction', 'cc_subunit',
    # Gene Ontology (GO)
    'go',
    # Subcellular location
    'cc_subcellular_location', 'ft_transmem',
    # Structure
    'structure_3d',
    # Family and domain
    'xref_cdd', 'xref_disprot', 'xref_gene3d', 'xref_hamap', 'xref_interpro',
    'xref_ncbifam', 'xref_panther', 'xref_pfam', 'xref_pirsf', 'xref_prints',
    'xref_prosite', 'xref_sfld', 'xref_smart', 'xref_supfam'
]

def batch_request(request_func:Callable, accession, chunk_size:int=500, **kwarg):
    """
    Batch run the request_func.

    Parameters
    ----------
    - request_func: Callable: request function to run in batches.
    - chunk_size: int: batch size. Default: 500.

    Reqturns
    --------
    : : concatenated output of the request function.
    """
    out = []
    for i in range(0, len(accession), chunk_size):
        chunk = accession[i:i+chunk_size]
        out.extend(request_func(chunk, **kwarg))
    return out
