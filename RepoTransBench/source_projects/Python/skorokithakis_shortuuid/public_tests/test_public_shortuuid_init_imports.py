import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_shortuuid_import_main_public():
    # Should successfully import the main module symbols
    import shortuuid
    assert hasattr(shortuuid, "ShortUUID")
    assert callable(shortuuid.encode)
    assert callable(shortuuid.decode)
    assert callable(shortuuid.uuid)