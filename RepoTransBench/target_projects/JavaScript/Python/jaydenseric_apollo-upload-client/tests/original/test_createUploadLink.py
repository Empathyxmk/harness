import pytest
from jaydenseric_apollo_upload_client.createUploadLink import createUploadLink

def test_createUploadLink_classic():
    options = {
        'uri': '/graphql',
        'credentials': 'include',
        'headers': {'x-test': 'foo'}
    }
    link = createUploadLink(options)
    assert isinstance(link, dict), "Should return a dict"
    assert link.get('isUploadLink') is True, "Should indicate isUploadLink=True"
    assert link.get('options') == options, "Returned options property does not match"