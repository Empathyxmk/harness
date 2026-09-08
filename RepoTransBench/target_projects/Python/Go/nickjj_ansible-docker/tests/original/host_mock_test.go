package original

import (
	"regexp"
	"strings"
	"testing"

	"github.com/example/nickjj_ansible_docker/tests"
)

func getHost() *tests.DummyHost {
	return tests.NewDummyHost()
}

func TestDockerVersion(t *testing.T) {
	host := getHost()
	if host.Run("docker --version").RC != 0 {
		t.Errorf("Expected docker --version rc=0")
	}
}

func TestPinnedDockerVersion(t *testing.T) {
	host := getHost()
	existing := host.CheckOutput("docker --version")
	host.Run("sudo apt-get update")
	host.Run("sudo apt-get upgrade")
	after := host.CheckOutput("docker --version")
	if existing != after {
		t.Errorf("Docker version changed after apt upgrade; want %v, got %v", existing, after)
	}
}

func TestDockerComposeV2Version(t *testing.T) {
	host := getHost()
	if host.Run("docker compose version").RC != 0 {
		t.Errorf("Expected docker compose version rc=0")
	}
}

func TestPinnedDockerComposeV2Version(t *testing.T) {
	host := getHost()
	existing := host.CheckOutput("docker compose version")
	host.Run("sudo apt-get update")
	host.Run("sudo apt-get upgrade")
	after := host.CheckOutput("docker compose version")
	if existing != after {
		t.Errorf("Docker compose version changed after apt upgrade")
	}
}

func TestAbleToAccessDockerWithoutRoot(t *testing.T) {
	host := getHost()
	user := host.User("test")
	found := false
	for _, g := range user.Groups {
		if g == "docker" {
			found = true
			break
		}
	}
	if !found {
		t.Errorf("Expected 'docker' in user groups, got %v", user.Groups)
	}
}

func TestDaemonJsonIsConfigured(t *testing.T) {
	host := getHost()
	daemonFile := host.File("/etc/docker/daemon.json")
	if !daemonFile.Contains("journald") {
		t.Errorf("daemon.json missing journald")
	}
	if !daemonFile.Contains("8.8.8.8") {
		t.Errorf("daemon.json missing 8.8.8.8")
	}
}

func TestCustomizedEnvironmentSystemdUnitFile(t *testing.T) {
	host := getHost()
	fileContents := host.File("/etc/systemd/system/docker.service.d/environment.conf").ContentString
	httpProxyMatched, _ := regexp.MatchString(`Environment="HTTP_PROXY=.*"`, fileContents)
	httpsProxyMatched, _ := regexp.MatchString(`Environment="HTTPS_PROXY=.*"`, fileContents)
	if !httpProxyMatched {
		t.Errorf("environment.conf missing HTTP_PROXY, got: %q", fileContents)
	}
	if !httpsProxyMatched {
		t.Errorf("environment.conf missing HTTPS_PROXY, got: %q", fileContents)
	}
}

func TestCustomizedDaemonFlagsSystemdUnitFile(t *testing.T) {
	host := getHost()
	fileContents := host.File("/etc/systemd/system/docker.service.d/options.conf").ContentString
	if !strings.Contains(fileContents, "-H fd://") {
		t.Errorf("options.conf missing -H fd://")
	}
	if !strings.Contains(fileContents, "--debug") {
		t.Errorf("options.conf missing --debug")
	}
}

func TestCustomizedSystemdOverride(t *testing.T) {
	host := getHost()
	fileContents := host.File("/etc/systemd/system/docker.service.d/custom.conf").ContentString
	if !strings.Contains(fileContents, "ATest") {
		t.Errorf("custom.conf missing ATest")
	}
}

func TestDockerCleanUpCronJob(t *testing.T) {
	host := getHost()
	crontxt := host.File("/etc/cron.d/docker-disk-clean-up").ContentString
	if !strings.Contains(crontxt, "test docker system prune -af") {
		t.Errorf("docker-disk-clean-up cron missing string")
	}
}

func TestPythonDockerModule(t *testing.T) {
	host := getHost()
	if host.Run("python3-docker -c 'import docker'").RC != 0 {
		t.Errorf("Expected python3-docker to successfully import docker module")
	}
}

func TestDaemonJsonMissingKeys(t *testing.T) {
	host := getHost()
	f := host.File("/wrong/path")
	if f.Contains("journald") {
		t.Errorf("Expected no journald in /wrong/path")
	}
	if f.Contains("8.8.8.8") {
		t.Errorf("Expected no 8.8.8.8 in /wrong/path")
	}
}

func TestCustomizedEnvironmentSystemdUnitFileMissingKeys(t *testing.T) {
	host := getHost()
	fileContents := host.File("/wrong/path").ContentString
	reHttp := regexp.MustCompile(`Environment="HTTP_PROXY=.*"`)
	reHttps := regexp.MustCompile(`Environment="HTTPS_PROXY=.*"`)
	if reHttp.MatchString(fileContents) {
		t.Errorf("Expected missing HTTP_PROXY in empty environment file: %q", fileContents)
	}
	if reHttps.MatchString(fileContents) {
		t.Errorf("Expected missing HTTPS_PROXY in empty environment file: %q", fileContents)
	}
}

func TestFileObjectEmpty(t *testing.T) {
	host := getHost()
	if host.File("/nonexistent/path").ContentString != "" {
		t.Errorf("Expected empty ContentString for nonexistent path")
	}
}

func TestUserWithoutDockerGroup(t *testing.T) {
	// Test user without docker group
	type NoDockerUser struct{ Groups []string }
	type NoDockerHost struct {
		*tests.DummyHost
	}
	user := NoDockerUser{Groups: []string{"test"}}
	host := NoDockerHost{tests.NewDummyHost()}
	// override the User method
	oldUser := host.DummyHost.User
	host.DummyHost.User = func(name string) *tests.DummyUser { return &tests.DummyUser{Groups: user.Groups} }
	defer func() { host.DummyHost.User = oldUser }()

	groups := host.User("test").Groups
	for _, g := range groups {
		if g == "docker" {
			t.Fatalf("User should *not* have docker group in this test, got %v", groups)
		}
	}
}