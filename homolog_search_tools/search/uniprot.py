"""Sub-module to interact with UniProt REST API."""

import sys
from typing import List
import requests
import pandas as pd
from .search_utils import Accession, AccessionId, UniProtRequestFields, UniProtRecord, batch_request

class UniProtRequest:
    "Class to interact with the UniProt REST API."
    fields = UniProtRequestFields

    def __init__(self, email:str) -> None:
        """
        Initialize class to interact with the UniProt REST API.

        Parameters
        ----------
        - email: str: email address.
        
        Reference
        ---------
        - https://www.uniprot.org/help/programmatic_access
        """
        self.email = email

    def fetch_records(self, accession:Accession, **kwarg) -> List[UniProtRecord]:
        """
        Batch fetch UniProt reccord a (or many) accession id(s).

        Parameters
        ----------
        - accession: str | List[str]: UniProt accession ids.
        - **kwarg: arguments for the batch_request function.

        Returns
        -------
        - : list of UniProtRecord.
        """

        def uniprot_request_function(accession, fields):
            params = {
                "accessions": ",".join(accession),
                "fields": fields
            }
            headers = {
                "accept": "application/json"
                }
            base_url = "https://rest.uniprot.org/uniprotkb/accessions"

            response = requests.get(base_url, headers=headers, params=params, timeout=500)
            if not response.ok:
                response.raise_for_status()
                sys.exit()
            return response.json()['results']

        if isinstance(accession, AccessionId):
            accession = [accession]
        records = batch_request(
            uniprot_request_function, accession=accession, **kwarg, fields=self.fields)
        return records

    def set_request_fields(self, fields:List) -> None:
        "Overwrites default request fields. Used for testing."
        self.fields = fields

def uniprotrecords_to_dataframe(records:List[UniProtRecord]) -> pd.DataFrame:
    """
    Reformats UniProtRecord(s) into flatten DataFrame.
    """
    out = []
    for record in records:
        parsed_record = {
            # Names & Taxonomy
            "primaryAccession": record["primaryAccession"],
            "uniProtkbId": record["uniProtkbId"],
            "genes": gene_sanitize(record),
            "organism_scientificName": record["organism"]["scientificName"],
            "organism_commonName": record.get("organism").get("commonName"),
            "taxonId": record["organism"]["taxonId"],
            "proteinDescription": protein_description_sanitize(record),
            # Sequences
            "sequence": record["sequence"]["value"],
            "sequenceLength": record["sequence"]["length"],
            "sequencemolWeight": record["sequence"]["molWeight"],
            "sequenceVersion": record["entryAudit"]["sequenceVersion"],
            # Function
            # Miscellaneous
            "annotationScore": record["annotationScore"],
            "proteinExistence": record["proteinExistence"],
            "uniParcId": record["extraAttributes"]["uniParcId"],
            # Interaction
            "Interaction": comment_sanitize(record, "INTERACTION"),
            "Subunit": comment_sanitize(record, "SUBUNIT"),
            # Gene Ontology (GO)
            "GO": references_sanitize(record["uniProtKBCrossReferences"], "GO"),
            # Subcellular location
            "SubcellularLocation": comment_sanitize(record, "SUBCELLULAR LOCATION"),
            # Structure
            "PDBAccession": references_sanitize(record["uniProtKBCrossReferences"], "PDB"),
            # Family and domain.
            "CDD": references_sanitize(record["uniProtKBCrossReferences"], "CDD"),
            "DisProt": references_sanitize(record["uniProtKBCrossReferences"], "DisProt"),
            "Gene3D": references_sanitize(record["uniProtKBCrossReferences"], "Gene3D"),
            "HAPMAP": references_sanitize(record["uniProtKBCrossReferences"], "HAPMAP"),
            "InterPro": references_sanitize(record["uniProtKBCrossReferences"], "InterPro"),
            "NCBIfam": references_sanitize(record["uniProtKBCrossReferences"], "NCBIfam"),
            "PANTHER": references_sanitize(record["uniProtKBCrossReferences"], "PANTHER"),
            "Pfam": references_sanitize(record["uniProtKBCrossReferences"], "Pfam"),
            "PRINTS": references_sanitize(record["uniProtKBCrossReferences"], "PRINTS"),
            "PROSITE": references_sanitize(record["uniProtKBCrossReferences"], "PROSITE"),
            "SFLD": references_sanitize(record["uniProtKBCrossReferences"], "SFLD"),
            "SMART": references_sanitize(record["uniProtKBCrossReferences"], "SMART"),
            "SUPFAM": references_sanitize(record["uniProtKBCrossReferences"], "SUPFAM"),
        }
        out.append(parsed_record)
    return pd.DataFrame(out)

def gene_sanitize(record):
    "Sanitize genes."
    gene = []
    if record.get("genes"):
        gene = [
            gene["geneName"]["value"] for gene in record["genes"] if gene.get("geneName")
        ]
    return gene

def references_sanitize(references, database):
    "Sanitize references."
    out = []
    for reference in references:
        if reference["database"] == database:
            out.append(reference["id"])
    return out

def protein_description_sanitize(record):
    "Sanitize proteinDescription."
    protein_description = None
    if record["proteinDescription"].get("recommendedName"):
        protein_description = record["proteinDescription"]["recommendedName"]["fullName"]["value"]
    return protein_description

def comment_sanitize(record, comment_type):
    "Sanitize comments."
    out = []
    for comment in record["comments"]:
        if comment_type  == "INTERACTION" and \
            comment["commentType"] == "INTERACTION":
            for interaction in comment['interactions']:
                out.append(interaction["interactantTwo"]["uniProtKBAccession"])
        elif comment_type  == "SUBUNIT" and \
            comment["commentType"] == "SUBUNIT":
            for text in comment['texts']:
                out.append(text["value"])
        elif comment_type  == "SUBCELLULAR LOCATION" and \
            comment["commentType"] == "SUBCELLULAR LOCATION":
            for location in comment['subcellularLocations']:
                out.append(location["location"]["value"])
    return out
