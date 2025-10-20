import numpy as np
from homolog_search_tools.similarity._similarity_utils import _compute_log_evalue, _read_tblastout

def test_compute_log_evalue():
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

def test_read_tblastout():
    pass