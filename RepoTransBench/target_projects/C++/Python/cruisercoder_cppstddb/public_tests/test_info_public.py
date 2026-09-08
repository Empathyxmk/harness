from cppstddb import info

def test_info_public():
    # info() returns version string or identification containing cppstddb
    assert "cppstddb" in info()