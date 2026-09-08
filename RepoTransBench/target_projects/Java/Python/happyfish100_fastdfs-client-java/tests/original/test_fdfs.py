import pytest
from datetime import datetime
import tempfile
import os

class DummyStorageClient:
    def upload_file(self, data, ext, meta):
        # Simulated upload logic.
        return ["group1", "remote_name"]

    def download_file(self, group, remote):
        return b"dummydata"

class DummyClientGlobal:
    g_network_timeout = 30
    g_charset = "utf-8"

global ClientGlobal
ClientGlobal = DummyClientGlobal()

class DummyLogger:
    def info(self, msg):
        pass

import types

@pytest.fixture(scope="module")
def dummy_storage_client():
    return DummyStorageClient()

def write_byte_to_file(fbyte, fileName):
    with open(fileName, "wb") as f:
        f.write(fbyte)

def test_upload(dummy_storage_client):
    metaList = [{"fileName":"build.PNG"}]
    local_filename = "build.PNG"
    fake_bytes = b"\x89PNG\r\n\x1a\n"
    # Emulate reading bytes from file
    result = dummy_storage_client.upload_file(fake_bytes, None, metaList)
    assert len(result) == 2

def test_download(dummy_storage_client):
    uploadresult = ["group1", "remote_remote"]
    result = dummy_storage_client.download_file(uploadresult[0], uploadresult[1])
    assert isinstance(result, bytes)
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        write_byte_to_file(result, tmp.name)
        assert os.path.isfile(tmp.name)

def test_upload_download(dummy_storage_client):
    metaList = [{"fileName":"commitment.d2f57e10 (2).jpg"}]
    fake_bytes = b"JPEGDATABYTES"
    result = dummy_storage_client.upload_file(fake_bytes, None, metaList)
    assert len(result) == 2
    down_bytes = dummy_storage_client.download_file(result[0], result[1])
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        write_byte_to_file(down_bytes, tmp.name)
        assert os.path.isfile(tmp.name)