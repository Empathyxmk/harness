import pytest

class Tribool:
    """A minimal 3-valued logic type: True, False, Indeterminate."""
    def __init__(self, value):
        if value is True: self.value = True
        elif value is False: self.value = False
        elif value == "indeterminate": self.value = "indeterminate"
        else: self.value = value

    def __eq__(self, other):
        if other is True: return self.value is True
        if other is False: return self.value is False
        if other == "indeterminate": return self.value == "indeterminate"
        return NotImplemented

def test_tribool_public():
    a = Tribool("indeterminate")
    if a == True:
        pytest.fail("a should not be True")
    elif a == False:
        pytest.fail("a should not be False")
    else:
        assert a.value == "indeterminate"