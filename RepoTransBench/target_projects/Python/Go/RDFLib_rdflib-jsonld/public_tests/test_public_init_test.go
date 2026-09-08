package public_tests

import (
	"os"
	"path/filepath"
	"testing"
)

func TestPublicInitModuleExists(t *testing.T) {
	path := filepath.Join("rdflib_jsonld", "__init__.py")
	if _, err := os.Stat(path); os.IsNotExist(err) {
		t.Fatalf("%s does not exist", path)
	}
}