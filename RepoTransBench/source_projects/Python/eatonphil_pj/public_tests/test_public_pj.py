import unittest

import pj


class TestStringMethodsPublic(unittest.TestCase):
    def test_object_multiple_keys(self):
        self.assertEqual(pj.from_string('{"alpha":42, "beta":"xyz"}'), {"alpha": 42, "beta": "xyz"})

    def test_object_array_numbers(self):
        self.assertEqual(pj.from_string('{"nums":[7,8,9]}'), {"nums": [7, 8, 9]})

    def test_object_boolean(self):
        self.assertEqual(pj.from_string('{"success":false}'), {"success": False})

    def test_object_with_null(self):
        self.assertEqual(pj.from_string('{"unset":null}'), {"unset": None})

    def test_object_with_float(self):
        self.assertEqual(pj.from_string('{"value":2.718}'), {"value": 2.718})

    def test_nested_array(self):
        self.assertEqual(pj.from_string('{"arr":[[1,2],[],[3]]}'), {"arr": [[1,2],[],[3]]})

    def test_nested_object_multiple_levels(self):
        self.assertEqual(
            pj.from_string('{"outer":{"inner":{"leaf":10}}}'),
            {"outer": {"inner": {"leaf": 10}}}
        )

    def test_array_of_objects(self):
        self.assertEqual(
            pj.from_string('{"users":[{"id":1},{"id":2}]}'),
            {"users": [{"id":1}, {"id":2}]}
        )

    def test_basic_string_with_whitespace(self):
        self.assertEqual(
            pj.from_string('{   "k"    :   "v"   }'), {"k": "v"}
        )

    def test_zero_int(self):
        self.assertEqual(pj.from_string('{"z":0}'), {"z": 0})


if __name__ == '__main__':
    unittest.main()