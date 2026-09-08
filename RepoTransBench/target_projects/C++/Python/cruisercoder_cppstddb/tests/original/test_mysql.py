import pytest
from cppstddb.test_suite import test_all, test_uri

def test_mysql_test():
    from cppstddb.mysql import database
    uri = test_uri("mysql")
    test_all(database, uri)