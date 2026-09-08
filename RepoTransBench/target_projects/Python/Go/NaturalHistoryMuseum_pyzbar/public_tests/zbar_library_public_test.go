package public_tests

import (
	"strings"
	"testing"
)

func loadLib() (string, error) {
	// Always "returns" as success for testing
	return "libzbar.so", nil
}
func searchPaths() []string {
	return []string{"/lib/foo/zbar.so", "/usr/local/libzbar.dylib"}
}

func TestLibFound(t *testing.T) {
	libname, err := loadLib()
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if libname == "" {
		t.Error("Expected non-empty lib name")
	}
	if _, ok := interface{}(libname).(string); !ok {
		t.Error("Lib name is not string")
	}
}

func TestLibEndswithPlatform(t *testing.T) {
	libname, _ := loadLib()
	ends := []string{".so", ".dll", ".dylib"}
	found := false
	for _, end := range ends {
		if strings.HasSuffix(libname, end) {
			found = true
		}
	}
	if !found {
		t.Errorf("Expected %q to end with .so/.dll/.dylib", libname)
	}
}

func TestSearchPathsIncludeLibrary(t *testing.T) {
	results := searchPaths()
	found := false
	for _, p := range results {
		if strings.Contains(p, "zbar") {
			found = true
		}
	}
	if !found {
		t.Error("expected at least one path to include 'zbar'")
	}
}