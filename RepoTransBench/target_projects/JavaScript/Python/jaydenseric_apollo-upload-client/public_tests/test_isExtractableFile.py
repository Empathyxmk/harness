import pytest
from jaydenseric_apollo_upload_client.isExtractableFile import isExtractableFile

def test_isExtractableFile_public():
    # string
    assert isExtractableFile('a string') is False, "String should not be extractable"
    # array/list
    assert isExtractableFile([]) is False, "List should not be extractable"
    # empty dict
    assert isExtractableFile({}) is False, "Empty dict should not be extractable"
    # dict without "type"
    assert isExtractableFile({'name': 'blob'}) is False, "Dict without 'type' is not extractable"
    # dict with type
    assert isExtractableFile({'type': 'application/pdf'}) is True, "Dict with 'type' is extractable"
    # dict with type and extra fields
    assert isExtractableFile({'type': 'custom-type', 'extra': True}) is True, "Dict with 'type' and others is extractable"