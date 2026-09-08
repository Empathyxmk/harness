package public_tests

import (
	"testing"
	"uuslug"
)

func TestImportAllPublic(t *testing.T) {
	if _, ok := any(uuslug.Uuslug).(func(string, interface{}, ...interface{}) (string, error)); !ok {
		t.Error("uuslug should have a 'Uuslug' function")
	}
	if _, ok := any(uuslug.Slugify).(func(string, ...interface{}) string); !ok {
		t.Error("uuslug should have a 'Slugify' function")
	}
	// Variation: check for __version__
	if uuslug.Version == "" {
		t.Error("uuslug should have a '__version__' field")
	}
}