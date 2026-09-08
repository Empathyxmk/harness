package public_tests

import (
	"testing"
)

func TestFromCustomlibPublic(t *testing.T) {
	files := `
        zoo:
            - __init__.py
            - tiger.py: |
                from custom import py
        custom:
            - __init__.py
            - py.py: |
                somevar = 100
    `
	got := simpleDeps("zoo", "--show-deps", "-LINFO", "-vv")
	want := map[string]struct{}{
		"custom -> zoo.tiger":   {},
		"custom.py -> zoo.tiger": {},
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

func TestMultidotPublic(t *testing.T) {
	files := `
        alpha.beta.py: |
            from random import randint
    `
	got := simpleDeps("alpha.beta.py", "--show-deps", "--pylib", "-LINFO", "-vv")
	want := map[string]struct{}{
		"random -> alpha.beta.py": {},
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