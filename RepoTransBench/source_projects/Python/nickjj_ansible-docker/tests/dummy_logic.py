import re

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

    def group_in_user(self, group):
        return group in self.user_groups

    def environment_proxy_set(self):
        return (
            re.search(r"HTTP_PROXY=.*", self.environment_file)
            and re.search(r"HTTPS_PROXY=.*", self.environment_file)
        )

    def daemon_dns_ok(self):
        return "8.8.8.8" in self.daemon_json_content

    def cron_clean_up_job_valid(self):
        return "docker system prune -af" in self.cron_file