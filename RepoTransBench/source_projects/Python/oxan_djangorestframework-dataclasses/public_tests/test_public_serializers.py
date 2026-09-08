import copy
import dataclasses
import datetime
import typing

from unittest import TestCase

from django.core.exceptions import ImproperlyConfigured
from rest_framework import fields, serializers
from rest_framework.fields import empty

from rest_framework_dataclasses import types
from rest_framework_dataclasses.serializers import (
    _strip_empty_sentinels,
    DataclassListSerializer,
    DataclassSerializer,
    HyperlinkedDataclassSerializer
)

@dataclasses.dataclass
class Person:
    name: str
    length: int
    birth_date: typing.Optional[datetime.date] = None

    def age(self) -> int:
        pass

    @property
    def is_child(self) -> bool:
        pass

@dataclasses.dataclass
class Group:
    leader: Person
    people: typing.List[Person]

class SerializerPublicTest(TestCase):
    def create_serializer(self, dataclass=None, arguments=None, declared=None, meta=None) -> DataclassSerializer:
        arguments = arguments or {}
        classdict = declared or {}

        if meta is not None:
            if dataclass:
                meta['dataclass'] = dataclass
            classdict['Meta'] = type('Meta', (), meta)
        elif dataclass:
            arguments['dataclass'] = dataclass

        serializer_type = type('TestSerializer', (DataclassSerializer, ), classdict)
        return serializer_type(**arguments)

    def test_many(self):
        ser = self.create_serializer(Person, {'many': True})
        self.assertIsInstance(ser, DataclassListSerializer)
        self.assertIsInstance(ser.child, DataclassSerializer)
        self.assertTrue(ser.allow_empty)

        ser = self.create_serializer(Person, {'many': True, 'allow_empty': False})
        self.assertFalse(ser.allow_empty)

    def test_definition(self):
        definition = self.create_serializer(Person).dataclass_definition
        self.assertIs(definition.dataclass_type, Person)
        self.assertIn('name', definition.fields)
        self.assertEqual(definition.field_types['name'], str)
        self.assertIn('length', definition.fields)
        self.assertEqual(definition.field_types['length'], int)
        self.assertIn('birth_date', definition.fields)
        self.assertEqual(definition.field_types['birth_date'], typing.Optional[datetime.date])

        with self.assertRaises(AssertionError):
            definition = self.create_serializer(arguments={'dataclass': Person},
                                                meta={}).dataclass_definition

        with self.assertRaises(AssertionError):
            definition = self.create_serializer().dataclass_definition

        with self.assertRaises(AssertionError):
            definition = self.create_serializer(meta={}).dataclass_definition

        with self.assertRaises(ValueError):
            definition = self.create_serializer(dict).dataclass_definition

    def test_strip_empty(self):
        in_data = Person(name='Eve', length=456, birth_date=empty)
        out_data = Person(name='Eve', length=456, birth_date=None)
        self.assertEqual(_strip_empty_sentinels(in_data), out_data)

        in_data = Group(leader=Person(name='Eve', length=456, birth_date=empty),
                        people=[Person(name='Mallory', length=789, birth_date=empty)])
        out_data = Group(leader=Person(name='Eve', length=456),
                         people=[Person(name='Mallory', length=789)])
        self.assertEqual(_strip_empty_sentinels(in_data), out_data)

    def test_save(self):
        def mock_save(validated_data, instance=None, partial=False, **kwargs):
            serializer = self.create_serializer(Person)
            serializer._errors = []
            serializer._validated_data = validated_data
            serializer.partial = partial
            if instance:
                serializer.instance = instance
            return serializer.save(**kwargs)

        in_data = Person(name='Eve', length=456)
        out_data = mock_save(in_data)
        self.assertEqual(in_data, out_data)

        inst = Person(name='Eve', length=456)
        in_data = dataclasses.replace(inst, length=654)
        out_data = mock_save(in_data, instance=inst)
        self.assertIs(out_data, inst)
        self.assertEqual(out_data, in_data)

        in_data = Person(name='Eve', length=456)
        out_data = mock_save(in_data, length=654)
        self.assertEqual(out_data, dataclasses.replace(in_data, length=654))

        inst = Person(name='Mallory', length=789)
        in_data = Person(name='Eve', length=654)
        out_data = mock_save(in_data, instance=inst, length=654)
        self.assertIs(out_data, inst)
        self.assertEqual(out_data, dataclasses.replace(in_data, length=654))

        inst = Person(name='Eve', length=456, birth_date=datetime.datetime(2019, 3, 4))
        in_data = Person(name='Eve', length=456, birth_date=None)
        out_data = mock_save(in_data, instance=inst)
        self.assertIs(out_data, inst)
        self.assertEqual(out_data.birth_date, None)

        inst = Person(name='Eve', length=456, birth_date=datetime.datetime(2019, 3, 4))
        in_data = Person(name='Eve', length=456, birth_date=empty)
        out_data = mock_save(in_data, instance=inst, partial=True)
        self.assertIs(out_data, inst)
        self.assertEqual(out_data.birth_date, datetime.datetime(2019, 3, 4))

        inst = Person(name='Eve', length=456)
        in_data = Person(name='Mallory', length=empty)
        out_data = mock_save(in_data, instance=inst, partial=True)
        self.assertIs(out_data, inst)
        self.assertEqual(out_data.name, 'Mallory')
        self.assertEqual(out_data.length, 456)

        with self.assertRaises(AssertionError):
            self.create_serializer(Person).save()

    def test_nested_save(self):
        def check(dataclass, representation, instance):
            empty_instance = copy.deepcopy(instance)
            for field in dataclasses.fields(empty_instance):
                setattr(empty_instance, field.name, None)

            serializer = self.create_serializer(dataclass, arguments={'data': representation})
            self.assertTrue(serializer.is_valid(raise_exception=False))
            self.assertEqual(serializer.save(), instance)

            serializer = self.create_serializer(dataclass, arguments={'data': representation,
                                                                      'instance': empty_instance})
            self.assertTrue(serializer.is_valid(raise_exception=False))
            self.assertEqual(serializer.save(), instance)

        simple = dataclasses.make_dataclass('child', [('value', str)])
        check(simple, {'value': 'D'}, simple('D'))

        parent = dataclasses.make_dataclass('parent', [('field', simple)])
        check(parent, {'field': {'value': 'D'}}, parent(simple('D')))

        grandparent = dataclasses.make_dataclass('grandparent', [('field', parent)])
        check(grandparent, {'field': {'field': {'value': 'D'}}}, grandparent(parent(simple('D'))))

        _list = dataclasses.make_dataclass('parent', [('fields', typing.List[simple])])
        check(_list, {'fields': [{'value': 'X'}, {'value': 'Y'}]}, _list([simple('X'), simple('Y')]))