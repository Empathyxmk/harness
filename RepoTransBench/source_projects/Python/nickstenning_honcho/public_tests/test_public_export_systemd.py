import pytest
from honcho.export import systemd

def test_systemd_get_master_target_name_public():
    assert systemd.get_master_target_name("foobar") == "foobar-master.target"
    assert systemd.get_master_target_name("qwerty") == "qwerty-master.target"

def test_systemd_get_service_name_public():
    assert systemd.get_service_name("myapp", "api", 5) == "myapp-api-5.service"
    assert systemd.get_service_name("weather", "web", 2) == "weather-web-2.service"

def test_systemd_get_service_and_master_target_public():
    files = list(systemd.get_service_and_master_target(
        "foo", {"worker": "python app.py"}, concurrency={"worker": 2}))
    file_names = sorted([f.name for f in files])
    assert "foo-master.target" in file_names
    assert any(f.name == "foo-worker-1.service" for f in files)
    assert any(f.name == "foo-worker-2.service" for f in files)