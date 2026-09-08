package public_tests

import "testing"

// Public version of ApplicationTest (library)
func TestLibraryApplicationPublicTest(t *testing.T) {
	app := struct{}{}
	if app == nil {
		t.Error("Application should not be nil")
	}
}