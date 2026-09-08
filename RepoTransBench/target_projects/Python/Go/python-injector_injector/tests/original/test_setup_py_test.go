package original

import (
	"os"
	"strings"
	"testing"
)

func TestSetupPyExistsAndHasSetupCall(t *testing.T) {
	// Check if the file exists
	if _, err := os.Stat("setup.py"); err != nil {
		t.Fatalf("setup.py does not exist: %v", err)
	}
	content, err := os.ReadFile("setup.py")
	if err != nil {
		t.Fatalf("failed to open setup.py: %v", err)
	}
	text := string(content)
	if !strings.Contains(text, "setup(") {
		t.Errorf("expected 'setup(' in setup.py, but not found")
	}
	if !strings.Contains(text, "__name__") {
		t.Errorf("expected '__name__' in setup.py, but not found")
	}
}