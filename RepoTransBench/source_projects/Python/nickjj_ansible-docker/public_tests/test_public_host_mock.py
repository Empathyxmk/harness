import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../tests')))
from test_host_mock import HostMock

def test_alternate_hostname():
    h = HostMock(hostname="custom-server", os="ubuntu", family="debian")
    assert h.hostname == "custom-server"
    assert h.vars["inventory_hostname"] == "custom-server"

def test_different_os_family():
    h = HostMock(hostname="web01", os="fedora", family="redhat")
    assert h.os == "fedora"
    assert h.family == "redhat"
    assert h.vars["ansible_os_family"] == "redhat"

def test_groups_and_vars_public():
    h = HostMock(groups=["docker", "backend"], vars={"extra": 123})
    assert h.groups == ["docker", "backend"]
    assert h.vars["extra"] == 123
    assert h.vars["docker_host"] == "unix:///var/run/docker.sock"

def test_getitem_public():
    h = HostMock(vars={"x": 100})
    assert h["x"] == 100

def test_vars_merging_public():
    h = HostMock(hostname="merge", vars={"a": 90, "docker_host": "/tmp"})
    # The vars provided at init should override builtins
    assert h.vars["a"] == 90
    assert h.vars["docker_host"] == "/tmp"
    # Should still have core expected vars present
    assert "inventory_hostname" in h.vars

def test_envvar_public():
    h = HostMock(vars={"env": "prod"})
    # Should just store extra var 'env'
    assert h.vars["env"] == "prod"

def test_repr_output_public():
    h = HostMock(hostname="visual", os="redhat", family="rhel")
    rep = repr(h)
    assert "visual" in rep
    assert "redhat" in rep
    assert "rhel" in rep