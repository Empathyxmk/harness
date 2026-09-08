import pytest

def build_s3_params(input_dict):
    # Simulate minimal S3 parameter builder
    if "Bucket" not in input_dict or "Key" not in input_dict:
        raise ValueError("Missing S3 bucket or key")
    # Pass through other params
    params = dict(input_dict)
    params["Built"] = True
    return params

def test_s3_parameter_builder_success():
    params = build_s3_params({"Bucket": "my-bucket", "Key": "thekey", "ContentType": "text/html"})
    assert params["Bucket"] == "my-bucket"
    assert params["Key"] == "thekey"
    assert params["ContentType"] == "text/html"
    assert params["Built"] is True

def test_s3_parameter_builder_missing_bucket():
    with pytest.raises(ValueError):
        build_s3_params({"Key": "thekey"})

def test_s3_parameter_builder_missing_key():
    with pytest.raises(ValueError):
        build_s3_params({"Bucket": "my-bucket"})