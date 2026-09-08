// tests/test_init_test.go
package tex2nix

import (
	"os"
	"path/filepath"
	"reflect"
	"strings"
	"testing"
)

// test_get_packages_basic: r"\usepackage{foo,bar}"
func TestGetPackagesBasic(t *testing.T) {
	line := `\usepackage{foo,bar}`
	pkgs := GetPackages(line)
	if _, ok := pkgs["foo"]; !ok {
		t.Errorf("expected 'foo' in pkgs")
	}
	if _, ok := pkgs["bar"]; !ok {
		t.Errorf("expected 'bar' in pkgs")
	}
}

func TestGetPackagesRequirepackage(t *testing.T) {
	line := `\RequirePackage{baz}`
	pkgs := GetPackages(line)
	want := map[string]struct{}{"baz": {}}
	if !reflect.DeepEqual(pkgs, want) {
		t.Errorf("Expected %v, got %v", want, pkgs)
	}
}

func TestGetPackagesNoMatch(t *testing.T) {
	line := `not a package line`
	pkgs := GetPackages(line)
	if len(pkgs) != 0 {
		t.Errorf("Expected empty set, got %v", pkgs)
	}
}

func TestGetPackagesWhitespace(t *testing.T) {
	line := `\usepackage{   foo ,   bar  }`
	pkgs := GetPackages(line)
	want := map[string]struct{}{"foo": {}, "bar": {}}
	if !reflect.DeepEqual(pkgs, want) {
		t.Errorf("Expected %v, got %v", want, pkgs)
	}
}

func TestGetPackagesEmptyBraces(t *testing.T) {
	line := `\usepackage{}`
	pkgs := GetPackages(line)
	if len(pkgs) != 0 {
		t.Errorf("Expected empty set: got %v", pkgs)
	}
}

func TestWriteTexEnv(t *testing.T) {
	tmpdir := t.TempDir()
	pkgs := map[string]struct{}{"foo": {}, "bar": {}}
	name := WriteTexEnv(tmpdir, pkgs)
	if _, err := os.Stat(name); err != nil {
		t.Fatalf("expected file to exist: %s", name)
	}
	content, err := os.ReadFile(name)
	if err != nil {
		t.Fatalf("ReadFile failed: %v", err)
	}
	s := string(content)
	if !strings.Contains(s, "foo") || !strings.Contains(s, "bar") {
		t.Errorf("expected content to mention foo and bar; got %q", s)
	}
}

func TestCollectDepsCalls(t *testing.T) {
	called := 0
	orig := _CollectDeps
	defer func() { _CollectDeps = orig }()
	_CollectDeps = func(workingSet, done, allPkgs map[string]struct{}) {
		for len(workingSet) > 0 {
			for k := range workingSet {
				done[k] = struct{}{}
				delete(workingSet, k)
				called++
			}
		}
	}
	pkgs := map[string]struct{}{"foo": {}, "bar": {}}
	allpkgs := map[string]struct{}{"foo": {}, "bar": {}, "baz": {}}
	result := CollectDeps(pkgs, allpkgs)
	if _, ok := result["foo"]; !ok || _, ok2 := result["bar"]; !ok2 {
		t.Errorf("expected 'foo' and 'bar' in result: %v", result)
	}
	if called != 2 {
		t.Errorf("expected _CollectDeps called 2 times, got %d", called)
	}
}

func TestExtractDependenciesAndCollect(t *testing.T) {
	origGetNix := GetNixPackages
	origCollect := CollectDeps
	defer func() {
		GetNixPackages = origGetNix
		CollectDeps = origCollect
	}()
	GetNixPackages = func() map[string]struct{} { return map[string]struct{}{"a": {}, "b": {}} }
	CollectDeps = func(x, y map[string]struct{}) map[string]struct{} {
		res := make(map[string]struct{})
		for k := range x {
			res[k] = struct{}{}
		}
		return res
	}
	lines := []string{`\usepackage{a,b}`, `\usepackage{c}`}
	result := ExtractDependencies(lines)
	want := map[string]struct{}{"a": {}, "b": {}}
	if !reflect.DeepEqual(result, want) {
		t.Errorf("Expected %v, got %v", want, result)
	}
}

func TestMainAndFileinput(t *testing.T) {
	origGetNix := GetNixPackages
	origCollect := CollectDeps
	origMain := Main
	origWrite := WriteTexEnv
	defer func() {
		GetNixPackages = origGetNix
		CollectDeps = origCollect
		Main = origMain
		WriteTexEnv = origWrite
	}()
	GetNixPackages = func() map[string]struct{} { return map[string]struct{}{"ji": {}, "li": {}} }
	CollectDeps = func(x, y map[string]struct{}) map[string]struct{} {
		res := make(map[string]struct{})
		for k := range x {
			res[k] = struct{}{}
		}
		return res
	}
	// Replace WriteTexEnv to capture output
	outputs := struct {
		dir  string
		pkgs map[string]struct{}
	}{}
	WriteTexEnv = func(dir string, pkgs map[string]struct{}) string {
		outputs.dir = dir
		outputs.pkgs = pkgs
		f := filepath.Join(dir, "tex-env.nix")
		os.WriteFile(f, []byte("dummy"), 0600)
		return f
	}
	// Simulate input
	tmpdir := t.TempDir()
	Main = func() {
		dir := tmpdir
		lines := []string{`\usepackage{ji,ki}`, `\RequirePackage{li}`}
		var pkgs = make(map[string]struct{})
		for _, l := range lines {
			for pkg := range GetPackages(l) {
				pkgs[pkg] = struct{}{}
			}
		}
		allpkgs := GetNixPackages()
		selected := CollectDeps(pkgs, allpkgs)
		WriteTexEnv(dir, selected)
	}
	Main()
	if outputs.dir != tmpdir {
		t.Errorf("Expected dir=%q, got %q", tmpdir, outputs.dir)
	}
	wantPkgs := map[string]struct{}{"ji": {}, "li": {}}
	if !reflect.DeepEqual(outputs.pkgs, wantPkgs) {
		t.Errorf("Expected pkgs=%v got %v", wantPkgs, outputs.pkgs)
	}
}

func TestCollectDepsReal(t *testing.T) {
	tmpdir := t.TempDir()
	fooDir := filepath.Join(tmpdir, "foo", "tex")
	os.MkdirAll(fooDir, 0755)
	texFile := filepath.Join(fooDir, "abc.sty")
	os.WriteFile(texFile, []byte(`\usepackage{morepkg}\n`), 0644)
	origGetPkgs := GetPackages
	defer func() { GetPackages = origGetPkgs }()
	GetPackages = func(l string) map[string]struct{} {
		if strings.Contains(l, "morepkg") {
			return map[string]struct{}{"morepkg": {}}
		}
		return map[string]struct{}{}
	}
	workingSet := map[string]struct{}{"bar": {}}
	done := make(map[string]struct{})
	allPackages := map[string]struct{}{"morepkg": {}, "bar": {}}
	_CollectDeps(workingSet, done, allPackages)
	if _, ok := done["bar"]; !ok {
		t.Errorf("Expected 'bar' in done")
	}
}

func TestGetNixPackagesSuccess(t *testing.T) {
	old := GetNixPackages
	GetNixPackages = func() map[string]struct{} {
		return map[string]struct{}{"foo": {}, "bar": {}, "baz": {}}
	}
	defer func() { GetNixPackages = old }()
	got := GetNixPackages()
	want := map[string]struct{}{"foo": {}, "bar": {}, "baz": {}}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("Expected %v, got %v", want, got)
	}
}

func TestWriteTexEnvEmpty(t *testing.T) {
	tmpdir := t.TempDir()
	pkgs := make(map[string]struct{})
	name := WriteTexEnv(tmpdir, pkgs)
	if _, err := os.Stat(name); err != nil {
		t.Fatalf("expected file to exist")
	}
	content, err := os.ReadFile(name)
	if err != nil {
		t.Fatalf("ReadFile: %v", err)
	}
	if !strings.Contains(string(content), "scheme-small") {
		t.Errorf("expected scheme-small in content: %q", string(content))
	}
}