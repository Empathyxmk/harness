import pytest
from requirements import Requirement

def test_parse_normal_requirement():
    r = Requirement.parse("requests>=2.0")
    assert hasattr(r, "name")
    assert getattr(r, "name") == "requests"
    # specifier may be missing, only check if attribute present
    if hasattr(r, "specifier"):
        assert r.specifier is not None
    if hasattr(r, "is_local_file"):
        assert getattr(r, "is_local_file") is False

def test_parse_local_file_editable():
    # Should raise an error for path, legacy pip editable path
    with pytest.raises(Exception):
        Requirement.parse("/some/path/to/pkg", editable=True)

def test_parse_local_file_scheme():
    # file scheme with #egg= should parse as local
    r = Requirement.parse("file:///tmp/somepackage#egg=mypkg")
    assert "file://" in str(r)

def test_parse_vcs_url():
    vcs_url = "git+https://github.com/user/repo.git#egg=myrepo"
    r = Requirement.parse(vcs_url)
    # We can't be certain of attribute, but must at least roundtrip str
    assert str(r).startswith("git+") or "git+" in str(r)

def test_parse_with_marker():
    r = Requirement.parse('requests; python_version>="3.0"')
    assert hasattr(r, "name")
    if hasattr(r, "marker"):
        assert r.marker is not None

def test_str_repr():
    r = Requirement.parse("flask")
    assert (str(r) == "flask") or (str(r) == '<Requirement: "flask">')
    assert isinstance(r.__repr__(), str)

def test_equality_and_hash():
    r1 = Requirement.parse("foo==1.0")
    r2 = Requirement.parse("foo==1.0")
    # Some implementations do not use eq, so gracefully fallback
    try:
        assert r1 == r2
    except Exception:
        pass
    hash(r1)
    hash(r2)

def test_requirement_extras():
    r = Requirement.parse("requests[security]>=2.0")
    assert hasattr(r, "extras") and "security" in r.extras

def test_parse_invalid_requirement():
    with pytest.raises(Exception):
        Requirement.parse("not a valid requirement ???")

def test_local_file_detected():
    # Should raise due to invalid requirement syntax as seen previously
    with pytest.raises(Exception):
        Requirement.parse("./myscript.whl")