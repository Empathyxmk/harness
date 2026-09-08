import pytest

# This file adapts the public tests for Trivia1 from the JS version

class ContractA_t1:
    def __init__(self):
        self.address = "0xA"
        self.events = []
        self._method1_count = 0
        self._method2_called = False

    def method1(self, contractb_address):
        # in public, called three times; first succeeds, then two revert
        if self._method1_count == 0:
            self._method1_count += 1
            self.events.append({"args": [self.address]})
            return Receipt(self.events[-1:])
        else:
            self._method1_count += 1
            raise Exception("VM Exception while processing transaction: reverted with reason string 'Nope!'")

    def method2(self, contractb_address):
        if not self._method2_called:
            self._method2_called = True
            self.events.append({"args": [self.address]})
            return Receipt(self.events[-1:])
        else:
            return Receipt([])

    def method3(self, contractb_address, sender):
        self.events.append({"args": [sender]})
        return Receipt(self.events[-1:])

class ContractB_t1:
    def __init__(self):
        self.address = "0xB"

class User:
    def __init__(self):
        self.address = "0xUSER"

class Receipt:
    def __init__(self, events):
        self.events = events

@pytest.fixture(scope="function")
def setup_contracts():
    user = User()
    contracta = ContractA_t1()
    contractb = ContractB_t1()
    return user, contracta, contractb

def test_first_method_reverts_twice(setup_contracts):
    user, ContractA, ContractB = setup_contracts
    errors = []
    records = []
    for _ in range(3):
        try:
            receipt = ContractA.method1(ContractB.address)
            if hasattr(receipt, "events") and receipt.events:
                event = receipt.events[0]
                records.append(event["args"][0])
        except Exception as e:
            errors.append(str(e))
    # Should have 2 errors out of 3 calls
    assert len(errors) == 2
    assert all("reverted with reason string 'Nope!'" in error for error in errors)
    assert len(records) == 1
    assert records[0] == ContractA.address

def test_second_method_no_revert_multi(setup_contracts):
    user, ContractA, ContractB = setup_contracts
    errors = []
    records = []
    for _ in range(4):
        try:
            receipt = ContractA.method2(ContractB.address)
            if hasattr(receipt, "events") and receipt.events:
                event = receipt.events[0]
                records.append(event["args"][0])
        except Exception as e:
            errors.append(str(e))
    assert len(errors) == 0
    assert len(records) == 1
    assert records[0] == ContractA.address

def test_third_method_called_once(setup_contracts):
    user, ContractA, ContractB = setup_contracts
    errors = []
    records = []
    for _ in range(1):
        try:
            receipt = ContractA.method3(ContractB.address, sender=user.address)
            if hasattr(receipt, "events") and receipt.events:
                event = receipt.events[0]
                records.append(event["args"][0])
        except Exception as e:
            errors.append(str(e))
    assert len(errors) == 0
    assert len(records) == 1
    assert records[0] == user.address