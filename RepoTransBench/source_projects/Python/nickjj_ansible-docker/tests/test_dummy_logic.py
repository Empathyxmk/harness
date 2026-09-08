import sys
import os

# Ensure that the tests directory is in sys.path so that dummy_logic can be imported
sys.path.insert(0, os.path.dirname(__file__))

from dummy_logic import DummyHost, DummyUser, DummyFile

def test_group_in_user_true():
    h = DummyHost()
    assert h.group_in_user("docker") is True

def test_group_in_user_false():
    h = DummyHost()
    assert h.group_in_user("other") is False

def test_environment_proxy_set_true():
    h = DummyHost()
    assert h.environment_proxy_set() is not None

def test_environment_proxy_set_false():
    h = DummyHost()
    h.environment_file = ""
    assert not h.environment_proxy_set()

def test_daemon_dns_ok_true():
    h = DummyHost()
    assert h.daemon_dns_ok() is True

def test_daemon_dns_ok_false():
    h = DummyHost()
    h.daemon_json_content = '{"log-driver":"journald"}'
    assert not h.daemon_dns_ok()

def test_cron_clean_up_job_valid_true():
    h = DummyHost()
    assert h.cron_clean_up_job_valid() is True

def test_cron_clean_up_job_valid_false():
    h = DummyHost()
    h.cron_file = ""
    assert not h.cron_clean_up_job_valid()