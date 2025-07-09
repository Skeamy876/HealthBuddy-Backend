import unittest
import requests
from unittest.mock import patch, MagicMock
from health_buddy_agent.utils.tools import icd10_search_tool

class TestTools(unittest.TestCase):

    @patch('requests.get')
    def test_icd10_search_tool_success(self, mock_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = ["", ["R51"]]
        mock_get.return_value = mock_response

        # Act
        result = icd10_search_tool("headache")

        # Assert
        self.assertEqual(result, "ICD-10 codes for 'headache': [R51]")

    @patch('requests.get')
    def test_icd10_search_tool_no_codes(self, mock_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = ["", []]
        mock_get.return_value = mock_response

        # Act
        result = icd10_search_tool("asdfghjkl")

        # Assert
        self.assertEqual(result, "No ICD-10‑CM codes found for 'asdfghjkl'.")

    @patch('requests.get')
    def test_icd10_search_tool_api_error(self, mock_get):
        # Arrange
        mock_get.side_effect = requests.exceptions.RequestException("API Error")

        # Act
        result = icd10_search_tool("test")

        # Assert
        self.assertEqual(result, "An error occurred while searching for ICD-10 codes: API Error")

if __name__ == '__main__':
    unittest.main()
