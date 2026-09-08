package original

import (
	"os"
	"path/filepath"
	"plugin"
	"testing"
	"reflect"
)

func TestImportPackageAndVersion(t *testing.T) {
	// Simulate importing the "secure_package_template" Go package as a plugin
	plg, err := plugin.Open("libsecure_package_template.so")
	if err != nil {
		t.Fatalf("Failed to load plugin: %v", err)
	}
	sym, err := plg.Lookup("__version__")
	if err != nil {
		t.Fatalf("__version__ symbol not found: %v", err)
	}

	version, ok := (*sym).(string)
	if !ok {
		t.Fatalf("__version__ found, but not a string")
	}
	if len(version) == 0 {
		t.Error("__version__ is empty")
	}
}

func TestDirectModuleImport(t *testing.T) {
	// Simulate direct import of a _version submodule as a plugin
	plg, err := plugin.Open("libsecure_package_template_version.so")
	if err != nil {
		t.Fatalf("Failed to load _version plugin: %v", err)
	}
	sym, err := plg.Lookup("__version__")
	if err != nil {
		t.Fatalf("__version__ in _version not found: %v", err)
	}
	_, ok := (*sym).(string)
	if !ok {
		t.Errorf("__version__ in _version is not a string")
	}
}

func TestPyTypedFileExists(t *testing.T) {
	// Simulate: py.typed file should exist in the package directory
	pkgPath := "./src/secure_package_template"
	pyTypedPath := filepath.Join(pkgPath, "py.typed")
	_, err := os.Stat(pyTypedPath)
	if err != nil {
		t.Fatalf("py.typed does not exist in package directory: %v", err)
	}
}

func TestReloadPreservesVersion(t *testing.T) {
	// In Go, re-import isn't direct. We'll load/unload via plugin as a simulation
	plg, err := plugin.Open("libsecure_package_template.so")
	if err != nil {
		t.Fatalf("Failed to import (plugin open): %v", err)
	}
	sym, err := plg.Lookup("__version__")
	if err != nil {
		t.Fatalf("Failed to lookup __version__ after reload: %v", err)
	}
	if reflect.TypeOf(*sym).Kind() != reflect.String {
		t.Error("__version__ does not exist after reload or is not string")
	}
}