import pytest

class ContractA_t1:
    def __init__(self):
        self.address = "0xA"
        self.events = []

    def method1(self, contractb_address):
        if hasattr(self, "_method1_called"):
            raise Exception("VM Exception while processing transaction: reverted with reason string 'Nope!'")
        self._method1_called = True
        self.events.append({"args": ["0xA"]})
        return Receipt(self.events.copy())

    def method2(self, contractb_address):
        if hasattr(self, "_method2_called"):
            raise Exception("Method2 can only be called once in this mockup.")
        self._method2_called = True
        self.events.append({"args": ["0xA"]})
        return Receipt(self.events.copy())

    def method3(self, contractb_address, sender):
        self.events.append({"args": [sender]})
        return Receipt(self.events.copy())

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

def test_first_method_reverts_once(setup_contracts):
    user, ContractA, ContractB = setup_contracts
    errors = []
    records = []

    for _ in range(2):
        try:
            receipt = ContractA.method1(ContractB.address)
            if hasattr(receipt, "events") and receipt.events:
                event = receipt.events[0]
                records.append(event["args"][0])
        except Exception as e:
            errors.append(str(e))

    assert len(errors) == 1
    assert errors[0] == "VM Exception while processing transaction: reverted with reason string 'Nope!'"
    assert len(records) == 1
    assert records[0] == ContractA.address

def test_second_method_no_revert(setup_contracts):
    user, ContractA, ContractB = setup_contracts
    errors = []
    records = []

    for _ in range(2):
        try:
            receipt = ContractA.method2(ContractB.address)
            if hasattr(receipt, "events") and receipt.events:
                event = receipt.events[0]
                records.append(event["args"][0])
        except Exception as e:
            errors.append(str(e))

    assert len(errors) == 1
    assert len(records) == 1
    assert records[0] == ContractA.address

def test_third_method_only_user_recorded(setup_contracts):
    user, ContractA, ContractB = setup_contracts
    errors = []
    records = []

    # Only call once, as the logic expects a single user record
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