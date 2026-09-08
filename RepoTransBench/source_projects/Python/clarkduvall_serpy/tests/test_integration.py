import unittest
import serpy
from obj import Obj

class DummyObj:
    def __init__(self, a=1, b=2, c=None, method_val=5):
        self.a = a
        self.b = b
        self.method_val = method_val
        if c is not None:
            self.c = c

    def meth(self):
        return self.method_val

class TestIntegrationSerpySerializer(unittest.TestCase):
    def test_simple_serialization(self):
        class Ex(serpy.Serializer):
            a = serpy.IntField()
            b = serpy.IntField()
        o = DummyObj(4, 5)
        result = Ex(o).data
        self.assertEqual(result, {'a': 4, 'b': 5})

    def test_method_and_custom_labels(self):
        class Ex(serpy.Serializer):
            foo = serpy.MethodField(label='maybe')
            def get_foo(self, obj):
                return obj.method_val
        o = DummyObj(method_val=42)
        ser = Ex(o)
        data = ser.data
        self.assertIn('maybe', data)
        self.assertEqual(data['maybe'], 42)

    def test_dict_serializer(self):
        class DSer(serpy.DictSerializer):
            x = serpy.IntField()
            y = serpy.IntField()
        d = {'x': 10, 'y': 21}
        result = DSer(d).data
        self.assertEqual(result, {'x': 10, 'y': 21})

    def test_edge_cases_and_repr(self):
        class Example(serpy.Serializer):
            foo = serpy.Field()
        o = Obj(foo='edgecase')
        ex = Example(o)
        repr_str = str(ex)
        self.assertIn('Example', repr_str)