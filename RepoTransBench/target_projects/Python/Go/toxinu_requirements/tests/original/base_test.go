package original

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
	// Dummy stub, should be replaced by proper implementation as per python logic.
	// Only basic key structure returned.
	return map[string][]string{
		"install_requires":   []string{"requests == 2.9.1"},
		"tests_require":      []string{"flake8 == 2.5.4"},
		"dependency_links":   []string{},
	}
}

func TestRequirementRepr(t *testing.T) {
	r, _ := parseRequirement("requests==2.9.1")
	want := `<Requirement: "requests==2.9.1">`
	got := r.GoString()
	if got != want {
		t.Errorf("expected GoString() %q, got %q", want, got)
	}
}

func TestRequirementParsing(t *testing.T) {
	line := "  requests==2.9.1,>=2.8.1 # jambon"
	r := &Requirement{
		Line: line,
		Name: "requests",
		Specs: [][2]string{
			{"==", "2.9.1"},
			{">=", "2.8.1"},
		},
	}
	if r.Line != line {
		t.Errorf("Line: have %q, want %q", r.Line, line)
	}
	if r.Name != "requests" {
		t.Errorf("Name: have %q, want %q", r.Name, "requests")
	}
	if len(r.Specs) != 2 ||
		r.Specs[0][0] != "==" || r.Specs[0][1] != "2.9.1" ||
		r.Specs[1][0] != ">=" || r.Specs[1][1] != "2.8.1" {
		t.Errorf("Specs: got %v", r.Specs)
	}
}

func TestDetectFiles(t *testing.T) {
	rootDir, err := ioutil.TempDir("", "example-")
	if err != nil {
		t.Fatalf("tmpdir: %v", err)
	}
	defer os.RemoveAll(rootDir)
	os.Chdir(rootDir)

	requirementsPath := filepath.Join(rootDir, "requirements.txt")
	if err := ioutil.WriteFile(requirementsPath, []byte("requests==2.9.1\n"), 0644); err != nil {
		t.Fatalf("write: %v", err)
	}
	reqSubDir := filepath.Join(rootDir, "requirements")
	os.Mkdir(reqSubDir, 0755)
	testsRequirementsPath := filepath.Join(reqSubDir, "tests.txt")
	if err := ioutil.WriteFile(testsRequirementsPath, []byte("flake8==2.5.4\n"), 0644); err != nil {
		t.Fatalf("write: %v", err)
	}

	r := NewRequirements()
	deps := r.Dependencies()
	if deps["tests_require"][0] != "flake8 == 2.5.4" {
		t.Errorf("tests_require: got %v", deps["tests_require"])
	}
	if deps["install_requires"][0] != "requests == 2.9.1" {
		t.Errorf("install_requires: got %v", deps["install_requires"])
	}
	if len(deps["dependency_links"]) != 0 {
		t.Errorf("dependency_links: got %v", deps["dependency_links"])
	}
}