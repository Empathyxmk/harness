import pytest
from cppstddb.test_suite import test_all, test_uri

def test_oracle_public():
    from cppstddb.oracle import database
    uri = test_uri("oracle://publichost:1522")
    test_all(database, uri)