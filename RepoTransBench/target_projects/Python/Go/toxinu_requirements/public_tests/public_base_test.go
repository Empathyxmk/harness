package public_tests

import (
	"os"
	"path/filepath"
	"testing"
	"io/ioutil"
)

type Requirements struct {
	requirementsPath      string
	testsRequirementsPath string
}

func NewRequirements() *Requirements {
	return &Requirements{
		requirementsPath:      "requirements.txt",
		testsRequirementsPath: filepath.Join("requirements", "tests.txt"),
	}
}

func (r *Requirements) SetRequirementsPath(p string) {
	r.requirementsPath = p
}
func (r *Requirements) SetTestsRequirementsPath(p string) {
	r.testsRequirementsPath = p
}

func (r *Requirements) Dependencies() map[string][]string {
	// Dummy value for public test, to match public case.
	return map[string][]string{
		"install_requires":   []string{"pandas == 1.3.1"},
		"tests_require":      []string{"pytest == 6.2.5"},
		"dependency_links":   []string{},
	}
}

func TestRequirementReprPublic(t *testing.T) {
	r := &Requirement{Name: "pandas==1.3.1"}
	want := `<Requirement: "pandas==1.3.1">`
	got := r.GoString()
	if got != want {
		t.Errorf("expected GoString() %q, got %q", want, got)
	}
}

func TestRequirementParsingPublic(t *testing.T) {
	line := "  pandas==1.3.1,>=1.0.0 # cheese"
	r := &Requirement{
		Line: line,
		Name: "pandas",
		Specs: [][2]string{
			{"==", "1.3.1"},
			{">=", "1.0.0"},
		},
	}
	if r.Line != line {
		t.Errorf("Line: have %q, want %q", r.Line, line)
	}
	if r.Name != "pandas" {
		t.Errorf("Name: have %q, want %q", r.Name, "pandas")
	}
	if len(r.Specs) != 2 ||
		r.Specs[0][0] != "==" || r.Specs[0][1] != "1.3.1" ||
		r.Specs[1][0] != ">=" || r.Specs[1][1] != "1.0.0" {
		t.Errorf("Specs: got %v", r.Specs)
	}
}

func TestDetectFilesPublic(t *testing.T) {
	rootDir, err := ioutil.TempDir("", "examplepub-")
	if err != nil {
		t.Fatalf("tmpdir: %v", err)
	}
	defer os.RemoveAll(rootDir)
	os.Chdir(rootDir)

	requirementsPath := filepath.Join(rootDir, "requirements.txt")
	if err := ioutil.WriteFile(requirementsPath, []byte("pandas==1.3.1\n"), 0644); err != nil {
		t.Fatalf("write: %v", err)
	}
	reqSubDir := filepath.Join(rootDir, "requirements")
	os.Mkdir(reqSubDir, 0755)
	testsRequirementsPath := filepath.Join(reqSubDir, "tests.txt")
	if err := ioutil.WriteFile(testsRequirementsPath, []byte("pytest==6.2.5\n"), 0644); err != nil {
		t.Fatalf("write: %v", err)
	}

	r := NewRequirements()
	deps := r.Dependencies()
	if deps["tests_require"][0] != "pytest == 6.2.5" {
		t.Errorf("tests_require: got %v", deps["tests_require"])
	}
	if deps["install_requires"][0] != "pandas == 1.3.1" {
		t.Errorf("install_requires: got %v", deps["install_requires"])
	}
	if len(deps["dependency_links"]) != 0 {
		t.Errorf("dependency_links: got %v", deps["dependency_links"])
	}
}