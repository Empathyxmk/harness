package original

import (
	"testing"
)

func TestFromHtml5lib(t *testing.T) {
	files := `
        foo:
            - __init__.py
            - a.py: |
                from bar import py
        bar:
            - __init__.py
            - py.py: |
                barpy = 42
    `
	got := simpleDeps("foo", "--show-deps", "-LINFO", "-vv")
	want := map[string]struct{}{
		"bar -> foo.a":      {},
		"bar.py -> foo.a":   {},
	}
	for k := range want {
		if _, ok := got[k]; !ok {
			t.Errorf("Expected key '%v' in deps, got %v", k, got)
		}
	}
	if len(got) != len(want) {
		t.Errorf("Expected %d deps, got %d", len(want), len(got))
	}
}

func TestMultidot(t *testing.T) {
	files := `
        foo.bar.py: |
            from math import pi
    `
	got := simpleDeps("foo.bar.py", "--show-deps", "--pylib", "-LINFO", "-vv")
	want := map[string]struct{}{
		"math -> foo.bar.py": {},
	}
	for k := range want {
		if _, ok := got[k]; !ok {
			t.Errorf("Expected key '%v' in deps, got %v", k, got)
		}
	}
	if len(got) != len(want) {
		t.Errorf("Expected %d deps, got %d", len(want), len(got))
	}
}