from io import StringIO
from unittest.mock import call, patch, Mock, MagicMock, mock_open
import pandas as pd
import pytest
import subprocess  
from homolog_search_tools.utils._utils import cmd_run, handle_sequence_data, read_fasta, write_fasta

@patch("subprocess.run")
def test_cmd_run(mocker):
    fake_cmd = ["blastp", "-query", "test.fasta", "-subject", "test.fasta", "-outfmt", "6", "-out", "blaspt.out"]
    fake_stdout = ""

    mocker.return_value = MagicMock(
        args = fake_cmd,
        stdout="",
        stderr="",
        returncode=0
    )

    output = cmd_run(fake_cmd)

    # assert subprocess.run(...) is called with the correct parameters
    mocker.assert_called_once_with(fake_cmd, capture_output=True, text=True, check=True)
    
    # assert output
    assert output == fake_stdout

@patch("homolog_search_tools.utils._utils.write_fasta")
def test_handle_sequence_data_dataframe(mocker):
    fake_df = pd.DataFrame({
        "Header": {0: "sequence 1", 1: "sequence 2"},
        "Sequence": {0: "AMINOACID", 1: "NEXTSEQUENCE"}
    })
    fake_file_name = "test.fasta"
    
    mock_response = Mock()
    mock_response.return_value = fake_file_name
    mocker.return_value = mock_response

    file_name = handle_sequence_data(fake_df, fake_file_name)

    # assert write_fasta(...) is called once
    mocker.assert_called_once_with(fake_df, fake_file_name)

    # assert results
    assert file_name == fake_file_name

@patch("homolog_search_tools.utils._utils.write_fasta")
def test_handle_sequence_data_fasta_file(mocker):
    fake_file_name = "test.fasta"
    
    mock_response = Mock()
    mock_response.return_value = fake_file_name
    mocker.return_value = mock_response

    file_name = handle_sequence_data(fake_file_name, fake_file_name)

    # assert write_fasta(...) is called once
    mocker.assert_not_called()

    # assert results
    assert file_name == fake_file_name

def test_handle_sequence_data_error():
    fake_file_name = "test.fasta"
    fake_data = 1

    with pytest.raises(ValueError, match="Unrecognized data type, requires either path to fasta file or dataframe."):
        handle_sequence_data(fake_data, fake_file_name)

@patch("builtins.open", new_callable=mock_open)
def test_read_fasta(mock_file):
    fake_file_name = "test.fasta"
    fake_file_content = StringIO(">sequence 1\nAMINO\nACID\n>sequence 2\nNEXT\nSEQUENCE\n\n")
    fake_headers = ["sequence 1", "sequence 2"]
    fake_seqs = ["AMINOACID", "NEXTSEQUENCE"]

    mock_file.return_value = fake_file_content
    data = read_fasta(fake_file_name)

    # assert open(...) with correct parameters
    mock_file.assert_called_once_with(fake_file_name, "r", encoding="utf-8")

    # assert contents of parsed file 
    assert data == (fake_headers, fake_seqs)

@patch("builtins.open", new_callable=mock_open)
def test_write_fasta(mock_file):
    fake_df = pd.DataFrame({
        "Header": {0: "sequence 1", 1: "sequence 2"},
        "Sequence": {0: "AMINOACID", 1: "NEXTSEQUENCE"}
    })
    fake_file_name = "test.fasta"
    fake_calls = [call(">sequence 1\nAMINOACID\n"), call(">sequence 2\nNEXTSEQUENCE\n")]

    write_fasta(fake_df, fake_file_name)

    # assert open(...) with correct parameters
    mock_file.assert_called_once_with(fake_file_name, "w+", encoding="utf-8")
    
    # assert number of write(...) calls
    assert mock_file().write.call_count == 2

    # assert contents of write(...) calls
    calls = mock_file().write.mock_calls
    assert calls == fake_calls