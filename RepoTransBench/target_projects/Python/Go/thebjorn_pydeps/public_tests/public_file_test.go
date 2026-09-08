package public_tests

import (
	"testing"
)

func createFiles(filesYaml string, cleanup bool, t *testing.T, testFunc func(workdir string)) {
	workdir := t.TempDir()
	testFunc(workdir)
}

func simpleDeps(target string, args ...string) map[string]struct{} {
	return make(map[string]struct{})
}

func TestFilePublic(t *testing.T) {
	files := `
        b.py: |
            import math
    `
	createFiles(files, true, t, func(workdir string) {
		actual := simpleDeps("b.py")
		if len(actual) != 0 {
			t.Errorf("Expected empty deps for b.py, got %v", actual)
		}
	})
}

func TestFileInSubDirectoryPublic(t *testing.T) {
	files := `
        baz:
            - d:
                - e.py: |
                    import f
                - f.py: ""
    `
	createFiles(files, true, t, func(workdir string) {
		found := false
		for k := range simpleDeps("baz/d/e.py") {
			if k == "f -> e.py" {
				found = true
			}
		}
		if !found {
			t.Errorf("Expected 'f -> e.py' in deps for baz/d/e.py")
		}
	})
}

func TestFileInDirectoryPublic(t *testing.T) {
	files := `
            - x:
                - y.py: |
                    import z
                - z.py: ""
    `
	createFiles(files, true, t, func(workdir string) {
		found := false
		for k := range simpleDeps("x/y.py") {
			if k == "z -> y.py" {
				found = true
			}
		}
		if !found {
			t.Errorf("Expected 'z -> y.py' in deps for x/y.py")
		}
	})
}

func TestFilePylibPublic(t *testing.T) {
	files := `
        q.py: |
            import sys
    `
	createFiles(files, true, t, func(workdir string) {
		found := false
		for k := range simpleDeps("q.py", "--pylib") {
			if k == "sys -> q.py" {
				found = true
			}
		}
		if !found {
			t.Errorf("Expected 'sys -> q.py' in deps with --pylib")
		}
	})
}

func TestFilePyliballPublic(t *testing.T) {
	files := `
        q.py: |
            import sys
    `
	createFiles(files, true, t, func(workdir string) {
		found := false
		for k := range simpleDeps("q.py", "--pylib", "--pylib-all") {
			if k == "sys -> q.py" {
				found = true
			}
		}
		if !found {
			t.Errorf("Expected 'sys -> q.py' in deps with --pylib --pylib-all")
		}
	})
}