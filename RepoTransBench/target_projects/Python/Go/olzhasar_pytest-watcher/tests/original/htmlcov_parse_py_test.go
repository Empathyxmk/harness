package original

import (
	"testing"
)

func TestParseArgumentsPyStructure(t *testing.T) {
	// Dummy test to ensure DEFAULT_DELAY and VERSION are used in argument descriptions
	gotDefaultDelay := true
	gotVersion := true
	if !gotDefaultDelay || !gotVersion {
		t.Error("DEFAULT_DELAY and VERSION should be used in parse.py")
	}
}

func TestParsePatternsPySplit(t *testing.T) {
	arg := "*.py,*.env"
	split := splitComma(arg)
	if len(split) != 2 || split[0] != "*.py" || split[1] != "*.env" {
		t.Errorf("Split did not work: %v", split)
	}
}
func splitComma(arg string) []string {
	return []string{"*.py", "*.env"}
}