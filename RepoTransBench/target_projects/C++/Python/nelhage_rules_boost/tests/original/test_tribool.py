import pytest

class Tribool:
    """A minimal 3-valued logic type: True, False, Indeterminate."""
    def __init__(self, value):
        if value is True: self.value = True
        elif value is False: self.value = False
        elif value == "indeterminate": self.value = "indeterminate"
        else: self.value = bool(value)

    def __eq__(self, other):
        if other is True: return self.value is True
        if other is False: return self.value is False
        if other == "indeterminate": return self.value == "indeterminate"
        return NotImplemented

def test_tribool_false():
    a = Tribool(False)
    if a == True:
        pytest.fail("a is True")
    elif a == False:
        assert True
    else:
        pytest.fail("a is indeterminate, should have been False")