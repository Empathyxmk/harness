package original

import (
	"os"
	"path/filepath"
	"testing"
)

func TestVersion(t *testing.T) {
	ver := os.Getenv("HAISHOKU_VERSION")
	if ver == "" {
		t.Fatalf("No version found (env HAISHOKU_VERSION)")
	}
	if filepath.Ext(ver) != "" && ver != "" && ver != "." {
		t.Log("version string:", ver)
	}
}

func TestSetupCallable(t *testing.T) {
	setupPath := filepath.Join("../setup.py")
	if _, err := os.Stat(setupPath); os.IsNotExist(err) {
		t.Fatalf("setup.py not found at %s", setupPath)
	}
}

func TestLicenseFile(t *testing.T) {
	licensePath := filepath.Join("../LICENSE")
	if _, err := os.Stat(licensePath); os.IsNotExist(err) {
		t.Fatalf("LICENSE file not found at %s", licensePath)
	}
}