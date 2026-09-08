package tests

import (
	"os"
	"path/filepath"
	"testing"
)

func writeText(filename, content string) error {
	return os.WriteFile(filename, []byte(content), 0644)
}

func TestGetVersionAndLongDesc(t *testing.T) {
	// Simulate a minimal __init__.py with __version__, and README.md
	tmpDir := t.TempDir()
	fapiDir := filepath.Join(tmpDir, "fastapi_events")
	err := os.Mkdir(fapiDir, 0755)
	if err != nil {
		t.Fatalf("failed to make fastapi_events dir: %v", err)
	}
	initFile := filepath.Join(fapiDir, "__init__.py")
	readmeFile := filepath.Join(tmpDir, "README.md")
	if err := writeText(initFile, `__version__ = "9.0.1"`+"\n"); err != nil {
		t.Fatalf("failed to write __init__.py: %v", err)
	}
	if err := writeText(readmeFile, "Hello this is a desc!"); err != nil {
		t.Fatalf("failed to write README.md: %v", err)
	}

	// Simulate get_version and get_long_description
	getVersion := func() (string, error) {
		data, err := os.ReadFile(initFile)
		if err != nil {
			return "", err
		}
		lines := string(data)
		for _, line := range []string{lines} {
			if len(line) > 0 && line[:12] == "__version__ =" {
				v := line[13:]
				if len(v) > 0 && v[0] == '"' {
					v = v[1 : len(v)-1]
				}
				return v, nil
			}
		}
		return "", nil
	}
	getLongDesc := func() (string, error) {
		data, err := os.ReadFile(readmeFile)
		return string(data), err
	}
	version, err := getVersion()
	if err != nil {
		t.Fatalf("getVersion error: %v", err)
	}
	if version != "9.0.1" {
		t.Errorf("expected version 9.0.1, got %q", version)
	}
	desc, err := getLongDesc()
	if err != nil {
		t.Fatalf("getLongDesc error: %v", err)
	}
	if desc == "" || desc != "Hello this is a desc!" {
		t.Errorf("expected description 'Hello this is a desc!', got %q", desc)
	}
}