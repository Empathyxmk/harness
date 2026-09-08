from pynubank.utils.parsing import parse_float, parse_generic_transaction

def test_parse_float_public():
    assert parse_float("1234,56") == 1234.56
    assert parse_float("0,00") == 0.0
    assert parse_float("-76,54") == -76.54

def test_parse_generic_transaction_public():
    # Use different keys/values from private test
    t = {"amount": "99,99", "description": "Check parsing public"}
    tx = parse_generic_transaction(t)
    assert isinstance(tx, dict)
    assert tx["amount"] == 99.99
    assert tx["description"] == "Check parsing public"