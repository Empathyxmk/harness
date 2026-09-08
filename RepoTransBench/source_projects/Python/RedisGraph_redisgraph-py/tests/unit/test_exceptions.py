import pytest
from redisgraph.exceptions import VersionMismatchException

def test_version_mismatch_exception():
    ver = "2.10.0"
    e = VersionMismatchException(ver)
    assert isinstance(e, VersionMismatchException)
    assert e.version == ver