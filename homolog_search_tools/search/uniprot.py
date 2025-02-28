import requests
import json
import sys
from typing import List
from .search_utils import ACCESSION, ACCESSION_ID, UniProtRecord, batch_request

class UniProtRequest:
    "Class to interact with the UniProt REST API."
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

        def uniprot_request_function(accession):
            params = {
                "accessions": ",".join(accession),
                "fields": [
                    "accession",
                    "protein_name",
                    "cc_function",
                    "ft_binding"
                ]
            }
            headers = {
                "accept": "application/json"
                }
            base_url = f"https://rest.uniprot.org/uniprotkb/accessions"

            response = requests.get(base_url, headers=headers, params=params)
            if not response.ok:
                response.raise_for_status()
                sys.exit()
            return response.json()['results']
        
        if isinstance(accession, ACCESSION_ID):
            accession = [accession]
        records = batch_request(uniprot_request_function, accession=accession, **kwarg)
        return records