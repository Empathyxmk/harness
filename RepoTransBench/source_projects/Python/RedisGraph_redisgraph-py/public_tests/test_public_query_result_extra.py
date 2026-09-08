import sys
import os
import pytest

# Ensure redisgraph module is found when running from repo root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from redisgraph.query_result import QueryResult

def test_public_queryresult_scalar_access():
    qr = QueryResult(header=['foo', 'bar'], records=[(5, "abc"), (6, "xyz")])
    assert qr.header == ['foo', 'bar']
    assert qr.records[1][1] == "xyz"

def test_public_queryresult_to_dicts():
    qr = QueryResult(header=['a', 'b'], records=[(10, 20), (30, 40)])
    dicts = qr.to_dicts()
    assert dicts == [{'a': 10, 'b': 20}, {'a': 30, 'b': 40}]

def test_public_queryresult_update_records():
    qr = QueryResult(header=['c'], records=[(123,)])
    # Add new record in a different way than existing test
    qr.records.append((456,))
    assert len(qr.records) == 2
    assert qr.records[-1][0] == 456