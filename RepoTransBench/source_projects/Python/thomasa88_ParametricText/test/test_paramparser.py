import unittest
from paramparser import ParamSpec, nullint

class TestParamSpec(unittest.TestCase):
    def test_from_string_basic(self):
        ps = ParamSpec.from_string("foo")
        self.assertEqual(ps, ParamSpec("foo", None, None, None))

    def test_from_string_with_member(self):
        ps = ParamSpec.from_string("foo.bar")
        self.assertEqual(ps, ParamSpec("foo", "bar", None, None))

    def test_from_string_with_slice(self):
        ps = ParamSpec.from_string("foo[2]")
        self.assertEqual(ps, ParamSpec("foo", None, slice(2, 3), None))
        ps2 = ParamSpec.from_string("foo[1:3]")
        self.assertEqual(ps2, ParamSpec("foo", None, slice(1, 3), None))
        ps3 = ParamSpec.from_string("foo[:4]")
        self.assertEqual(ps3, ParamSpec("foo", None, slice(None, 4), None))
        ps4 = ParamSpec.from_string("foo[-2:]")
        self.assertEqual(ps4, ParamSpec("foo", None, slice(-2, None), None))

    def test_from_string_with_format(self):
        ps = ParamSpec.from_string("foo:0.2f")
        self.assertEqual(ps, ParamSpec("foo", None, None, "0.2f"))
        ps = ParamSpec.from_string("foo.bar[0:2]:spec")
        self.assertEqual(ps, ParamSpec("foo", "bar", slice(0, 2), "spec"))

    def test_from_string_invalid(self):
        # Invalid string produces None
        self.assertIsNone(ParamSpec.from_string("bad["))

    def test_eq(self):
        a = ParamSpec("foo", "bar", slice(1,2), "fmt")
        b = ParamSpec("foo", "bar", slice(1,2), "fmt")
        c = ParamSpec("foo", "baz", slice(1,2), "fmt")
        self.assertTrue(a == b)
        self.assertFalse(a == c)
        self.assertFalse(a == None)
    
    def test_nullint(self):
        self.assertEqual(nullint("3"), 3)
        self.assertEqual(nullint(None), None)
        self.assertEqual(nullint(""), None)