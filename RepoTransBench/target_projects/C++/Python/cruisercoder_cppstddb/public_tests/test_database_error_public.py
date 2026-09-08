from cppstddb import database_error

def test_database_error_public():
    # Use a different message for public test
    err = database_error("public_test_db_error: unique violation on public key")
    assert "public_test_db_error" in str(err)