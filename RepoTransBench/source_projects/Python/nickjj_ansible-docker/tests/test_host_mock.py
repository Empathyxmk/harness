import types
import re

import pytest

class DummyRunResult:
    def __init__(self, rc):
        self.rc = rc

class DummyFile:
    def __init__(self, content):
        self.content_string = content

    def contains(self, needle):
        return needle in self.content_string

class DummyUser:
    def __init__(self, groups):
        self.groups = groups

class DummyHost:
    def __init__(self):
        self.docker_version = "Docker version 20.10.10, build b485636"
        self.docker_compose_version = "Docker Compose version v2.3.3"
        self.daemon_json_content = '{"log-driver":"journald","dns":["8.8.8.8"]}'
        self.environment_file = 'Environment="HTTP_PROXY=http://proxy"\nEnvironment="HTTPS_PROXY=https://proxy"'
        self.options_file = "-H fd:// --debug"
        self.custom_conf_file = "ATest"
        self.cron_file = "0 * * * * test docker system prune -af"
        self.user_groups = ["docker", "test"]

    def run(self, command):
        if "docker --version" in command:
            return DummyRunResult(rc=0)
        if "docker compose version" in command:
            return DummyRunResult(rc=0)
        if "python3-docker" in command:
            return DummyRunResult(rc=0)
        return DummyRunResult(rc=1)

    def check_output(self, command):
        if command == "docker --version":
            return self.docker_version
        if command == "docker compose version":
            return self.docker_compose_version
        return "UNKNOWN"

    def user(self, name):
        return DummyUser(groups=self.user_groups)

    def file(self, path):
        if path == "/etc/docker/daemon.json":
            return DummyFile(self.daemon_json_content)
        if path == "/etc/systemd/system/docker.service.d/environment.conf":
            return DummyFile(self.environment_file)
        if path == "/etc/systemd/system/docker.service.d/options.conf":
            return DummyFile(self.options_file)
        if path == "/etc/systemd/system/docker.service.d/custom.conf":
            return DummyFile(self.custom_conf_file)
        if path == "/etc/cron.d/docker-disk-clean-up":
            return DummyFile(self.cron_file)
        return DummyFile("")

@pytest.fixture
def host():
    return DummyHost()

def test_docker_version(host):
    assert 0 == host.run("docker --version").rc

def test_pinned_docker_version(host):
    existing_docker_version = host.check_output("docker --version")
    host.run("sudo apt-get update")
    host.run("sudo apt-get upgrade")
    docker_version_after_apt_update = host.check_output("docker --version")
    assert existing_docker_version == docker_version_after_apt_update

def test_docker_compose_v2_version(host):
    assert 0 == host.run("docker compose version").rc

def test_pinned_docker_compose_v2_version(host):
    existing_docker_compose_version = host.check_output("docker compose version")
    host.run("sudo apt-get update")
    host.run("sudo apt-get upgrade")
    docker_compose_version_after_apt_update = host.check_output("docker compose version")
    assert existing_docker_compose_version == docker_compose_version_after_apt_update

def test_able_to_access_docker_without_root(host):
    assert "docker" in host.user("test").groups

def test_daemon_json_is_configured(host):
    daemon_json = host.file("/etc/docker/daemon.json")
    assert daemon_json.contains("journald")
    assert daemon_json.contains("8.8.8.8")

def test_customized_environment_systemd_unit_file(host):
    unit_file = "/etc/systemd/system/docker.service.d/environment.conf"
    file_contents = host.file(unit_file).content_string
    assert re.search(r"Environment=\"HTTP_PROXY=.*\"", file_contents)
    assert re.search(r"Environment=\"HTTPS_PROXY=.*\"", file_contents)

def test_customized_daemon_flags_systemd_unit_file(host):
    unit_file = "/etc/systemd/system/docker.service.d/options.conf"
    file_contents = host.file(unit_file).content_string
    assert "-H fd://" in file_contents
    assert "--debug" in file_contents

def test_customized_systemd_override(host):
    unit_file = "/etc/systemd/system/docker.service.d/custom.conf"
    file_contents = host.file(unit_file).content_string
    assert "ATest" in file_contents

def test_docker_clean_up_cron_job(host):
    cron_conf = host.file("/etc/cron.d/docker-disk-clean-up").content_string
    assert "test docker system prune -af" in cron_conf

def test_python_docker_module(host):
    assert 0 == host.run("python3-docker -c 'import docker'").rc

def test_daemon_json_missing_keys(host):
    # Missing content
    f = host.file("/wrong/path")
    assert not f.contains("journald")
    assert not f.contains("8.8.8.8")

def test_customized_environment_systemd_unit_file_missing_keys(host):
    # Should not find proxies in empty file
    file_contents = host.file("/wrong/path").content_string
    assert not re.search(r"Environment=\"HTTP_PROXY=.*\"", file_contents or "")
    assert not re.search(r"Environment=\"HTTPS_PROXY=.*\"", file_contents or "")

def test_file_object_empty(host):
    assert host.file("/nonexistent/path").content_string == ""

def test_user_without_docker_group():
    class NoDockerUser(DummyUser):
        def __init__(self):
            self.groups = ["test"]
    class NoDockerHost(DummyHost):
        def user(self, name):
            return NoDockerUser()
    h = NoDockerHost()
    assert "docker" not in h.user("test").groups