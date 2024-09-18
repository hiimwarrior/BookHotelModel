import pytest
import os
import json
import pandas as pd
from unittest import mock
from io import StringIO
import requests
# Import the functions from the script you provided
from src.utils.file import load_schema, is_csv_empty, save_to_csv, download_dataset
from src.utils.config import DATASETS

@pytest.fixture
def mock_schema(tmp_path):
    schema_content = {"field1": "type1", "field2": "type2"}
    schema_file = tmp_path / "schema.json"
    with open(schema_file, "w") as f:
        json.dump(schema_content, f)
    return schema_file

@pytest.fixture
def mock_csv_file(tmp_path):
    csv_content = "col1,col2\nval1,val2"
    csv_file = tmp_path / "test.csv"
    with open(csv_file, "w") as f:
        f.write(csv_content)
    return csv_file

@pytest.fixture
def empty_csv_file(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.touch()
    return csv_file

# Test for load_schema function
def test_load_schema(mock_schema):
    schema = load_schema(mock_schema)
    assert schema == {"field1": "type1", "field2": "type2"}

# Test for is_csv_empty function
def test_is_csv_empty_when_file_does_not_exist():
    assert is_csv_empty("non_existing_file.csv") is True

def test_is_csv_empty_with_empty_file(empty_csv_file):
    assert is_csv_empty(str(empty_csv_file)) is True

def test_is_csv_empty_with_non_empty_file(mock_csv_file):
    assert is_csv_empty(str(mock_csv_file)) is False

# Test for save_to_csv function
def test_save_to_csv(tmp_path):
    df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    output_file = tmp_path / "output.csv"
    save_to_csv(df, file_path=output_file)

    # Verify the file was saved
    assert os.path.exists(output_file)

    # Verify content
    saved_df = pd.read_csv(output_file)
    pd.testing.assert_frame_equal(saved_df, df)

# Test for download_dataset function
@mock.patch("requests.get")
def test_download_dataset_success(mock_get, tmp_path):
    dataset_key = 'test_dataset'
    DATASETS[dataset_key] = {
        'url': 'https://example.com/data.csv',
        'destination': tmp_path / 'data.csv'
    }

    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.content = b'test data'
    mock_get.return_value = mock_response

    download_dataset(dataset_key)

    # Verify file was created
    assert os.path.exists(DATASETS[dataset_key]['destination'])

    # Verify file content
    with open(DATASETS[dataset_key]['destination'], 'rb') as f:
        assert f.read() == b'test data'

@mock.patch("requests.get")
def test_download_dataset_fail(mock_get):
    dataset_key = 'test_dataset'
    DATASETS[dataset_key] = {
        'url': 'https://example.com/data.csv',
        'destination': 'data.csv'
    }

    mock_response = mock.Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    with pytest.raises(Exception, match="Failed to download data"):
        download_dataset(dataset_key)

@mock.patch("requests.get", side_effect=requests.RequestException("Network error"))
def test_download_dataset_request_exception(mock_get):
    dataset_key = 'test_dataset'
    DATASETS[dataset_key] = {
        'url': 'https://example.com/data.csv',
        'destination': 'data.csv'
    }

    with pytest.raises(requests.RequestException):
        download_dataset(dataset_key)

# Test when dataset_key is not found in the DATASETS dictionary
def test_download_dataset_key_not_found():
    with pytest.raises(ValueError, match="Dataset 'invalid_key' not found in configuration."):
        download_dataset('invalid_key')
