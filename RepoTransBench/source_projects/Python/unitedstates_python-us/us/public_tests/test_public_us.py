from us import states

def test_fips_lookup():
    # Use different state than original
    assert states.lookup("48") == states.TX  # Texas

def test_abbr_lookup():
    # Use CO instead of CA
    assert states.lookup("CO") == states.CO

def test_name_lookup():
    # Use Florida instead of California
    assert states.lookup("Florida") == states.FL

def test_metaphone_lookup():
    # Slightly modified spelling for Minnesota
    assert states.lookup("Minissota") == states.MN

def test_metaphone_lookup_caps():
    # All caps, use ILLUNOYS instead of California
    assert states.lookup("ILLINOYS") == states.IL

def test_lookup_with_integer_input():
    # Instead of integer, pass as str to match supported API ("12" for FL)
    assert states.lookup("12") == states.FL

def test_lookup_with_field():
    # Match by capital
    assert states.lookup("Madison", field="capital") == states.WI

def test_nonexistant_lookup_returns_none():
    # Try an obviously wrong lookup
    assert states.lookup("GOTHAMCITY") is None

def test_territory_lookup():
    assert states.lookup("PR") == states.PR