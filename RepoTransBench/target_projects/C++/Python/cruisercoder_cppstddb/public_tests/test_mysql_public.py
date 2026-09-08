import pytest
from cppstddb.test_suite import test_all, test_uri

def test_mysql_public():
    from cppstddb.mysql import database
    uri = test_uri("mysql_public")
    test_all(database, uri)