import unittest
from unittest.mock import patch, mock_open
from data import download_dataset

class TestDownloadDataset(unittest.TestCase):
    
    @patch('requests.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_download_success(self, mock_open, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b'some data'
        
        dataset_key = 'test_dataset'
        with patch.dict('config.DATASETS', {
            dataset_key: {
                'url': 'http://example.com/test.csv',
                'destination': 'data/raw/test.csv'
            }
        }):
            download_dataset(dataset_key)
            mock_open.assert_called_once_with('data/raw/test.csv', 'wb')
            mock_open().write.assert_called_once_with(b'some data')

    @patch('requests.get')
    def test_download_failure(self, mock_get):
        mock_get.return_value.status_code = 404
        
        dataset_key = 'test_dataset'
        with patch.dict('config.DATASETS', {
            dataset_key: {
                'url': 'http://example.com/test.csv',
                'destination': 'data/raw/test.csv'
            }
        }):
            with self.assertRaises(Exception):
                download_dataset(dataset_key)

if __name__ == '__main__':
    unittest.main()
