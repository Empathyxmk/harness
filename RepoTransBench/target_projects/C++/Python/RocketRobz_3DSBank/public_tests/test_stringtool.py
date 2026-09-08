import pytest

# --- Begin: Minimal implementation for stringtool utilities (to test logic) ---
class stringtool:
    @staticmethod
    def ToLower(s):
        return s.lower()

    @staticmethod
    def ToUpper(s):
        return s.upper()

    @staticmethod
    def Split(s, delim):
        return s.split(delim)

    @staticmethod
    def Join(lst, delim):
        return delim.join(lst)
# --- End: Minimal implementation ---

def test_to_lower_public():
    str_ = "TeStCaSe"
    str_ = stringtool.ToLower(str_)
    assert str_ == "testcase"

def test_to_upper_public():
    str_ = "TeStCaSe"
    str_ = stringtool.ToUpper(str_)
    assert str_ == "TESTCASE"

def test_split_public():
    str_ = "alpha,beta,gamma,delta"
    result = stringtool.Split(str_, ',')
    assert len(result) == 4
    assert result[0] == "alpha"
    assert result[3] == "delta"

def test_join_public():
    vec = ["these", "are", "joined"]
    joined = stringtool.Join(vec, '-')
    assert joined == "these-are-joined"