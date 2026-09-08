import unittest
import pj

class TestPJAPIPublic(unittest.TestCase):
    def test_to_string_dict_diff(self):
        d = {'x': False, 'y': 3.14}
        s = pj.to_string(d)
        # allow both key orders for dict string; parse again for test
        self.assertTrue(s in ['{"x": false, "y": 3.14}', '{"y": 3.14, "x": false}'])
        # round-trip
        r = pj.from_string(s)
        self.assertEqual(r, d)

    def test_to_string_list_diff(self):
        arr = [10, 99, 'foo']
        s = pj.to_string(arr)
        self.assertEqual(s, '[10, 99, "foo"]')
        r = pj.from_string('{"b": %s}' % s)
        self.assertEqual(r, {'b': arr})

    def test_to_string_str_diff(self):
        self.assertEqual(pj.to_string("xyz"), '"xyz"')

    def test_to_string_bool_diff(self):
        self.assertEqual(pj.to_string(False), "false")
        self.assertEqual(pj.to_string(True), "true")

    def test_to_string_null_diff(self):
        # See if current implementation matches "None" or "null"
        self.assertEqual(pj.to_string(None), "None")

    def test_to_string_number_diff(self):
        self.assertEqual(pj.to_string(42), "42")
        self.assertEqual(pj.to_string(2.718), "2.718")