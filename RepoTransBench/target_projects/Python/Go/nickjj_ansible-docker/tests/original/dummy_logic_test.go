package original

import (
	"testing"

	"github.com/example/nickjj_ansible_docker/tests"
)

func newDummyHostLogic() *tests.DummyHostLogic {
	return &tests.DummyHostLogic{
		DaemonJsonContent: `{"log-driver":"journald","dns":["8.8.8.8"]}`,
		EnvironmentFile:   `Environment="HTTP_PROXY=http://proxy"` + "\n" + `Environment="HTTPS_PROXY=https://proxy"`,
		CronFile:          "0 * * * * test docker system prune -af",
	}
}

func TestGroupInUserTrue(t *testing.T) {
	h := newDummyHostLogic()
	if !h.GroupInUser("docker") {
		t.Errorf("group_in_user('docker') should be true")
	}
}

func TestGroupInUserFalse(t *testing.T) {
	h := newDummyHostLogic()
	if h.GroupInUser("other") {
		t.Errorf("group_in_user('other') should be false")
	}
}

func TestEnvironmentProxySetTrue(t *testing.T) {
	h := newDummyHostLogic()
	if !h.EnvironmentProxySet() {
		t.Errorf("environment_proxy_set() should be true")
	}
}

func TestEnvironmentProxySetFalse(t *testing.T) {
	h := newDummyHostLogic()
	h.EnvironmentFile = ""
	if h.EnvironmentProxySet() {
		t.Errorf("environment_proxy_set() should be false when environment_file is empty")
	}
}

func TestDaemonDnsOkTrue(t *testing.T) {
	h := newDummyHostLogic()
	if !h.DaemonDNSOK() {
		t.Errorf("daemon_dns_ok() should be true")
	}
}

func TestDaemonDnsOkFalse(t *testing.T) {
	h := newDummyHostLogic()
	h.DaemonJsonContent = `{"log-driver":"journald"}`
	if h.DaemonDNSOK() {
		t.Errorf("daemon_dns_ok() should be false when no dns key")
	}
}

func TestCronCleanUpJobValidTrue(t *testing.T) {
	h := newDummyHostLogic()
	if !h.CronCleanUpJobValid() {
		t.Errorf("cron_clean_up_job_valid() should be true")
	}
}

func TestCronCleanUpJobValidFalse(t *testing.T) {
	h := newDummyHostLogic()
	h.CronFile = ""
	if h.CronCleanUpJobValid() {
		t.Errorf("cron_clean_up_job_valid() should be false when cron_file is empty")
	}
}