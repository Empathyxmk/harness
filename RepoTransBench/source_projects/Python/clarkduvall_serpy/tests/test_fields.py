import unittest
from obj import Obj
import serpy

class TestFields(unittest.TestCase):
    def test_str_field(self):
        class Example(serpy.Serializer):
            foo = serpy.StrField()
        o = Obj(foo='hello')
        self.assertEqual(Example(o).data['foo'], 'hello')

    def test_int_field(self):
        class Example(serpy.Serializer):
            foo = serpy.IntField()
        o = Obj(foo='23')
        self.assertEqual(Example(o).data['foo'], 23)

    def test_float_field(self):
        class Example(serpy.Serializer):
            foo = serpy.FloatField()
        o = Obj(foo=2)
        self.assertEqual(Example(o).data['foo'], 2.0)

    def test_bool_field(self):
        class Example(serpy.Serializer):
            foo = serpy.BoolField()
        o = Obj(foo=1)
        self.assertEqual(Example(o).data['foo'], True)

    def test_method_field(self):
        class Example(serpy.Serializer):
            foo = serpy.MethodField()
            def get_foo(self, obj):
                return obj.foo * 2
        o = Obj(foo=3)
        self.assertEqual(Example(o).data['foo'], 6)