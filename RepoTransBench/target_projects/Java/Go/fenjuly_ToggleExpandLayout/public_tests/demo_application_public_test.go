package public_tests

import "testing"

// Public version of ApplicationTest (demo)
func TestDemoApplicationPublicTest(t *testing.T) {
	app := struct{}{}
	if app == nil {
		t.Error("Application should not be nil")
	}
}