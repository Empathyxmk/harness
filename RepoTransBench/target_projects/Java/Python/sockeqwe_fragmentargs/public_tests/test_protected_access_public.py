def test_protected_field_access_test_public_variant():
    class DummyProtectedObjectPublic:
        def __init__(self):
            self.field = None
        def setValue(self, val):
            self.field = val
        def getValue(self):
            return self.field

    dummy = DummyProtectedObjectPublic()
    dummy.setValue("barBaz")
    assert dummy.getValue() == "barBaz"