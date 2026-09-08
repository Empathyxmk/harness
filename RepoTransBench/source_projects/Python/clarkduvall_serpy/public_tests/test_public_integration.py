import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../serpy")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../tests")))

from obj import Obj
import unittest
from serpy import fields as serpy_fields
from serpy.serializer import Serializer

class IntegrationPublicSerializer(Serializer):
    a = serpy_fields.IntField()
    b = serpy_fields.StrField()
    c = serpy_fields.MethodField()
    # Remove 'd' as a Field: instead, use a MethodField for controlled missing
    d = serpy_fields.MethodField()

    def get_c(self, obj):
        return obj.b * 2 if isinstance(obj.b, str) else str(obj.b)

    def get_d(self, obj):
        # Return the value of d if present else None
        return getattr(obj, "d", None)

class TestPublicIntegration(unittest.TestCase):

    def test_all_fields(self):
        obj = Obj(a=99, b="foo", d=255)
        s = IntegrationPublicSerializer(obj)
        self.assertEqual(s.data, {'a': 99, 'b': 'foo', 'c': 'foofoo', 'd': 255})

    def test_missing_field(self):
        obj = Obj(a=44, b="echo")  # d is missing
        s = IntegrationPublicSerializer(obj)
        self.assertEqual(s.data, {'a': 44, 'b': 'echo', 'c': 'echoecho', 'd': None})

    def test_list_many(self):
        objs = [Obj(a=8, b="a"), Obj(a=9, b="Xx", d=777)]
        res = IntegrationPublicSerializer(objs, many=True).data
        expected = [
            {'a': 8, 'b': 'a', 'c': 'aa', 'd': None},
            {'a': 9, 'b': 'Xx', 'c': 'XxXx', 'd': 777},
        ]
        self.assertEqual(res, expected)

if __name__ == "__main__":
    unittest.main()