import pytest

def public_s3_params(obj):
    if not obj.get("pn") or not obj.get("bk"):
        raise ValueError("Missing param")
    out = dict(obj)
    out["public"] = True
    return out

def test_s3_parameter_builder_public_success():
    params = public_s3_params({"pn": "somefile.txt", "bk": "pubbucket"})
    assert params["pn"] == "somefile.txt"
    assert params["bk"] == "pubbucket"
    assert params["public"] is True

def test_s3_parameter_builder_public_missing_param():
    with pytest.raises(ValueError):
        public_s3_params({"bk": "pubbucket"})
    with pytest.raises(ValueError):
        public_s3_params({"pn": "x"})