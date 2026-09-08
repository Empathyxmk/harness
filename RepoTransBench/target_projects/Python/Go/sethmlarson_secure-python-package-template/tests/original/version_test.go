package original

import (
	"plugin"
	"testing"
	"reflect"
)

func TestVersionModuleImportable(t *testing.T) {
	// Simulate importing "_version" as a plugin and check version value
	plg, err := plugin.Open("libsecure_package_template_version.so")
	if err != nil {
		t.Fatalf("Failed to open _version plugin: %v", err)
	}
	sym, err := plg.Lookup("__version__")
	if err != nil {
		t.Fatalf("Failed to lookup __version__ in _version plugin: %v", err)
	}
	version, ok := (*sym).(string)
	if !ok {
		t.Fatalf("__version__ in _version is not a string")
	}
	if version != "0.7.1" {
		t.Errorf("__version__ in _version is %q, want %q", version, "0.7.1")
	}
}

func TestVersionAttributeConsistency(t *testing.T) {
	mainPkg, err := plugin.Open("libsecure_package_template.so")
	if err != nil {
		t.Fatalf("Failed to open package plugin: %v", err)
	}
	versionMod, err := plugin.Open("libsecure_package_template_version.so")
	if err != nil {
		t.Fatalf("Failed to open _version plugin: %v", err)
	}
	syma, err := mainPkg.Lookup("__version__")
	if err != nil {
		t.Fatalf("Failed to lookup __version__ in package: %v", err)
	}
	symb, err := versionMod.Lookup("__version__")
	if err != nil {
		t.Fatalf("Failed to lookup __version__ in _version: %v", err)
	}
	va, oka := (*syma).(string)
	vb, okb := (*symb).(string)
	if !oka || !okb {
		t.Fatalf("__version__ missing or not string in one or both places")
	}
	if va != vb {
		t.Errorf("__version__ differs: main=%q, _version=%q", va, vb)
	}
}

func TestImportVersionStr(t *testing.T) {
	plg, err := plugin.Open("libsecure_package_template.so")
	if err != nil {
		t.Fatalf("Failed to open plugin: %v", err)
	}
	sym, err := plg.Lookup("__version__")
	if err != nil {
		t.Fatalf("Failed to lookup __version__: %v", err)
	}
	val, ok := (*sym).(string)
	if !ok {
		t.Fatalf("__version__ is not a string")
	}
	if len(val) == 0 {
		t.Errorf("__version__ string is empty")
	}
}

func TestReloadPackagePreservesVersion(t *testing.T) {
	plg, err := plugin.Open("libsecure_package_template.so")
	if err != nil {
		t.Fatalf("Failed to reload plugin: %v", err)
	}
	sym, err := plg.Lookup("__version__")
	if err != nil {
		t.Fatalf("Failed to lookup __version__ after reload: %v", err)
	}
	if reflect.TypeOf(*sym).Kind() != reflect.String {
		t.Errorf("__version__ missing or not string after reload")
	}
}