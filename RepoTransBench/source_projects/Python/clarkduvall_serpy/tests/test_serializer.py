import unittest
from obj import Obj
import serpy

class TestSerializer(unittest.TestCase):
    def test_label_field(self):
        class Example(serpy.Serializer):
            foo_label = serpy.Field(attr='foo', label='foo_out')
        o = Obj(foo='thing')
        self.assertEqual(Example(o).data['foo_out'], 'thing')

    def test_serializer_to_value(self):
        class Example(serpy.Serializer):
            one = serpy.IntField()
            two = serpy.IntField()
        o = Obj(one=1, two=2)
        e = Example(o)
        self.assertEqual(e.to_value(o), {'one': 1, 'two': 2})

    def test_missing_attr(self):
        class Example(serpy.Serializer):
            foo = serpy.Field(attr='bar')
        o = Obj(bar='baz')
        self.assertEqual(Example(o).data['foo'], 'baz')