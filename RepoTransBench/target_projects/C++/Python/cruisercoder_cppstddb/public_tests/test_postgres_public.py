import pytest
from cppstddb.test_suite import test_all, test_uri

def test_postgres_public():
    from cppstddb.postgres import database
    # Use altered URI for public test
    uri = test_uri("postgres_public")
    test_all(database, uri)