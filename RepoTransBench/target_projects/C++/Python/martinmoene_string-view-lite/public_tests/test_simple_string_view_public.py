import pytest
from src.string_view import StringView

def test_simple_string_view_public():
    # Construct from str
    sv1 = StringView("world!")
    assert sv1.length() == 6
    assert sv1.size() == 6
    assert not sv1.empty()
    assert sv1[2] == 'r'

    # Substring
    sv2 = sv1.substr(1, 3)
    assert sv2.size() == 3
    assert sv2[0] == 'o'
    assert sv2[2] == 'l'

    # Remove prefix/suffix
    sv3 = StringView("ghijkl")
    sv3.remove_prefix(3)  # "jkl"
    assert sv3[0] == 'j'
    sv3.remove_suffix(1)  # "jk"
    assert sv3.size() == 2
    assert sv3[1] == 'k'

    # Comparison
    sv4 = StringView("xy")
    assert sv3 != sv4
    sv5 = StringView("jk")
    assert sv3 == sv5

    # Find
    sv6 = StringView("deedee")
    assert sv6.find('e') == 1
    assert sv6.find('d', 2) == 3
    assert sv6.rfind('e') == 5

    # Edge: empty
    empty_sv = StringView()
    assert empty_sv.empty()
    assert empty_sv.size() == 0
    data = empty_sv.data()
    assert data is None or data == ""