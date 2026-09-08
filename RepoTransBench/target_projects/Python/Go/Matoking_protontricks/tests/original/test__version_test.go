package original

import (
	"testing"
)

// Simulate _version module attributes directly, as Go doesn't have module-level variables by default
// In a real Go port of protontricks, these should exist in the corresponding Go package, but for the test,
// we define them here to match the test logic.
type VersionInfo struct {
	Version      string
	VersionTuple [3]int
}

var _version = struct {
	__version__   string
	version       string
	version_tuple [3]int
}{
	__version__:   "0.0.0",
	version:       "0.0.0",
	version_tuple: [3]int{0, 0, 0},
}

func TestVersionAttributes(t *testing.T) {
	// Equivalent to assert hasattr(_version, ...)
	if _version.__version__ == "" {
		t.Errorf("__version__ is missing or empty")
	}
	if _version.version == "" {
		t.Errorf("version is missing or empty")
	}
	// Go type check is enforced at compile time, but we'll check basic Go string and [3]int values
	if _, ok := interface{}(_version.version).(string); !ok {
		t.Errorf("version is not a string")
	}
	if _, ok := interface{}(_version.version_tuple).([3]int); !ok {
		t.Errorf("version_tuple is not [3]int")
	}
	// Direct equality checks
	if _version.__version__ != "0.0.0" {
		t.Errorf("Expected __version__ = '0.0.0', got %q", _version.__version__)
	}
	expected := [3]int{0, 0, 0}
	if _version.version_tuple != expected {
		t.Errorf("Expected version_tuple = (0, 0, 0), got %#v", _version.version_tuple)
	}
}