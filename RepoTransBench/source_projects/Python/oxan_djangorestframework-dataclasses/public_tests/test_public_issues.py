import dataclasses
import sys
import typing
import unittest

from unittest import TestCase

from rest_framework import fields, serializers
from rest_framework_dataclasses.serializers import DataclassSerializer

@dataclasses.dataclass
class Simple:
    value: str

class SimpleSerializer(DataclassSerializer):
    class Meta:
        dataclass = Simple

class IssuesPublicTest(TestCase):
    def check_deserialize(self, serializer=DataclassSerializer, **kwargs):
        serializer = serializer(**kwargs)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def test_save_nested_dataclass(self):
        # Different data than original
        parent = dataclasses.make_dataclass('Parent', [('nested', Simple)])
        data = {'nested': {'value': 'B'}}
        self.check_deserialize(dataclass=parent, data=data)

    def test_nested_list(self):
        # Different data
        parent = dataclasses.make_dataclass('Parent', [('nested', typing.List[Simple])])
        data = {'nested': [{'value': 'B'}, {'value': 'C'}]}

        class ParentSerializer(DataclassSerializer):
            nested = SimpleSerializer(many=True)

        self.check_deserialize(ParentSerializer, dataclass=parent, data=data)

    def test_nested_nullable(self):
        parent = dataclasses.make_dataclass('Parent', [('nested', typing.Optional[Simple])])
        data = {'nested': None}

        class ParentSerializer(DataclassSerializer):
            nested = SimpleSerializer(allow_null=True, required=False)

        self.check_deserialize(ParentSerializer, dataclass=parent, data=data)

    def test_create_source(self):
        data = {'renamed_value': 'b'}

        class SimpleRenamedSerializer(DataclassSerializer):
            renamed_value = fields.CharField(source='value')

            class Meta:
                dataclass = Simple
                fields = ('renamed_value', )

        self.check_deserialize(SimpleRenamedSerializer, data=data)

    def test_many_empty(self):
        @dataclasses.dataclass
        class HelloWorld:
            value: str = 'changed'

        serializer = DataclassSerializer(dataclass=HelloWorld, many=True, data=[{}])
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        self.assertIsNot(fields.empty, data[0].value)
        self.assertEqual('changed', data[0].value)

    @unittest.skipIf(sys.version_info < (3, 9, 0), 'Python 3.9 required')
    def test_forward_reference_list(self):
        @dataclasses.dataclass
        class WithForwardReferences:
            children: list['Simple']
            nested_children: list[list['Simple']]

        serializer = DataclassSerializer(dataclass=WithForwardReferences)
        serializer.get_fields()

    def test_empty_sentinel_nesting(self):
        @dataclasses.dataclass
        class Foo:
            value: typing.Optional[str] = 'modified'

        class ParentSerializer(serializers.Serializer):
            foo = DataclassSerializer(dataclass=Foo)

        serializer = ParentSerializer(data={'foo': {}})
        serializer.is_valid(raise_exception=True)

        self.assertEqual(serializer.validated_data['foo'].value, 'modified')

    def test_noninit_fields(self):
        @dataclasses.dataclass
        class A:
            foo: str
            bar: str = dataclasses.field(init=False)

        serializer = DataclassSerializer(dataclass=A, data={'foo': 'def', 'bar': 'xyz'})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        self.assertEqual(instance.foo, 'def')
        self.assertEqual(instance.bar, 'xyz')

    def test_list_save(self):
        @dataclasses.dataclass
        class Foo:
            name: str

        serializer = DataclassSerializer(dataclass=Foo, many=True, data=[{'name': 'alice'}, {'name': 'eve'}])
        serializer.is_valid(raise_exception=True)
        items = serializer.save()

        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0], Foo('alice'))
        self.assertEqual(items[1], Foo('eve'))