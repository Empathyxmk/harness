package original

import (
	"testing"
	"uuslug"
)

// Test that the main uuslug package exports the expected symbols.
func TestImportAll(t *testing.T) {
	if _, ok := any(uuslug.Uuslug).(func(string, interface{}, ...interface{}) (string, error)); !ok {
		t.Error("uuslug should have a 'Uuslug' function")
	}
	if _, ok := any(uuslug.Slugify).(func(string, ...interface{}) string); !ok {
		t.Error("uuslug should have a 'Slugify' function")
	}
}