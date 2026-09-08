import pytest

class Customer:
    def __init__(self, name):
        self.name = name
    def get_name(self):
        return self.name

class CustomersRepository:
    def __init__(self):
        self.customers = {}

    def persist(self, customer):
        self.customers[customer.get_name()] = customer

    def contains(self, name):
        return name in self.customers

CUSTOMER_NAME = "John Smith"

class TestCustomersRepository:
    def setup_method(self, method):
        self.repository = CustomersRepository()

    def test_non_existence(self):
        assert not self.repository.contains(CUSTOMER_NAME)

    def test_customer_persistence(self):
        self.repository.persist(Customer(CUSTOMER_NAME))
        assert self.repository.contains(CUSTOMER_NAME)