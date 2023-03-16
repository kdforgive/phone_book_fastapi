import unittest
from core import token_


class TestToken(unittest.TestCase):

    def test_generate_token_no_args(self):
        result = token_.create_access_token()
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 120)

    def test_generate_token_with_args(self):
        token_length = 100
        result = token_.create_access_token(token_length)
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), token_length)

    def test_generate_token_length_lower_zero(self):
        token_length = -3
        result = token_.create_access_token(token_length)
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 0)

    def test_generate_token_correct_used_symbols(self):
        result = token_.create_access_token()
        all_symbols = set(list(token_.SYMBOLS_SOURCE))
        result_symbols = set(list(result))
        self.assertTrue(result_symbols.issubset(all_symbols))

    def test_generate_token_unique_token(self):
        result = token_.create_access_token()
        for _ in range(1000):
            new_result = token_.create_access_token()
            self.assertNotEqual(result, new_result)

    def test_generate_token_argument_type(self):
        with self.assertRaises(TypeError) as context:
            token_.create_access_token('abc')

    def test_generate_token_not_unique_more_then_five_times(self):
        pass
