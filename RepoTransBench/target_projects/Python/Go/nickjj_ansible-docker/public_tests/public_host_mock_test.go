package public_tests

import (
	"strings"
	"testing"

	"github.com/example/nickjj_ansible_docker/tests"
)

func TestAlternateHostname(t *testing.T) {
	h := tests.NewHostMock(tests.WithHostname("custom-server"), tests.WithOS("ubuntu"), tests.WithFamily("debian"))
	if h.Hostname != "custom-server" {
		t.Errorf("Expected hostname to be custom-server, got %v", h.Hostname)
	}
	if h.Vars["inventory_hostname"] != "custom-server" {
		t.Errorf("inventory_hostname incorrect, got %v", h.Vars["inventory_hostname"])
	}
}

func TestDifferentOSFamily(t *testing.T) {
	h := tests.NewHostMock(tests.WithHostname("web01"), tests.WithOS("fedora"), tests.WithFamily("redhat"))
	if h.OS != "fedora" {
		t.Errorf("Expected OS fedora, got %v", h.OS)
	}
	if h.Family != "redhat" {
		t.Errorf("Expected family redhat, got %v", h.Family)
	}
	if h.Vars["ansible_os_family"] != "redhat" {
		t.Errorf("ansible_os_family got %v", h.Vars["ansible_os_family"])
	}
}

func TestGroupsAndVarsPublic(t *testing.T) {
	h := tests.NewHostMock(
		tests.WithGroups([]string{"docker", "backend"}),
		tests.WithVars(map[string]interface{}{"extra": 123}),
	)
	if len(h.Groups) != 2 || h.Groups[0] != "docker" || h.Groups[1] != "backend" {
		t.Errorf("Expected docker/backend groups, got %v", h.Groups)
	}
	if h.Vars["extra"] != 123 {
		t.Errorf("vars 'extra' expected 123, got %v", h.Vars["extra"])
	}
	if h.Vars["docker_host"] != "unix:///var/run/docker.sock" {
		t.Errorf("docker_host variable mismatch, got %v", h.Vars["docker_host"])
	}
}

func TestGetitemPublic(t *testing.T) {
	h := tests.NewHostMock(tests.WithVars(map[string]interface{}{"x": 100}))
	if x := h.GetVar("x"); x != 100 {
		t.Errorf("getitem x expected 100, got %v", x)
	}
}

func TestVarsMergingPublic(t *testing.T) {
	h := tests.NewHostMock(
		tests.WithHostname("merge"),
		tests.WithVars(map[string]interface{}{"a": 90, "docker_host": "/tmp"}),
	)
	if h.Vars["a"] != 90 {
		t.Errorf("vars['a'] = 90 expected, got %v", h.Vars["a"])
	}
	if h.Vars["docker_host"] != "/tmp" {
		t.Errorf("docker_host should be /tmp, got %v", h.Vars["docker_host"])
	}
	if _, ok := h.Vars["inventory_hostname"]; !ok {
		t.Errorf("inventory_hostname missing in merged vars")
	}
}

func TestEnvvarPublic(t *testing.T) {
	h := tests.NewHostMock(tests.WithVars(map[string]interface{}{"env": "prod"}))
	if h.Vars["env"] != "prod" {
		t.Errorf("vars['env'] should be prod, got %v", h.Vars["env"])
	}
}

func TestReprOutputPublic(t *testing.T) {
	h := tests.NewHostMock(tests.WithHostname("visual"), tests.WithOS("redhat"), tests.WithFamily("rhel"))
	rep := h.String()
	if !(strings.Contains(rep, "visual") && strings.Contains(rep, "redhat") && strings.Contains(rep, "rhel")) {
		t.Errorf("HostMock String() missing expected values; got: %v", rep)
	}
}