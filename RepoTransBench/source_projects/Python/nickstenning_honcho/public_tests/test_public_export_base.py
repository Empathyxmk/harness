import pytest
from honcho.export import base

def test_exporter_env_public(tmp_path):
    path = tmp_path / "envfile"
    path.write_text("HELLO=world\nPUBLIC=success\n")
    e = base.Exporter()
    env = e.read_environment(str(path))
    assert env["HELLO"] == "world"
    assert env["PUBLIC"] == "success"