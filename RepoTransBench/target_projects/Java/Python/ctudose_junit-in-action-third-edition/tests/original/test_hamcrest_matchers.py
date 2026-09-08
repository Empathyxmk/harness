import pytest

class Customer:
    def __init__(self, first_name, last_name):
        self.firstName = first_name
        self.lastName = last_name

@pytest.fixture
def customer():
    first_name = "John"
    last_name = "Smith"
    return Customer(first_name, last_name)

def test_hamcrest_is():
    price1 = 1
    price2 = 1
    price3 = 2

    assert 1 == price1
    assert 1 == price2 or 1 == price3  # "anyOf"
    assert 1 == price1 and 1 == price2 # "allOf"

def test_null():
    assert None is None

def test_not_null(customer):
    assert customer is not None

def test_correct_customer_properties(customer):
    assert hasattr(customer, "firstName") and customer.firstName == "John"
    assert hasattr(customer, "lastName") and customer.lastName == "Smith"