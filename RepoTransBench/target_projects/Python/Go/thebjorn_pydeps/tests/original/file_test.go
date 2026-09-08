package original

import (
	"os"
	"testing"
)

// NOTE: In Go, the "filemaker" and "simpledeps" helpers would need to be re-implemented for accurate test functionality.
// Here, we provide stubs for these helpers to focus on preserving test logic structure.

func createFiles(filesYaml string, cleanup bool, t *testing.T, testFunc func(workdir string)) {
	// Stub. Should create temporary files based on the YAML definition.
	// Use t.TempDir() in real implementation.
	workdir := t.TempDir()
	testFunc(workdir)
}

func simpleDeps(target string, args ...string) map[string]struct{} {
	// Stub. Should analyze dependencies.
	return make(map[string]struct{})
}

func TestFile(t *testing.T) {
	files := `
        a.py: |
            import collections
    `
	createFiles(files, true, t, func(workdir string) {
		actual := simpleDeps("a.py")
		if len(actual) != 0 {
			t.Errorf("Expected empty deps for a.py, got %v", actual)
		}
	})
}

func TestFileInSubDirectory(t *testing.T) {
	files := `
        foo:
            - a:
                - b.py: |
                    import c
                - c.py: ""
    `
	createFiles(files, true, t, func(workdir string) {
		found := false
		for k := range simpleDeps("foo/a/b.py") {
			if k == "c -> b.py" {
				found = true
			}
		}
		if !found {
			t.Errorf("Expected 'c -> b.py' in deps for foo/a/b.py")
		}
	})
}

func TestFileInDirectory(t *testing.T) {
	files := `
            - a:
                - b.py: |
                    import c
                - c.py: ""
    `
	createFiles(files, true, t, func(workdir string) {
		found := false
		for k := range simpleDeps("a/b.py") {
			if k == "c -> b.py" {
				found = true
			}
		}
		if !found {
			t.Errorf("Expected 'c -> b.py' in deps for a/b.py")
		}
	})
}

func TestFilePylib(t *testing.T) {
	files := `
        a.py: |
            import collections
    `
	createFiles(files, true, t, func(workdir string) {
		found := false
		for k := range simpleDeps("a.py", "--pylib") {
			if k == "collections -> a.py" {
				found = true
			}
		}
		if !found {
			t.Errorf("Expected 'collections -> a.py' in deps with --pylib")
		}
	})
}

func TestFilePylibAll(t *testing.T) {
	files := `
        a.py: |
            import collections
    `
	createFiles(files, true, t, func(workdir string) {
		found := false
		for k := range simpleDeps("a.py", "--pylib", "--pylib-all") {
			if k == "collections -> a.py" {
				found = true
			}
		}
		if !found {
			t.Errorf("Expected 'collections -> a.py' in deps with --pylib --pylib-all")
		}
	})
}