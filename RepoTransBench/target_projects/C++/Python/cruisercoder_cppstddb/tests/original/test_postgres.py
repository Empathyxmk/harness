import pytest
from cppstddb.test_suite import test_all, test_uri

def test_postgres_test():
    from cppstddb.postgres import database
    # This tests using the postgres URI per the C++ logic
    uri = test_uri("postgres")
    test_all(database, uri)