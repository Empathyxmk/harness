import pytest
from unittest.mock import patch, MagicMock
import cloudconvert.task as task_mod

def test_upload_wrong_operation_public(tmp_path):
    file_path = tmp_path / "file.txt"
    with open(file_path, "w") as f:
        f.write("Test data!")

    bad_task = {'operation': 'import/url', 'result': {'form': {}}}
    with pytest.raises(Exception) as exc:
        task_mod.Upload.upload(str(file_path), bad_task)
    assert "not import/upload" in str(exc.value)

def test_upload_file_not_found_public():
    # check non-existing path but with correct operation
    with pytest.raises(Exception) as exc:
        task_mod.Upload.upload("definitely_missing.xyz", {"operation": "import/upload", "result": {"form": {}}})
    assert "exact path" in str(exc.value)

def test_upload_success_and_failure_public(tmp_path, monkeypatch):
    # Prepare file
    file_path = tmp_path / "upload_file_success.txt"
    file_path.write_text("data")
    # fake task dict with correct form
    task = {
        "operation": "import/upload",
        "result": {"form": {"url": "http://upload.url", "parameters": {"key": "val"}}}
    }

    class DummyResponse:
        def __init__(self, status_code):
            self.status_code = status_code

    send_status = []

    def fake_request(method, url, files, data):
        send_status.append((method, url, files, data))
        # first call - success, second call - fail
        return DummyResponse(201 if len(send_status) == 1 else 400)

    monkeypatch.setattr("requests.request", fake_request)
    # Should return True (201)
    assert task_mod.Upload.upload(str(file_path), task) == True
    # Second call returns 400, should yield False
    assert task_mod.Upload.upload(str(file_path), task) == False