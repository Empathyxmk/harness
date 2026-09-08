import copy
import dataclasses
import datetime
import decimal
import enum
import typing
import uuid

from unittest import TestCase

from rest_framework import fields
from rest_framework.serializers import Serializer

from rest_framework_dataclasses.serializers import DataclassSerializer
from rest_framework_dataclasses.types import Literal

class FunctionalTestMixin:
    representation_readonly = {}

    def test_serialize(self):
        serializer = self.serializer(instance=self.instance)
        self.assertDictEqual(serializer.data, {**self.representation, **self.representation_readonly})

    def test_validated_data(self):
        serializer = self.serializer(data=self.representation)
        serializer.is_valid(raise_exception=True)

        self.assertEqual(serializer.validated_data, self.instance)

    def test_create(self: TestCase):
        serializer = self.serializer(data=self.representation)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        self.assertEqual(instance, self.instance)

    def test_update(self: TestCase):
        empty_instance = copy.deepcopy(self.instance)
        for field in dataclasses.fields(empty_instance):
            setattr(empty_instance, field.name, None)

        serializer = self.serializer(instance=empty_instance, data=self.representation)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        self.assertIs(instance, empty_instance)
        self.assertEqual(instance, self.instance)

# Public Testcase 1: Pet with different data
@dataclasses.dataclass
class Pet:
    animal: Literal['cat', 'dog']
    name: str
    weight: typing.Optional[decimal.Decimal] = \
        dataclasses.field(default=None, metadata={'serializer_kwargs': {'max_digits': 4, 'decimal_places': 1}})

class PetSerializer(DataclassSerializer):
    class Meta:
        dataclass = Pet

class PetPublicTest(TestCase, FunctionalTestMixin):
    serializer = PetSerializer
    instance = Pet(animal='dog', name='Charlie', weight=decimal.Decimal('12.5'))
    representation = {'animal': 'dog', 'name': 'Charlie', 'weight': '12.5'}

# Public Testcase 2: Union types, different data
@dataclasses.dataclass
class Wood:
    species: str

@dataclasses.dataclass
class Steel:
    alloy: str

@dataclasses.dataclass
class Building:
    material: typing.Union[Wood, Steel]

class BuildingSerializer(DataclassSerializer):
    class Meta:
        dataclass = Building

class BuildingPublicTest(TestCase, FunctionalTestMixin):
    serializer = BuildingSerializer
    instance = Building(
        material=Steel(alloy='stainless')
    )
    representation = {
        'material': {
            'type': 'Steel',
            'alloy': 'stainless',
        }
    }

# Public Testcase 3: Complicated fields and nesting, different data

class Gender(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

@dataclasses.dataclass
class Person:
    id: uuid.UUID
    name: str
    email: str
    phone: typing.List[str]
    gender: typing.Optional[Gender] = None
    length: typing.Optional[decimal.Decimal] = None
    pets: typing.Optional[typing.List[Pet]] = None
    birth_date: typing.Optional[datetime.date] = None
    favorite_pet: typing.Optional[Pet] = \
        dataclasses.field(default=None, metadata={'serializer_field': PetSerializer(allow_null=True)})
    movie_ratings: typing.Optional[typing.Dict[str, int]] = None

    def age(self) -> int:
        return datetime.date(2021, 1, 1).year - self.birth_date.year if self.birth_date else None

    def is_child(self) -> bool:
        return self.age() < 18 if self.birth_date else None

class PersonSerializer(DataclassSerializer):
    full_name = fields.CharField(source='name')
    email = fields.EmailField()
    slug = fields.SlugField(source='name', read_only=True)

    class Meta:
        dataclass = Person
        fields = ('id', 'full_name', 'email', 'phone', 'gender', 'length', 'pets', 'birth_date', 'favorite_pet',
                  'movie_ratings', 'slug', 'age', 'is_child')
        extra_kwargs = {
            'id': {'format': 'hex'},
            'phone': {'child_kwargs': {'max_length': 15}},
            'pets': {'child_kwargs': {'extra_kwargs': {'weight': {'max_digits': 4, 'decimal_places': 1}}}},
        }

class PersonPublicTest(TestCase, FunctionalTestMixin):
    maxDiff = None
    serializer = PersonSerializer
    instance = Person(
        id=uuid.UUID('12345678-1234-5678-1234-567812345678'),
        name='Bob',
        email='bob@example.org',
        length=decimal.Decimal('1.75'),
        phone=['+1-800-555-1234'],
        gender=Gender.MALE,
        pets=[Pet(animal='dog', name='Charlie', weight=decimal.Decimal('12.5'))],
        birth_date=datetime.date(2000, 6, 15),
        favorite_pet=Pet(animal='dog', name='Charlie', weight=decimal.Decimal('12.5')),
        movie_ratings={'Jaws': 10, 'Finding Nemo': 7}
    )
    representation = {
        'id': '12345678123456781234567812345678',
        'full_name': 'Bob',
        'email': 'bob@example.org',
        'length': '1.75',
        'phone': ['+1-800-555-1234'],
        'gender': 'male',
        'pets': [
            {'animal': 'dog', 'name': 'Charlie', 'weight': '12.5'}
        ],
        'birth_date': '2000-06-15',
        'age': 21,
        'is_child': False,
        'favorite_pet': {'animal': 'dog', 'name': 'Charlie', 'weight': '12.5'},
        'movie_ratings': {'Jaws': 10, 'Finding Nemo': 7},
    }
    representation_readonly = {
        'slug': 'Bob'
    }

class EmptyPersonPublicTest(TestCase, FunctionalTestMixin):
    serializer = PersonSerializer
    instance = Person(
        id=uuid.UUID('12345678-1234-5678-1234-567812345678'),
        name='Bob',
        email='bob@example.org',
        phone=[],
    )
    representation = {
        'id': '12345678123456781234567812345678',
        'full_name': 'Bob',
        'email': 'bob@example.org',
        'phone': [],
        'gender': None,
        'length': None,
        'pets': None,
        'birth_date': None,
        'favorite_pet': None,
        'movie_ratings': None,
        'age': None,
        'is_child': None,
    }
    representation_readonly = {
        'slug': 'Bob'
    }