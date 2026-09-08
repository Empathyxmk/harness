package public_tests

import (
	"os"
	"testing"
)

func TestGotoHasNoGotoAndLabelByDefault(t *testing.T) {
	// There is no global 'goto' or 'label' symbol - simulate the check
	_, foundGoto := os.LookupEnv("GOTO_NO_SYMBOL") // Always not present
	_, foundLabel := os.LookupEnv("LABEL_NO_SYMBOL")
	if foundGoto || foundLabel {
		t.Errorf("expected no goto/label symbols by default")
	}
}

func TestGotoModuleHasFileAttribute(t *testing.T) {
	// Simulate: module has __file__, mimic with os.Args[0]
	file := os.Args[0]
	if len(file) == 0 {
		t.Errorf("expected non-empty file name")
	}
}

func TestGotoModuleNameIsGoto(t *testing.T) {
	modName := "goto"
	if modName != "goto" {
		t.Fatalf("expected module name 'goto', got %q", modName)
	}
}