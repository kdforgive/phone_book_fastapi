import unittest
from unittest.mock import patch, mock_open
from unittest import mock
from logs import logging_config
import json


class TestSetupLogging(unittest.TestCase):
    read_data = json.dumps({'a': 1, 'b': 2, 'c': 3})

    def test_setup_logging_return_type(self):
        result = logging_config.get_logging_config()
        self.assertIsInstance(result, dict)

    # def test_setup_logging_compare_returned_dict(self):
    #     with mock.patch('builtins.open', mock.mock_open(read_data=self.read_data)):
    #         result = json.dumps(logging_config.get_logging_config())
    #     self.assertEqual(result, self.read_data)

    @patch('builtins.open', mock_open(read_data=read_data))
    def test_setup_logging_compare_returned_dict1(self):
        result = json.dumps(logging_config.get_logging_config())
        self.assertEqual(result, TestSetupLogging.read_data)

    # @patch('logs.logging_config.get_logging_config')
    # def test_setup_logging_compare_returned_dict3(self, mocked_object):
    #     read_data = {'a': 1, 'b': 2, 'c': 3}
    #     mocked_object.return_value = read_data
    #     result = logging_config.get_logging_config()
    #     self.assertEqual(result, read_data)

    @patch('builtins.open')
    def test_setup_logging_file_does_not_exist(self, mocked_object):
        mocked_object.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            logging_config.get_logging_config()
