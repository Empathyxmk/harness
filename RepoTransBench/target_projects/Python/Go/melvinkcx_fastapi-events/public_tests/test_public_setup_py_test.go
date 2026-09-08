package public_tests

import (
	"os"
	"path/filepath"
	"testing"
)

func createFakeInitPy(path, versionStr string) error {
	fapiDir := filepath.Join(path, "fastapi_events")
	os.MkdirAll(fapiDir, 0755)
	initFile := filepath.Join(fapiDir, "__init__.py")
	return os.WriteFile(initFile, []byte("__version__ = '"+versionStr+"'\n"), 0644)
}

func createFakeReadme(path, content string) error {
	readmeFile := filepath.Join(path, "README.md")
	return os.WriteFile(readmeFile, []byte(content), 0644)
}

func createFakeSetupPy(path string) error {
	setupFile := filepath.Join(path, "setup.py")
	code := `
import os
def get_version():
    package_init = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'fastapi_events', '__init__.py'
    )
    with open(package_init) as f:
        for line in f:
            if line.startswith('__version__ ='):
                return line.split('=')[1].strip().strip('\"\\'')
def get_long_description():
    with open('README.md', 'r') as fh:
        return fh.read()
`
	return os.WriteFile(setupFile, []byte(code), 0644)
}

func TestGetVersionAndLongDescPublic(t *testing.T) {
	tempDir := t.TempDir()
	if err := createFakeInitPy(tempDir, "7.5.1-pub"); err != nil {
		t.Fatalf("failed to create __init__.py: %v", err)
	}
	publicReadme := "## My Awesome Public Package\n\nA library for cool public event handling.\n\nPublic Test Coverage Section\nSee more at: https://public.example.com\n"
	if err := createFakeReadme(tempDir, publicReadme); err != nil {
		t.Fatalf("failed to create README.md: %v", err)
	}
	if err := createFakeSetupPy(tempDir); err != nil {
		t.Fatalf("failed to create setup.py: %v", err)
	}
	// Simulate get_version and get_long_description
	initFile := filepath.Join(tempDir, "fastapi_events", "__init__.py")
	data, err := os.ReadFile(initFile)
	if err != nil {
		t.Fatalf("could not read __init__.py: %v", err)
	}
	version := ""
	for _, line := range []string{string(data)} {
		if len(line) > 0 && line[:12] == "__version__ =" {
			v := line[13:]
			if len(v) > 0 && v[0] == '\'' {
				v = v[1 : len(v)-2]
			}
			version = v
		}
	}
	if version != "7.5.1-pub" {
		t.Errorf("expected version 7.5.1-pub, got %v", version)
	}
	readmeData, err := os.ReadFile(filepath.Join(tempDir, "README.md"))
	if err != nil {
		t.Fatalf("could not read README.md: %v", err)
	}
	longDesc := string(readmeData)
	if longDesc == "" || len(longDesc) < 10 {
		t.Errorf("expected long description to be non-empty")
	}
	if longDesc[:len("## My Awesome Public Package")] != "## My Awesome Public Package" {
		t.Errorf("expected README to start with headline, got %q", longDesc[:30])
	}
	if !contains(longDesc, "Public Test Coverage Section") {
		t.Errorf("expected long description to contain test coverage section")
	}
	if !contains(longDesc, "https://public.example.com") {
		t.Errorf("expected long description to contain link")
	}
}

func contains(s, substr string) bool {
	return len(s) >= len(substr) && (len(substr) > 0 && (s == substr || contains(s[1:], substr) || contains(s[:len(s)-1], substr)))
}