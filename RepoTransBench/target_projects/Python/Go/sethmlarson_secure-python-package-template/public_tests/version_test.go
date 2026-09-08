package public_tests

import (
	"plugin"
	"strings"
	"testing"
)

func TestPublicVersionModuleImportableAndFormat(t *testing.T) {
	plg, err := plugin.Open("libsecure_package_template_version.so")
	if err != nil {
		t.Fatalf("Failed to load _version plugin: %v", err)
	}
	sym, err := plg.Lookup("__version__")
	if err != nil {
		t.Fatalf("__version__ symbol not found: %v", err)
	}
	v, ok := (*sym).(string)
	if !ok {
		t.Fatalf("__version__ is not a string")
	}
	parts := strings.Split(v, ".")
	if len(parts) < 2 {
		t.Fatalf("version has fewer than 2 parts: %q", v)
	}
	if parts[0] != "0" {
		t.Errorf("major version expected 0, got %q", parts[0])
	}
	if parts[1] != "7" {
		t.Errorf("minor version expected 7, got %q", parts[1])
	}
}

func TestPublicVersionAttributeConsistencyAndNotEmpty(t *testing.T) {
	mainPkg, err := plugin.Open("libsecure_package_template.so")
	if err != nil {
		t.Fatalf("Failed to load package plugin: %v", err)
	}
	verPkg, err := plugin.Open("libsecure_package_template_version.so")
	if err != nil {
		t.Fatalf("Failed to load _version plugin: %v", err)
	}
	syma, err := mainPkg.Lookup("__version__")
	symb, errb := verPkg.Lookup("__version__")
	if err != nil || errb != nil {
		t.Fatalf("Failed to lookup __version__ symbols: %v, %v", err, errb)
	}
	verA, oka := (*syma).(string)
	verB, okb := (*symb).(string)
	if !oka || !okb {
		t.Fatalf("__version__ missing or not string")
	}
	if verA != verB {
		t.Errorf("__version__ mismatch: main=%q _version=%q", verA, verB)
	}
	if verA == "0.0.0" {
		t.Error("__version__ must not be 0.0.0")
	}
}

func TestPublicImportVersionTypeAndLength(t *testing.T) {
	plg, err := plugin.Open("libsecure_package_template.so")
	if err != nil {
		t.Fatalf("Failed to open plugin: %v", err)
	}
	sym, err := plg.Lookup("__version__")
	if err != nil {
		t.Fatalf("Failed to lookup __version__: %v", err)
	}
	ver, ok := (*sym).(string)
	if !ok {
		t.Fatalf("__version__ is not a string")
	}
	if len(ver) < 5 {
		t.Errorf("version string is too short: %q", ver)
	}
}

func TestPublicReloadPackagePreservesVersionType(t *testing.T) {
	plg, err := plugin.Open("libsecure_package_template.so")
	if err != nil {
		t.Fatalf("Failed to reload plugin: %v", err)
	}
	sym, err := plg.Lookup("__version__")
	if err != nil {
		t.Fatalf("__version__ not found after reload: %v", err)
	}
	ver, ok := (*sym).(string)
	if !ok {
		t.Fatalf("__version__ after reload is not string")
	}
	if !strings.Contains(ver, ".") {
		t.Error("version string does not contain '.'")
	}
	noDot := strings.ReplaceAll(ver, ".", "")
	for _, ch := range noDot {
		if !(('0' <= ch && ch <= '9') || ('A' <= ch && ch <= 'Z') || ('a' <= ch && ch <= 'z')) {
			t.Errorf("version string %q contains non-alphanumeric character", ver)
			break
		}
	}
}