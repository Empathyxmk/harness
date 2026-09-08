import uuid

def test_public_uuid1_not_equal():
    u1 = uuid.uuid1()
    u2 = uuid.uuid1()
    assert u1 != u2
    assert isinstance(u1, uuid.UUID)

def test_public_uuid5_generation():
    ns = uuid.NAMESPACE_OID
    value = "example.org"
    u = uuid.uuid5(ns, value)
    # This will always produce same value for same name/namespace
    assert str(u) == str(uuid.uuid5(ns, value))