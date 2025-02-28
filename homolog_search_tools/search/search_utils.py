from typing import Callable, List

ACCESSION_ID = str
ACCESSION_IDS = List[ACCESSION_ID]
ACCESSION = ACCESSION_ID | ACCESSION_IDS
UniProtRecord = dict

def batch_request(request_func:Callable, accession, chunk_size:int=500):
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
        out.extend(request_func(chunk))
    return out