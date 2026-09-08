package original

import (
	"strings"
	"testing"
)

var (
	__version__           = "2.1.0"
	__pypi_packagename__  = "cloudconvert"
	__endpoint_map__      = map[string]string{"live": "https://...", "test": "..."}
	__sync_endpoint_map__ = map[string]string{"sandbox": "..."}
	SANDBOX_API_KEY       = "eyJ0endiTst...etc"
	__github_reponame__   = "cloudconvert-cloudconvert-python"
)

func TestConfigValues(t *testing.T) {
	if __version__ != "2.1.0" {
		t.Errorf("Config version expected 2.1.0, got %v", __version__)
	}
	if __pypi_packagename__ != "cloudconvert" {
		t.Errorf("Config package name cloudconvert expected, got %v", __pypi_packagename__)
	}
	if _, ok := __endpoint_map__["live"]; !ok {
		t.Errorf("Config endpoint map should have live")
	}
	if _, ok := __sync_endpoint_map__["sandbox"]; !ok {
		t.Errorf("Config sync endpoint map should have sandbox")
	}
	if !strings.HasPrefix(SANDBOX_API_KEY, "eyJ0") {
		t.Errorf("SANDBOX_API_KEY must start with 'eyJ0'")
	}
}

func TestConfigImports(t *testing.T) {
	// import present
	if __github_reponame__ == "" {
		t.Errorf("Config must have __github_reponame__")
	}
}