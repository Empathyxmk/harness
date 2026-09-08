import re

def test_pattern_matching_with_new_pattern():
    patterns = [re.compile(r"^PUBLIC_\d+$"), re.compile(r"TestCase.*")]
    value1 = "PUBLIC_1234"
    value2 = "TestCasePublic"
    value3 = "NotMatching"

    assert patterns[0].match(value1)
    assert not patterns[0].match(value2)

    assert patterns[1].match(value2)
    assert not patterns[1].match(value3)