from protontricks.util import lower_dict

def test_public_lower_dict():
    # Use different keys and values,
    # all keys are strings for robust comparison since util.lower_dict expects keys to have .lower()
    # see: https://github.com/Matoking/protontricks/blob/master/src/protontricks/util.py#L54
    upper_dict = {"KEY": 10, "ALPHA": 20, "Z": "VALUE", "MiXeD": "Flag", "foo": "Bar"}
    lowered = lower_dict(upper_dict)
    assert lowered == {
        "key": 10,
        "alpha": 20,
        "z": "VALUE",
        "mixed": "Flag",
        "foo": "Bar",
    }