package original

import (
	"errors"
	"strings"
	"testing"
)

type zbarLib struct {
	platform string
	loadErr  error
}

func (z *zbarLib) load() (string, []string, error) {
	if z.platform == "Not windows" {
		if z.loadErr != nil {
			return "", nil, z.loadErr
		}
		return "libzbar.so", []string{}, nil
	}
	if z.platform == "Windows" {
		if z.loadErr != nil {
			return "", nil, z.loadErr
		}
		return "dll fname", []string{"dll fname"}, nil
	}
	return "", nil, errors.New("unsupported platform")
}

func (z *zbarLib) searchPaths() []string {
	return []string{"libzbar-32.dll", "libzbar-64.dll", "libiconv-2.dll", "libiconv.dll"}
}

func TestFoundNonWindows(t *testing.T) {
	lib := &zbarLib{platform: "Not windows"}
	filename, paths, err := lib.load()
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if filename != "libzbar.so" {
		t.Fatalf("got %v, want libzbar.so", filename)
	}
	if len(paths) != 0 {
		t.Fatalf("unexpected dependencies: %v", paths)
	}
}

func TestNotFoundNonWindows(t *testing.T) {
	lib := &zbarLib{platform: "Not windows", loadErr: errors.New("not found")}
	_, _, err := lib.load()
	if err == nil {
		t.Fatalf("Expected error for missing zbar")
	}
}

func TestFoundWindows(t *testing.T) {
	lib := &zbarLib{platform: "Windows"}
	filename, deps, err := lib.load()
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if filename != "dll fname" {
		t.Errorf("got %v, want dll fname", filename)
	}
	if len(deps) != 1 || deps[0] != "dll fname" {
		t.Errorf("expected dependencies: dll fname, got %v", deps)
	}
}

func TestNotFoundWindows(t *testing.T) {
	lib := &zbarLib{platform: "Windows", loadErr: errors.New("OSError")}
	_, _, err := lib.load()
	if err == nil {
		t.Errorf("Expected OSError for load")
	}
}

func TestSearchPathsIncludeLibrary(t *testing.T) {
	lib := &zbarLib{}
	found := false
	for _, path := range lib.searchPaths() {
		if strings.Contains(path, "zbar") {
			found = true
		}
	}
	if !found {
		t.Errorf("expected at least one zbar path")
	}
}

// WindowsFnames - mimic the two scenarios
func windowsFnames(maxsize int) (string, []string) {
	if maxsize == 1<<32 {
		return "libzbar-32.dll", []string{"libiconv-2.dll"}
	}
	return "libzbar-64.dll", []string{"libiconv.dll"}
}

func Test32bit(t *testing.T) {
	dll, deps := windowsFnames(1 << 32)
	if dll != "libzbar-32.dll" || len(deps) != 1 || deps[0] != "libiconv-2.dll" {
		t.Errorf("Expected 32bit fnames")
	}
}
func Test64bit(t *testing.T) {
	dll, deps := windowsFnames((1 << 32) + 1)
	if dll != "libzbar-64.dll" || len(deps) != 1 || deps[0] != "libiconv.dll" {
		t.Errorf("Expected 64bit fnames")
	}
}