def underline_to_camel(s):
    parts = s.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

def camel_to_underline(s):
    import re
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()

def join(items, sep):
    return sep.join(items)

def test_underline_to_camel_public():
    assert underline_to_camel("snake_case_field") == "snakeCaseField"
    assert underline_to_camel("another_example") == "anotherExample"
    assert underline_to_camel("simple_test") == "simpleTest"

def test_camel_to_underline_public():
    assert camel_to_underline("userName") == "user_name"
    assert camel_to_underline("testData") == "test_data"
    assert camel_to_underline("redBlueGreen") == "red_blue_green"

def test_join_public():
    items = ["a", "b", "c"]
    assert join(items, ",") == "a,b,c"
    assert join(items, "|") == "a|b|c"
    assert join(items, "") == "abc"