import unittest
from core import token_


class TestToken(unittest.TestCase):

    def test_equal(self):
        self.assertEqual(1, 1)

    def test_generate_token(self):
        result = token_.create_access_token()
        self.assertIsInstance(result, str)
