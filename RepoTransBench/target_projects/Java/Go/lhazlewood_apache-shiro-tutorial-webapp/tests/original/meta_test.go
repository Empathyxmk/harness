package original

import (
	"os"
	"testing"
)

func TestMetaTest_ProjectStructureExists(t *testing.T) {
	if _, err := os.Stat("pom.xml"); err != nil {
		t.Errorf("pom.xml should exist, but failed: %v", err)
	}
	if _, err := os.Stat("README.md"); err != nil {
		t.Errorf("README.md should exist, but failed: %v", err)
	}
}