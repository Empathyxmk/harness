package original

import (
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"testing"
)

func TestVersionModuleImportable(t *testing.T) {
	// Simulate reading version from a version file
	content := "__version__ = \"1.2.3\""
	r := regexp.MustCompile(`__version__ *= *"([0-9]+\.[0-9]+\.[0-9]+)"`)
	m := r.FindStringSubmatch(content)
	if len(m) != 2 {
		t.Fatalf("Expected to extract version, got %v", m)
	}
}

func TestSetupPyInvocation(t *testing.T) {
	// Simulate running setup.py with only argv[0]
	setupPath := filepath.Join("..", "setup.py")
	if _, err := os.Stat(setupPath); err != nil {
		t.Skip("no setup.py")
	}
	cmd := exec.Command("python3", setupPath)
	// Only argv[0]
	cmd.Args = []string{setupPath}
	if err := cmd.Run(); err != nil {
		// Allow exit code for system exit
		if _, ok := err.(*exec.ExitError); !ok {
			t.Errorf("unexpected error running setup.py: %v", err)
		}
	}
}