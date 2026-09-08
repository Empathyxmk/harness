import pytest
from cppstddb.test_suite import test_all, test_uri

def test_oracle_test():
    from cppstddb.oracle import database
    # Use connection string "oracle://localhost" as in the C++ test
    uri = test_uri("oracle://localhost")
    test_all(database, uri)