import pytest
from itsdangerous import Serializer, BadSignature, BadData

def test_serializer_dumps_loads():
    s = Serializer("secret-key")
    data = {"hello": "world"}
    dumped = s.dumps(data)
    loaded = s.loads(dumped)
    assert loaded == data

def test_serializer_loads_bad_signature():
    s = Serializer("secret-key")
    bad_token = "bad-token"
    with pytest.raises(BadSignature):
        s.loads(bad_token)

def test_serializer_loads_payload_variants():
    s = Serializer("secret-key")
    data = {"foo": "bar"}
    dumped = s.dumps(data)
    # return_payload default (should just return value)
    loaded = s.loads(dumped, return_payload=False)
    assert loaded == data
    # return_payload=True: Not all Serializers return tuple, this checks only that value is correct
    loaded_payload = s.loads(dumped, return_payload=True)
    assert loaded_payload == data

def test_serializer_dump_and_load_to_file(tmp_path):
    s = Serializer("secret")
    data = {"a": 1, "b": 2}
    file_path = tmp_path / "token.txt"
    # Use text mode for file, as dumps returns str (not bytes)
    with open(file_path, "w") as f:
        s.dump(data, f)
    with open(file_path, "r") as f:
        loaded = s.load(f)
    assert loaded == data