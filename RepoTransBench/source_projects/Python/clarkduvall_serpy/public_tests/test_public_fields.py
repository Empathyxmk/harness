import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../serpy")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../tests")))

from obj import Obj
import unittest
from serpy import fields as serpy_fields
from serpy.serializer import Serializer

class TestPublicFields(unittest.TestCase):

    def test_str_field(self):
        class TestSerializer(Serializer):
            foo = serpy_fields.StrField()

        o = Obj(foo="differentstr")
        self.assertEqual(TestSerializer(o).data, {'foo': 'differentstr'})

    def test_int_field(self):
        class TestSerializer(Serializer):
            bar = serpy_fields.IntField()

        o = Obj(bar=100)
        self.assertEqual(TestSerializer(o).data, {'bar': 100})

    def test_method_field(self):
        class TestSerializer(Serializer):
            special = serpy_fields.MethodField()

            def get_special(self, obj):
                return obj.foo.upper()

        o = Obj(foo="public")
        self.assertEqual(TestSerializer(o).data, {'special': 'PUBLIC'})

    def test_missing_value_field(self):
        class TestSerializer(Serializer):
            # Use a MethodField to simulate optional field
            bar = serpy_fields.MethodField()
            def get_bar(self, obj):
                return getattr(obj, "bar", None)

        o = Obj()  # bar is missing
        self.assertEqual(TestSerializer(o).data, {'bar': None})

if __name__ == "__main__":
    unittest.main()