import unittest
from unittest.mock import patch, Mock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.retry_handler import RetryHandler
import requests


class TestRetryHandler(unittest.TestCase):
    def setUp(self):
        self.handler = RetryHandler(max_retries=3, backoff_factor=1)

    @patch("src.retry_handler.requests.get")
    def test_successful_get(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = self.handler.get("https://example.com")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(mock_get.call_count, 1)

    @patch("src.retry_handler.requests.get")
    def test_retry_on_429_with_retry_after(self, mock_get):
        # First response: 429
        mock_429 = Mock()
        mock_429.status_code = 429
        mock_429.headers = {"Retry-After": "1"}
        mock_429.raise_for_status.side_effect = requests.exceptions.HTTPError()

        # Second response: 200
        mock_200 = Mock()
        mock_200.status_code = 200
        mock_200.raise_for_status.return_value = None

        mock_get.side_effect = [mock_429, mock_200]

        result = self.handler.get("https://example.com")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(mock_get.call_count, 2)

    @patch("src.retry_handler.requests.get")
    def test_request_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

        result = self.handler.get("https://example.com")
        self.assertIsNone(result)
        self.assertEqual(mock_get.call_count, 1)

if __name__ == "__main__":
    unittest.main()