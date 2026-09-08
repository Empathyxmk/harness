def strverscmp(s1, s2):
    """Naive implementation."""
    import re
    def splitver(s):
        return [int(x) if x.isdigit() else x for x in re.findall(r'\d+|[^0-9]+', s)]
    return (splitver(s1) > splitver(s2)) - (splitver(s1) < splitver(s2))

def test_strverscmp_eq():
    assert strverscmp('a1', 'a1') == 0

def test_strverscmp_gt():
    assert strverscmp('a2', 'a1') == 1

def test_strverscmp_lt():
    assert strverscmp('a0', 'a1') == -1