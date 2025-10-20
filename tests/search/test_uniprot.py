import pandas as pd
from unittest.mock import Mock, patch

from homolog_search_tools.search._uniprot import UniProtRequest, uniprotrecords_to_dataframe
from homolog_search_tools.search._search_utils import UniProtRequestFields

def test_UniProtRequest_init():
    uniprot = UniProtRequest('example@email.com')
    assert uniprot
    assert uniprot.email == 'example@email.com'
    assert uniprot.fields == UniProtRequestFields

@patch("requests.get")
def test_UniProtRequest_fetch_records(mocker):
    fake_records = [
        {
            'entryType': 'UniProtKB reviewed (Swiss-Prot)', 'primaryAccession': 'P01308', 
            'uniProtkbId': 'INS_HUMAN', 
            'extraAttributes': {'uniParcId': 'UPI00000017EA'}}, 
        {
            'entryType': 'UniProtKB reviewed (Swiss-Prot)', 'primaryAccession': 'P05067', 
            'uniProtkbId': 'A4_HUMAN', 
            'extraAttributes': {'uniParcId': 'UPI000002DB1C'}}
    ]
    mock_response = Mock()
    mock_response.json.return_value = {"results": fake_records}
    mocker.return_value = mock_response

    uniprot = UniProtRequest('example@email.com')
    uniprot.set_request_fields(['id'])
    records = uniprot.fetch_records(['P01308','P05067'])

    mocker.assert_called_with(
        'https://rest.uniprot.org/uniprotkb/accessions',
        headers={'accept': 'application/json'}, 
        params={'accessions': 'P01308,P05067', 'fields': ['id']}, 
        timeout=500
    )
    assert records == fake_records

def test_uniprotrecords_to_dataframe():
    example_record = [{
        'entryType': 'UniProtKB reviewed (Swiss-Prot)',
        'primaryAccession': 'Q8PZ49',
        'uniProtkbId': 'HACB_METMA',
        'entryAudit': {'sequenceVersion': 1},
        'annotationScore': 3.0,
        'organism': {
            'scientificName': 'Methanosarcina mazei',
            'commonName': 'Methanosarcina frisia',
            'taxonId': 192952},
        'proteinExistence': '3: Inferred from homology',
        'proteinDescription': {
            'recommendedName': {
                'fullName': {'value': 'Methanogen homoaconitase small subunit'},
                'shortNames': [{'value': 'HACN'}],
                'ecNumbers': [{
                    'evidences': [{'evidenceCode': 'ECO:0000250', 'source': 'UniProtKB', 'id': 'Q58667'}], 
                    'value': '4.2.1.114'}]},
            'alternativeNames': [{'fullName': {'value': 'Homoaconitate hydratase'}}]},
        'genes': [{
            'geneName': {'value': 'hacB'},
            'orderedLocusNames': [{'value': 'MM_0645'}]}],
        'comments': [
            {'texts': [{
                'evidences': [{'evidenceCode': 'ECO:0000250', 'source': 'UniProtKB','id': 'Q58667'}],
                'value': 'Heterotetramer of 2 HacA and 2 HacB proteins'}],
            'commentType': 'SUBUNIT'}],
        'features': [],
        'uniProtKBCrossReferences': [
            {'database': 'GO', 'id': 'GO:0004409'},
            {'database': 'GO', 'id': 'GO:0019298'},
            {'database': 'CDD', 'id': 'cd01577'},
            {'database': 'Gene3D', 'id': '3.20.19.10'},
            {'database': 'HAMAP','id': 'MF_01032'},
            {'database': 'InterPro', 'id': 'IPR015928'},
            {'database': 'InterPro', 'id': 'IPR000573'},
            {'database': 'InterPro', 'id': 'IPR033940'},
            {'database': 'InterPro', 'id': 'IPR050075'},
            {'database': 'InterPro', 'id': 'IPR011827'},
            {'database': 'NCBIfam', 'id': 'TIGR02087'},
            {'database': 'PANTHER', 'id': 'PTHR43345:SF2'},
            {'database': 'PANTHER', 'id': 'PTHR43345'},
            {'database': 'Pfam', 'id': 'PF00694'},
            {'database': 'SUPFAM', 'id': 'SSF52016'}],
        'sequence': {
            'value': 'MMENPIKGRVWKFGNDIDTDVIIPGKYLRTKDMQVFAAHAMEGIDPGFSKKAKPGDIIVAGDNFGCGSSREQAPLALKHAGIACIVAKSFARIFFRNAINIGLPLMEADIECEEGDQIEVDLLKGEVKVSGKGVFRGNKLPDFLLDMLTDGGLVAHRKKVRDQEKEESA',
            'length': 169,
            'molWeight': 18489,
            'crc64': '3E1AFAEE5EDD0CBE',
            'md5': '8A3D5F192D1BFCB786C9D44C308E70B3'},
        'extraAttributes': {'uniParcId': 'UPI000012E400'}}]
    
    example_df = {
        'primaryAccession': {0: 'Q8PZ49'},
        'uniProtkbId': {0: 'HACB_METMA'},
        'genes': {0: ['hacB']},
        'organism_scientificName': {0: 'Methanosarcina mazei'},
        'organism_commonName': {0: 'Methanosarcina frisia'},
        'taxonId': {0: 192952},
        'proteinDescription': {0: 'Methanogen homoaconitase small subunit'},
        'sequence': {0: 'MMENPIKGRVWKFGNDIDTDVIIPGKYLRTKDMQVFAAHAMEGIDPGFSKKAKPGDIIVAGDNFGCGSSREQAPLALKHAGIACIVAKSFARIFFRNAINIGLPLMEADIECEEGDQIEVDLLKGEVKVSGKGVFRGNKLPDFLLDMLTDGGLVAHRKKVRDQEKEESA'},
        'sequenceLength': {0: 169},
        'sequencemolWeight': {0: 18489},
        'sequenceVersion': {0: 1},
        'annotationScore': {0: 3.0},
        'proteinExistence': {0: '3: Inferred from homology'},
        'uniParcId': {0: 'UPI000012E400'},
        'Interaction': {0: []},
        'Subunit': {0: ['Heterotetramer of 2 HacA and 2 HacB proteins']},
        'GO': {0: ['GO:0004409', 'GO:0019298']},
        'SubcellularLocation': {0: []},
        'PDBAccession': {0: []},
        'CDD': {0: ['cd01577']},
        'DisProt': {0: []},
        'Gene3D': {0: ['3.20.19.10']},
        'HAPMAP': {0: []},
        'InterPro': {0: ['IPR015928', 'IPR000573', 'IPR033940', 'IPR050075', 'IPR011827']},
        'NCBIfam': {0: ['TIGR02087']},
        'PANTHER': {0: ['PTHR43345:SF2', 'PTHR43345']},
        'Pfam': {0: ['PF00694']},
        'PRINTS': {0: []},
        'PROSITE': {0: []},
        'SFLD': {0: []},
        'SMART': {0: []},
        'SUPFAM': {0: ['SSF52016']}}

    uniprotrecords_to_dataframe(example_record) == pd.DataFrame(example_df)
