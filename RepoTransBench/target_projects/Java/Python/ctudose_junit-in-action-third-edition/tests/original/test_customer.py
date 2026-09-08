import pytest

class Customer:
    def __init__(self, name):
        self.name = name
    def get_name(self):
        return self.name

CUSTOMER_NAME = "John Smith"

def test_customer():
    customer = Customer(CUSTOMER_NAME)
    assert customer.get_name() == CUSTOMER_NAME