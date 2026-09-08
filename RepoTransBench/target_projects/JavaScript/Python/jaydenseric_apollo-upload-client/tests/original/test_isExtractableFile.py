import pytest
from jaydenseric_apollo_upload_client.isExtractableFile import isExtractableFile

def test_isExtractableFile_various():
    # undefined (None in Python) => False
    assert isExtractableFile(None) is False, "None (undefined) is not extractable"
    # null (None) => False
    assert isExtractableFile(None) is False, "None (null) is not extractable"
    # number
    assert isExtractableFile(123) is False, "Number is not extractable"
    # object without type
    assert isExtractableFile({'foo': 'bar'}) is False, "Dict without type is not extractable"
    # object with type
    assert isExtractableFile({'type': 'image/gif'}) is True, "Dict with type should be extractable"
    # object with type and other keys
    assert isExtractableFile({'type': '', 'foo': 'bar'}) is True, "Dict with type and others is extractable"