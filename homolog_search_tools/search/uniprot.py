import requests
import json
import sys

from typing import List, Callable

ACCESSION_ID = str
ACCESSION_IDS = List[ACCESSION_ID]
ACCESSION = ACCESSION_ID | ACCESSION_IDS
UniProtRecord = dict

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
        
        def batch_request(request_func:Callable, data, chunk_size:int):
            """
            Batch run the request_func.

            Parameters
            ----------
            - request_func: Callable: request function to run in batches.
            - chunk_size: int: batch size.

            Reqturns
            --------
            : : concatenated output of the request function.
            """
            out = []
            for i in range(0, len(data), chunk_size):
                chunk = data[i:i+chunk_size]
                out.append(request_func(chunk))
            return out

        def uniprot_request_function(accession):
            params = {
                "accessions": "".join(accession),
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
            base_url = "https://rest.uniprot.org/uniprotkb/accessions"

            response = requests.get(base_url, headers=headers, params=params)
            if not response.ok:
                response.raise_for_status()
                sys.exit()
            return response.json()

        
        records = uniprot_request_function(accession=accession)
        return records