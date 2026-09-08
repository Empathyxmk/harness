import os
import re
import us
import builtins
import pytest

def test_state_repr_and_str():
    s = us.states.AL
    assert repr(s) == f"<State:{s.name}>"
    assert str(s) == s.name

def test_shapefile_urls_with_fips():
    s = us.states.AL
    urls = s.shapefile_urls()
    assert isinstance(urls, dict)
    # Spot check that at least tract and county in urls
    assert "tract" in urls
    assert "county" in urls

def test_shapefile_urls_without_fips():
    # Construct a State with no FIPS
    from us.states import State
    s = State(name="Fake", abbr="ZZ", fips=None, is_obsolete=True, is_territory=True, is_contiguous=False, is_continental=False,
              ap_abbr=None, capital=None, capital_tz=None, name_metaphone="FK", statehood_year=None, time_zones=[])
    assert s.shapefile_urls() is None

def test_lookup_with_field_argument():
    md = us.states.MD
    assert us.states.lookup("MD", field="abbr") == md
    assert us.states.lookup("24", field="fips") == md
    assert us.states.lookup(md.name_metaphone, field="name_metaphone") == md
    # Should miss because it's case-sensitive
    assert us.states.lookup("maryland", field="name") is None

def test_lookup_no_match_returns_none():
    assert us.states.lookup("nonesuchstate") is None
    # Deliberately obscure metaphone so it cannot succeed
    assert us.states.lookup("zzzzzzzzzz") is None

def test_lookup_caching():
    val = "MD"
    # Prime the cache
    md = us.states.lookup(val)
    # Now remove MD from STATES_AND_TERRITORIES to test cache
    from us.states import _lookup_cache
    cache_key = "abbr:MD"
    assert cache_key in _lookup_cache
    assert us.states.lookup(val, use_cache=True) == md

def test_mapping_default_and_custom():
    # Default: check mapping from abbr to fips
    m = us.states.mapping("abbr", "fips")
    assert m["MD"] == "24"
    assert m["AL"] == "01"
    # Custom: just DC and MD
    custom = us.states.mapping("abbr", "fips", states=[us.states.DC, us.states.MD])
    assert set(custom.keys()) == {"DC", "MD"}

def test_FIPS_RE_and_ABBR_RE():
    assert us.states.FIPS_RE.match("24")
    assert not us.states.FIPS_RE.match("a2")
    assert us.states.ABBR_RE.match("MD")
    assert us.states.ABBR_RE.match("md")
    assert not us.states.ABBR_RE.match("maryland")

def test_DCS_statehood_env(monkeypatch):
    monkeypatch.setenv("DC_STATEHOOD", "1")
    import importlib
    import us.states
    importlib.reload(us.states)
    assert us.states.DC_STATEHOOD is True
    monkeypatch.delenv("DC_STATEHOOD")
    importlib.reload(us.states)
    assert us.states.DC_STATEHOOD is False

def test_imports_exports_version():
    import us
    assert hasattr(us, "version")
    import us.unitedstatesofamerica as usa
    assert hasattr(usa, "name")
    assert hasattr(usa, "abbr")
    assert hasattr(usa, "birthday")
    assert usa.name == "United States of America"
    assert usa.abbr == "US"
    assert str(usa.birthday) == "1776-07-04"