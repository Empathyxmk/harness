import unittest

class TestGsonUtilPublic(unittest.TestCase):
    def test_number_string_deserialization_public(self):
        json_num = "123"
        num = int(json_num)
        self.assertEqual(123, num)