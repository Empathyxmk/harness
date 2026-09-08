import pytest
import cloudconvert.task as taskmod
import tempfile
import os

class DummyTask(dict):
    pass

def make_task(valid=True):
    # Returns a fake task dict mimicking what cloudconvert expects
    if valid:
        return {
            'operation': 'import/upload',
            'result': {
                'form': {
                    'url': 'http://dummy-upload',
                    'parameters': {'key': 'value'}
                }
            }
        }
    else:
        return {
            'operation': 'other'
        }

def test_upload_correct(monkeypatch):
    dummy_file = tempfile.NamedTemporaryFile(delete=False)
    dummy_file.write(b"hello")
    dummy_file.close()
    dummy_task = make_task()

    class DummyResp:
        status_code = 201
    def fake_request(method, url, files, data):
        assert method == 'POST'
        assert url == 'http://dummy-upload'
        return DummyResp()
    monkeypatch.setattr("requests.request", fake_request)

    res = taskmod.Upload.upload(dummy_file.name, dummy_task)
    os.unlink(dummy_file.name)
    assert res is True

def test_upload_wrong_operation():
    dummy_task = make_task(valid=False)
    with pytest.raises(Exception) as ex:
        taskmod.Upload.upload("file", dummy_task)
    assert "task operation is not import/upload" in str(ex.value)

def test_upload_missing_file(tmp_path):
    dummy_task = make_task()
    fake_file = tmp_path / "nonexistant.file"
    with pytest.raises(Exception) as ex:
        taskmod.Upload.upload(str(fake_file), dummy_task)
    assert "Does not find the exact path" in str(ex.value)

def test_upload_http_failure(monkeypatch):
    dummy_file = tempfile.NamedTemporaryFile(delete=False)
    dummy_file.write(b"fail")
    dummy_file.close()
    dummy_task = make_task()

    class DummyResp:
        status_code = 400
    def fake_request(method, url, files, data):
        return DummyResp()
    monkeypatch.setattr("requests.request", fake_request)
    result = taskmod.Upload.upload(dummy_file.name, dummy_task)
    os.unlink(dummy_file.name)
    assert result is False

def test_upload_exception(monkeypatch):
    dummy_file = tempfile.NamedTemporaryFile(delete=False)
    dummy_file.write(b"fail2")
    dummy_file.close()
    dummy_task = make_task()

    def fake_request(**kwargs):
        raise Exception("simulated error")
    monkeypatch.setattr("requests.request", fake_request)
    res = taskmod.Upload.upload(dummy_file.name, dummy_task)
    os.unlink(dummy_file.name)
    assert res is False