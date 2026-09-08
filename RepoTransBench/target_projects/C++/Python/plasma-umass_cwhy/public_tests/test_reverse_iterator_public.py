def trim(s):
    return s.lstrip().rstrip()

def test_trim_public():
    s1 = "   example   "
    s2 = "\t\n  test123\t\t"
    s3 = "public_case"
    s4 = "   surrounded\t"

    assert trim(s1) == "example"
    assert trim(s2) == "test123"
    assert trim(s3) == "public_case"
    assert trim(s4) == "surrounded"