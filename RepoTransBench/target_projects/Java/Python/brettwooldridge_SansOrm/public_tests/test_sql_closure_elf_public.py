def get_field_value(obj, field):
    return getattr(obj, field)

def set_field_value(obj, field, value):
    setattr(obj, field, value)

class SampleEntity:
    publicInt: int
    publicString: str

def test_get_field_value_public():
    obj = SampleEntity()
    obj.publicInt = 77
    obj.publicString = "helloPublic"
    assert get_field_value(obj, "publicInt") == 77
    assert get_field_value(obj, "publicString") == "helloPublic"

def test_set_field_value_public():
    obj = SampleEntity()
    set_field_value(obj, "publicInt", 51)
    set_field_value(obj, "publicString", "worldPublic")
    assert obj.publicInt == 51
    assert obj.publicString == "worldPublic"