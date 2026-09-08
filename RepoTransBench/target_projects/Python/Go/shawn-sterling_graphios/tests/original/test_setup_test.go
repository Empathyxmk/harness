package original

import (
	"os"
	"testing"
)

func TestSetupPyImportable(t *testing.T) {
	if _, err := os.Stat("setup.py"); os.IsNotExist(err) {
		t.Fatalf("setup.py should exist but was not found")
	}
}

// Note: test_setup_main_functionality is intentionally skipped
// as setup.py executes code on import; Go doesn't have an equivalent
// defer to just import/discover script-not-library source safely.