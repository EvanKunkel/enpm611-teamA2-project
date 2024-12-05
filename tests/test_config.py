import unittest
from unittest.mock import patch, MagicMock
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config

class TestConfigModule(unittest.TestCase):

    @patch('config.os.environ')
    def test_set_parameter(self, mock_environ):
        # Mocking the environment to check if set_parameter updates it correctly
        config.set_parameter('NEW_PARAM', {'key': 'value'})

        # Checking if the correct value was set in the environment
        mock_environ.__setitem__.assert_called_with('NEW_PARAM', 'json:{"key": "value"}')

    def test_convert_to_typed_value(self):
        # Testing conversion of JSON string to Python value
        result = config.convert_to_typed_value('{"key": "value"}')
        self.assertEqual(result, {"key": "value"})  # Should be a dict
        
        # Testing when no conversion is needed (non-string values)
        result = config.convert_to_typed_value(42)
        self.assertEqual(result, 42)  # Should remain as an integer

        # Testing invalid JSON (should return the string as is)
        result = config.convert_to_typed_value('Invalid JSON')
        self.assertEqual(result, 'Invalid JSON')


if __name__ == '__main__':
    unittest.main()
