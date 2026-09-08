package public_tests

import (
	"os"
	"path/filepath"
	"plugin"
	"testing"
	"strings"
)

func TestPublicImportPackageAndVersion(t *testing.T) {
	plg, err := plugin.Open("libsecure_package_template.so")
	if err != nil {
		t.Fatalf("Failed to load plugin: %v", err)
	}
	sym, err := plg.Lookup("__version__")
	if err != nil {
		t.Fatalf("__version__ symbol not found: %v", err)
	}
	ver, ok := (*sym).(string)
	if !ok {
		t.Fatalf("__version__ found, but not a string")
	}

	parts := strings.Split(ver, ".")
	if len(parts) < 3 {
		t.Errorf("version %q does not have at least 3 parts", ver)
	}
	for _, part := range parts {
		for _, ch := range part {
			if ch < '0' || ch > '9' {
				t.Errorf("version part %q is not numeric", part)
			}
		}
	}
}

func TestPublicDirectModuleImport(t *testing.T) {
	plg, err := plugin.Open("libsecure_package_template_version.so")
	if err != nil {
		t.Fatalf("Failed to load version plugin: %v", err)
	}
	sym, err := plg.Lookup("__version__")
	if err != nil {
		t.Fatalf("__version__ in _version not found: %v", err)
	}
	v, ok := (*sym).(string)
	if !ok {
		t.Fatalf("__version__ is not a string")
	}
	if strings.Count(v, ".") != 2 {
		t.Errorf("version %q does not match X.Y.Z pattern", v)
	}
}

func TestPublicPyTypedFileExists(t *testing.T) {
	pkgPath := "./src/secure_package_template"
	pyTypedPath := filepath.Join(pkgPath, "py.typed")
	stat, err := os.Stat(pyTypedPath)
	if err != nil {
		t.Fatalf("py.typed file does not exist: %v", err)
	}
	if stat.Size() < 0 {
		t.Errorf("py.typed file size < 0 (impossible): %d", stat.Size())
	}
}

func TestPublicReloadPreservesVersionAndType(t *testing.T) {
	plg, err := plugin.Open("libsecure_package_template.so")
	if err != nil {
		t.Fatalf("Failed to reload plugin: %v", err)
	}
	sym, err := plg.Lookup("__version__")
	if err != nil {
		t.Fatalf("__version__ symbol not found after reload: %v", err)
	}
	val, ok := (*sym).(string)
	if !ok {
		t.Fatalf("__version__ loaded after reload but not a string")
	}
	if len(val) >= 20 {
		t.Errorf("__version__ string after reload too long: %q", val)
	}
}