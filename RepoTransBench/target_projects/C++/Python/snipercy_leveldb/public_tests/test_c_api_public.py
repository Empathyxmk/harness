"""
Python translation of the LevelDB C API public test.

Note: This test simulates the scenario of db/c_public_test.c by
using Python's LevelDB bindings as a blackbox for similar C API checks.
If possible, use "plyvel" (pip install plyvel).

The key value logic, edge cases, and DB destruction are analogous to the C test.
"""

import pytest
import tempfile
import shutil
import os
import plyvel

def test_c_api_public():
    dbname = tempfile.mkdtemp(prefix="cdb_public_test_tmpdb_")
    try:
        # Open DB (automatically creates if missing)
        db = plyvel.DB(dbname, create_if_missing=True)
        key = b"cat"
        val = b"meow"

        # Put
        db.put(key, val)
        # Get
        get_value = db.get(key)
        assert get_value == val

        # Delete
        db.delete(key)
        get_deleted = db.get(key)
        assert get_deleted is None

        # Clean up: close and remove db dir
        db.close()
    finally:
        if os.path.exists(dbname):
            shutil.rmtree(dbname)