import pytest
from datetime import datetime

class Gender:
    MALE = 'male'
    FEMALE = 'female'

class Customer:
    class Builder:
        def __init__(self, gender, first_name, last_name):
            self._gender = gender
            self._first_name = first_name
            self._last_name = last_name
            self._middle_name = None
            self._become_customer = None

        def with_middle_name(self, middle_name):
            self._middle_name = middle_name
            return self

        def with_become_customer(self, date):
            self._become_customer = date
            return self

        def build(self):
            return Customer(
                gender=self._gender,
                first_name=self._first_name,
                last_name=self._last_name,
                middle_name=self._middle_name,
                become_customer=self._become_customer
            )
    def __init__(self, gender, first_name, last_name, middle_name=None, become_customer=None):
        self._gender = gender
        self._first_name = first_name
        self._last_name = last_name
        self._middle_name = middle_name
        self._become_customer = become_customer

    def get_gender(self):
        return self._gender
    def get_first_name(self):
        return self._first_name
    def get_last_name(self):
        return self._last_name
    def get_middle_name(self):
        return self._middle_name
    def get_become_customer(self):
        return self._become_customer

    def __eq__(self, other):
        return (
            isinstance(other, Customer)
            and self._gender == other._gender
            and self._first_name == other._first_name
            and self._last_name == other._last_name
        )

    def __hash__(self):
        return hash((self._gender, self._first_name, self._last_name))

FIRST_NAME = "John"
LAST_NAME = "Smith"

def test_customer_builder():
    MIDDLE_NAME = "Michael"
    customer_date = datetime.strptime("04-21-2019", "%m-%d-%Y")
    customer = Customer.Builder(Gender.MALE, FIRST_NAME, LAST_NAME) \
        .with_middle_name(MIDDLE_NAME) \
        .with_become_customer(customer_date) \
        .build()
    assert customer.get_gender() == Gender.MALE
    assert customer.get_first_name() == FIRST_NAME
    assert customer.get_last_name() == LAST_NAME
    assert customer.get_middle_name() == MIDDLE_NAME
    assert customer.get_become_customer() == customer_date

def test_different_customers():
    other_first = "John"
    other_last = "Doe"
    customer = Customer.Builder(Gender.MALE, FIRST_NAME, LAST_NAME).build()
    other_customer = Customer.Builder(Gender.MALE, other_first, other_last).build()
    assert customer != other_customer

def test_same_customer():
    customer = Customer.Builder(Gender.MALE, FIRST_NAME, LAST_NAME).build()
    other_customer = Customer.Builder(Gender.MALE, FIRST_NAME, LAST_NAME).build()
    assert customer == other_customer
    assert customer is not other_customer

def test_different_customers_hash():
    other_first = "John"
    other_last = "Doe"
    customer = Customer.Builder(Gender.MALE, FIRST_NAME, LAST_NAME).build()
    other_customer = Customer.Builder(Gender.MALE, other_first, other_last).build()
    assert hash(customer) != hash(other_customer)

def test_same_customer_hash():
    customer = Customer.Builder(Gender.MALE, FIRST_NAME, LAST_NAME).build()
    other_customer = Customer.Builder(Gender.MALE, FIRST_NAME, LAST_NAME).build()
    assert hash(customer) == hash(other_customer)