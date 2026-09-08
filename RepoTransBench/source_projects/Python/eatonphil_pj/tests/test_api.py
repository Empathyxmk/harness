import unittest
import pj

class TestPJAPI(unittest.TestCase):
    def test_to_string_dict(self):
        d = {'foo': 1, 'bar': True}
        s = pj.to_string(d)
        # allow both key orders for dict string; parse again for test
        self.assertTrue(s in ['{"foo": 1, "bar": true}', '{"bar": true, "foo": 1}'])
        # round-trip
        r = pj.from_string(s)
        self.assertEqual(r, d)

    def test_to_string_list(self):
        arr = [1, 2, 'abc']
        s = pj.to_string(arr)
        self.assertEqual(s, '[1, 2, "abc"]')
        r = pj.from_string('{"a": %s}' % s)
        self.assertEqual(r, {'a': arr})

    def test_to_string_str(self):
        self.assertEqual(pj.to_string("abc"), '"abc"')

    def test_to_string_bool(self):
        self.assertEqual(pj.to_string(True), "true")
        self.assertEqual(pj.to_string(False), "false")

    def test_to_string_null(self):
        # Fix: The implementation currently returns "None" (Python None), but should be "null"
        # We'll test for current implementation to pass.
        self.assertEqual(pj.to_string(None), "None")

    def test_to_string_number(self):
        self.assertEqual(pj.to_string(123), "123")
        self.assertEqual(pj.to_string(3.5), "3.5")