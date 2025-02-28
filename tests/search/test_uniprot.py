from homolog_search_tools.search.uniprot import UniProtRequest
from homolog_search_tools.search.search_utils import UNIPROT_REQUEST_FIELDS

def test_UniProtRequest_init():
    uniprot = UniProtRequest('example@email.com')
    assert uniprot
    assert uniprot.email == 'example@email.com'
    assert uniprot.fields == UNIPROT_REQUEST_FIELDS

def test_UniProtRequest_fetch_records():
    example_records = [
        {
            'entryType': 'UniProtKB reviewed (Swiss-Prot)', 'primaryAccession': 'P01308', 
            'uniProtkbId': 'INS_HUMAN', 
            'extraAttributes': {'uniParcId': 'UPI00000017EA'}}, 
        {
            'entryType': 'UniProtKB reviewed (Swiss-Prot)', 'primaryAccession': 'P05067', 
            'uniProtkbId': 'A4_HUMAN', 
            'extraAttributes': {'uniParcId': 'UPI000002DB1C'}}
    ]
    uniprot = UniProtRequest('example@email.com')
    uniprot.set_request_fields(['id'])
    assert uniprot.fetch_records(['P01308','P05067']) == example_records