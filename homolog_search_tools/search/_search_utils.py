"""Helper functions for the search sub-module."""

from typing import Callable, Dict, List, Union

AccessionId = str
AccessionIds = List[AccessionId]
Accession = Union[AccessionIds, AccessionIds]
UniProtRecord = Dict

UniProtRequestFields = [
    # Names & Taxonomy
    "accession", "id", "gene_names", "gene_primary", "gene_synonym",
    "organism_name", "organism_id", "protein_name",
    # Sequences
    "organelle", "length", "mass", "sequence", "sequence_version",
    # Function
    "ft_act_site", "ft_binding", "cc_catalytic_activity", "cc_cofactor",
    "ec", "rhea", "temp_dependence",
    # Miscellaneous
    "annotation_score", "protein_existence", "reviewed", "uniparc_id",
    # Interaction
    "cc_interaction", "cc_subunit",
    # Gene Ontology (GO)
    "go",
    # Subcellular location
    "cc_subcellular_location", "ft_transmem",
    # Structure
    "structure_3d",
    # Family and domain
    "xref_cdd", "xref_disprot", "xref_gene3d", "xref_hamap", "xref_interpro",
    "xref_ncbifam", "xref_panther", "xref_pfam", "xref_pirsf", "xref_prints",
    "xref_prosite", "xref_sfld", "xref_smart", "xref_supfam"
]

def batch_request(request_func:Callable, accessions:Accession, batch_size:int=500, **kwarg):
    """
    Exectues request_func in batches. Can handle potential
    unknown accession (404) errors.

    Parameters
    ----------
    - request_func: Callable: api request function to execute in batches.
    - accession: list of accessions
    - batch_size: int: batch size. Default: 500.

    Reqturns
    --------
    : : concatenated output of the request function.
    """
    output = []
    if len(accessions) == 1:
        try:
            output.extend(request_func(accessions))
        except:
            print(f"Unable to handle {accessions}")
    else:
        for i in range(0, len(accessions), batch_size):
            batch = accessions[i: i+batch_size]
            try:
                output.extend(request_func(batch))
            except:
                output.extend(batch_request(request_func, batch, batch_size//2))
    return output