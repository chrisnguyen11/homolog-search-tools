from io import StringIO
import numpy as np
import pandas as pd

from homolog_search_tools.similarity._similarity_utils import (
    _compute_log_evalue, _alphabetized_accessions, _read_tblastout, read_transform_tblastout
)

def test__compute_log_evalue():
    np.testing.assert_equal(
        _compute_log_evalue(np.array([-1, 0, 1, 2])), 
        np.array([np.nan, 0.0, 0.0, -0.3010299956639812])
    )
    np.testing.assert_equal(
        _compute_log_evalue(np.array([0.0, 0.0, 0.0, 0.0])), 
        np.array([300.0, 300.0, 300.0, 300.0])
    )
    np.testing.assert_equal(
        _compute_log_evalue(np.array([1E-10, 1E-15, 1E20, 0.000000e+00])), 
        np.array([10.0,  15.0, -20.0,  15.0])
    )

def test__alphabetized_accessions():
    assert _alphabetized_accessions({"Query_Accession": "AA", "Target_Accession": "BB"}) == ("AA", "BB")
    assert _alphabetized_accessions({"Query_Accession": "BB", "Target_Accession": "AA"}) == ("AA", "BB")
    assert _alphabetized_accessions({"Query_Accession": "AA", "Target_Accession": "AA"}) == ("AA", "AA")

def test__read_tblastout():
    fake_df = pd.DataFrame({
        'Query_Accession': {0: 'P42212'},
        'Target_Accession': {0: 'P42212'},
        'Percent_Identity': {0: 100.0},
        'Alignment_Length': {0: 238},
        'Mismatches': {0: 0},
        'Gap_Openings': {0: 0},
        'Query_Start': {0: 1},
        'Query_End': {0: 238},
        'Target_Start': {0: 1},
        'Target_End': {0: 238},
        'E_Value': {0: 0.0},
        'Bit_Score': {0: 494.0}}
    )
    fake_file = StringIO("P42212	P42212	100.000	238	0	0	1	238	1	238	0.0	494")
    assert all(_read_tblastout(fake_file) == fake_df)

def test_read_transform_tblastout():
    fake_df = pd.DataFrame({
        'Accession_1': {0: 'P42212', 1: 'P42212'},
        'Accession_2': {0: 'P42212', 1: 'Q8GHE4'},
        'Percent_Identity': {0: 100.0, 1: 99.16},
        'Alignment_Length': {0: 238, 1: 238},
        'Mismatches': {0: 0, 1: 2},
        'Gap_Openings': {0: 0, 1: 0},
        'Query_Start': {0: 1, 1: 1},
        'Query_End': {0: 238, 1: 238},
        'Target_Start': {0: 1, 1: 1},
        'Target_End': {0: 238, 1: 238},
        'E_Value': {0: 0.0, 1: 0.01},
        'Bit_Score': {0: 494.0, 1: 491.0},
        'Log_E_Value': {0: 2.0, 1: 2.0}}
    )
    fake_file = StringIO(
        "P42212	P42212	100.000	238	0	0	1	238	1	238	0.00	494\n"
        "P42212	Q8GHE4	99.160	238	2	0	1	238	1	238	0.01	491"
    )
    assert all(read_transform_tblastout(fake_file) == fake_df)
    