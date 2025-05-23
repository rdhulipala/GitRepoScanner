import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.scanner import GitRepoScanner

class TestGitRepoScanner(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_github_data_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.json.return_value = {
            'full_name': 'nodejs/node',
            'owner': {'id': 9950313},
            'forks': 31603,
            'stargazers_count': 11359,
            'open_issues_count': 2239,
            'topics': '[javascript, js, linux, macos, mit, node, nodejs, runtime, windows]'
        }
        mock_get.return_value = mock_response
        # Initialize the GitRepoScanner class
        scanner = GitRepoScanner("nodejs/node")
        data = scanner.fetch_github_data()

        # Assert that the returned data is what we expect
        self.assertEqual(data['full_name'], 'nodejs/node')
        self.assertEqual(data['owner']['id'], 9950313)
        self.assertEqual(data['forks'], 31603)

if __name__ == '__main__':
    unittest.main()