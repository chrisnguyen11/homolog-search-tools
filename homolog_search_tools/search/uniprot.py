import requests
import sys
from typing import List
import pandas as pd
from .search_utils import ACCESSION, UNIPROT_REQUEST_FIELDS, ACCESSION_ID, UniProtRecord, batch_request

class UniProtRequest:
    "Class to interact with the UniProt REST API."
    fields = UNIPROT_REQUEST_FIELDS

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
    
    def fetch_records(self, accession:ACCESSION, **kwarg) -> List[UniProtRecord]:
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

            response = requests.get(base_url, headers=headers, params=params)
            if not response.ok:
                response.raise_for_status()
                sys.exit()
            return response.json()['results']
        
        if isinstance(accession, ACCESSION_ID):
            accession = [accession]
        records = batch_request(uniprot_request_function, accession=accession, **kwarg, fields=self.fields)
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
            "genes": [gene["geneName"]["value"] for gene in record["genes"] if gene.get("geneName")] if record.get("genes") else [],
            "organism_scientificName": record["organism"]["scientificName"],
            "organism_commonName": record.get("organism").get("commonName"),
            "taxonId": record["organism"]["taxonId"],
            "proteinDescription": record["proteinDescription"]["recommendedName"]["fullName"]["value"] if record["proteinDescription"].get("recommendedName") else None,
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
            "Interaction": [interaction["interactantTwo"]["uniProtKBAccession"] for comment in record["comments"] if comment["commentType"] == "INTERACTION" for interaction in comment['interactions']],
            "Subunit": [text["value"] for comment in record["comments"] if comment["commentType"] == "SUBUNIT" for text in comment['texts']],
            # Gene Ontology (GO)
            "GO": [reference["id"] for reference in record["uniProtKBCrossReferences"] if reference["database"] == "GO"],
            # Subcellular location
            "SubcellularLocation": [location["location"]["value"] for comment in record["comments"] if comment["commentType"] == "SUBCELLULAR LOCATION" for location in comment['subcellularLocations']],
            # Structure
            "PDBAccession": [reference["id"] for reference in record["uniProtKBCrossReferences"] if reference["database"] == "PDB"],
            # Family and domain
            "CDD": [reference["id"] for reference in record["uniProtKBCrossReferences"] if reference["database"] == "CDD"],
            "DisProt": [reference["id"] for reference in record["uniProtKBCrossReferences"] if reference["database"] == "DisProt"],
            "Gene3D": [reference["id"] for reference in record["uniProtKBCrossReferences"] if reference["database"] == "Gene3D"],
            "HAPMAP": [reference["id"] for reference in record["uniProtKBCrossReferences"] if reference["database"] == "HAPMAP"],
            "InterPro": [reference["id"] for reference in record["uniProtKBCrossReferences"] if reference["database"] == "InterPro"],
            "NCBIfam": [reference["id"] for reference in record["uniProtKBCrossReferences"] if reference["database"] == "NCBIfam"],
            "PANTHER": [reference["id"] for reference in record["uniProtKBCrossReferences"] if reference["database"] == "PANTHER"],
            "Pfam": [reference["id"] for reference in record["uniProtKBCrossReferences"] if reference["database"] == "Pfam"],
            "PRINTS": [reference["id"] for reference in record["uniProtKBCrossReferences"] if reference["database"] == "PRINTS"],
            "PROSITE": [reference["id"] for reference in record["uniProtKBCrossReferences"] if reference["database"] == "PROSITE"],
            "SFLD": [reference["id"] for reference in record["uniProtKBCrossReferences"] if reference["database"] == "SFLD"],
            "SMART": [reference["id"] for reference in record["uniProtKBCrossReferences"] if reference["database"] == "SMART"],
            "SUPFAM": [reference["id"] for reference in record["uniProtKBCrossReferences"] if reference["database"] == "SUPFAM"],
        }
        out.append(parsed_record)
    return pd.DataFrame(out)