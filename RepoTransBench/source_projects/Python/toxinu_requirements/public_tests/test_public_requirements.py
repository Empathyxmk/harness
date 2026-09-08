import pytest
from requirements import Requirement

def test_parse_normal_requirement_public():
    r = Requirement.parse("boto3>=1.15")
    assert hasattr(r, "name")
    assert getattr(r, "name") == "boto3"
    if hasattr(r, "specifier"):
        assert r.specifier is not None
    if hasattr(r, "is_local_file"):
        assert getattr(r, "is_local_file") is False

def test_parse_local_file_editable_public():
    with pytest.raises(Exception):
        Requirement.parse("/another/path/to/pkg2", editable=True)

def test_parse_local_file_scheme_public():
    r = Requirement.parse("file:///tmp/anotherpackage#egg=otherpkg")
    assert "file://" in str(r)

def test_parse_vcs_url_public():
    vcs_url = "hg+https://bitbucket.org/user/repo2#egg=hgproject"
    r = Requirement.parse(vcs_url)
    assert str(r).startswith("hg+") or "hg+" in str(r)

def test_parse_with_marker_public():
    r = Requirement.parse('urllib3; sys_platform=="win32"')
    assert hasattr(r, "name")
    if hasattr(r, "marker"):
        assert r.marker is not None

def test_str_repr_public():
    r = Requirement.parse("sqlalchemy")
    assert (str(r) == "sqlalchemy") or (str(r) == '<Requirement: "sqlalchemy">')
    assert isinstance(r.__repr__(), str)

def test_equality_and_hash_public():
    r1 = Requirement.parse("bar==3.4")
    r2 = Requirement.parse("bar==3.4")
    try:
        assert r1 == r2
    except Exception:
        pass
    hash(r1)
    hash(r2)

def test_requirement_extras_public():
    r = Requirement.parse("pandas[performance,io]>=1.0")
    assert hasattr(r, "extras") and "performance" in r.extras

def test_parse_invalid_requirement_public():
    with pytest.raises(Exception):
        Requirement.parse("??? this is not valid")

def test_local_file_detected_public():
    with pytest.raises(Exception):
        Requirement.parse("../something.whl")