class CheckTarget:
    @staticmethod
    def isValid(s):
        # Very basic URL validity
        if s is None or s == "":
            return False
        return s.startswith("http://") or s.startswith("https://")

    @staticmethod
    def sanitize(s):
        if s is None:
            return ""
        return s

def test_is_valid():
    assert CheckTarget.isValid("http://test.com")
    assert not CheckTarget.isValid("invalid_string")
    assert not CheckTarget.isValid("")

def test_sanitize():
    assert CheckTarget.sanitize("abc") == "abc"
    assert CheckTarget.sanitize(None) == ""