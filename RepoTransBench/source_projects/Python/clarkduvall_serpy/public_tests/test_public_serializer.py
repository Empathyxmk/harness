import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../serpy")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../tests")))

from obj import Obj
import unittest
from serpy.serializer import Serializer
from serpy import fields as serpy_fields

class AnotherPublicSerializer(Serializer):
    name = serpy_fields.StrField()
    value = serpy_fields.IntField()

class MethodPublicSerializer(Serializer):
    foo = serpy_fields.StrField()
    double = serpy_fields.MethodField()

    def get_double(self, obj):
        return obj.foo * 2

class TestPublicSerializer(unittest.TestCase):

    def test_serializer_basic(self):
        o = Obj(name="other", value=13)
        self.assertEqual(AnotherPublicSerializer(o).data, {'name': 'other', 'value': 13})

    def test_serializer_many(self):
        objects = [Obj(name="x", value=2), Obj(name="y", value=7)]
        expected = [
            {'name': 'x', 'value': 2},
            {'name': 'y', 'value': 7}
        ]
        res = AnotherPublicSerializer(objects, many=True).data
        self.assertEqual(res, expected)

    def test_method_serializer(self):
        o = Obj(foo="hello")
        res = MethodPublicSerializer(o).data
        self.assertEqual(res, {'foo': 'hello', 'double': 'hellohello'})

    def test_method_serializer_many(self):
        objects = [Obj(foo="abc"), Obj(foo="de")]
        expected = [
            {'foo': 'abc', 'double': 'abcabc'},
            {'foo': 'de', 'double': 'dede'}
        ]
        res = MethodPublicSerializer(objects, many=True).data
        self.assertEqual(res, expected)

if __name__ == '__main__':
    unittest.main()