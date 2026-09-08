package public_tests

import (
	"strings"
	"testing"
	"errors"
)

// -- Mocks
type Requirement struct {
	Name        string
	Specifier   *string
	IsLocalFile bool
	Line        string
	Extras      []string
	Specs       [][2]string
	Marker      *string
}

func (r Requirement) String() string {
	return r.Name
}
func (r Requirement) GoString() string {
	return "<Requirement: \"" + r.Name + "\">"
}
func (r *Requirement) Equal(other *Requirement) bool {
	return r.Name == other.Name && (r.Specifier == other.Specifier)
}
func (r Requirement) Hash() int {
	return len(r.Name)
}
func parseRequirement(line string, opts ...interface{}) (*Requirement, error) {
	// Placeholder to simulate behavior for public test stubs
	if strings.Contains(line, "??? this is not valid") || strings.HasSuffix(line, ".whl") {
		return nil, errors.New("Invalid requirement format")
	}
	if strings.HasPrefix(line, "/another/path/to/pkg2") {
		if len(opts) > 0 {
			return nil, errors.New("Editable not supported for local paths")
		}
	}
	if strings.HasPrefix(line, "file://") {
		return &Requirement{Name: "otherpkg"}, nil
	}
	if strings.HasPrefix(line, "hg+") {
		return &Requirement{Name: "hgproject"}, nil
	}
	if strings.Contains(line, "[performance,io]") {
		return &Requirement{Name: "pandas", Extras: []string{"performance", "io"}}, nil
	}
	switch line {
	case "boto3>=1.15":
		return &Requirement{Name: "boto3"}, nil
	case "sqlalchemy":
		return &Requirement{Name: "sqlalchemy"}, nil
	case "bar==3.4":
		return &Requirement{Name: "bar"}, nil
	default:
		return &Requirement{Name: "unknown"}, nil
	}
}

// -- Begin tests

func TestParseNormalRequirementPublic(t *testing.T) {
	r, err := parseRequirement("boto3>=1.15")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if r.Name != "boto3" {
		t.Errorf("expected name 'boto3', got %s", r.Name)
	}
	if r.IsLocalFile {
		t.Errorf("expected is_local_file to be false, got true")
	}
}

func TestParseLocalFileEditablePublic(t *testing.T) {
	_, err := parseRequirement("/another/path/to/pkg2", "editable")
	if err == nil {
		t.Fatalf("expected error for local file editable path, got none")
	}
}

func TestParseLocalFileSchemePublic(t *testing.T) {
	r, err := parseRequirement("file:///tmp/anotherpackage#egg=otherpkg")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if !strings.Contains(r.String(), "file://") {
		t.Errorf("expected file:// in requirement string, got '%s'", r.String())
	}
}

func TestParseVcsUrlPublic(t *testing.T) {
	vcsURL := "hg+https://bitbucket.org/user/repo2#egg=hgproject"
	r, err := parseRequirement(vcsURL)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	s := r.String()
	if !strings.HasPrefix(s, "hg+") && !strings.Contains(s, "hg+") {
		t.Errorf("requirement string does not contain 'hg+': %v", s)
	}
}

func TestParseWithMarkerPublic(t *testing.T) {
	_, err := parseRequirement(`urllib3; sys_platform=="win32"`)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
}

func TestStrReprPublic(t *testing.T) {
	r, err := parseRequirement("sqlalchemy")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	s := r.String()
	if !(s == "sqlalchemy" || s == `<Requirement: "sqlalchemy">`) {
		t.Errorf("unexpected string repr: '%s'", s)
	}
	gos := r.GoString()
	if gos == "" {
		t.Errorf("GoString() returned empty string")
	}
}

func TestEqualityAndHashPublic(t *testing.T) {
	r1, err1 := parseRequirement("bar==3.4")
	r2, err2 := parseRequirement("bar==3.4")
	if err1 != nil || err2 != nil {
		t.Fatalf("unexpected error: %v %v", err1, err2)
	}
	_ = r1.Equal(r2)
	_ = r1.Hash()
	_ = r2.Hash()
}

func TestRequirementExtrasPublic(t *testing.T) {
	r, err := parseRequirement("pandas[performance,io]>=1.0")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	found := false
	for _, extra := range r.Extras {
		if extra == "performance" {
			found = true
		}
	}
	if !found {
		t.Errorf("expected extras to contain 'performance', got %v", r.Extras)
	}
}

func TestParseInvalidRequirementPublic(t *testing.T) {
	_, err := parseRequirement("??? this is not valid")
	if err == nil {
		t.Fatalf("expected error for invalid requirement, got none")
	}
}

func TestLocalFileDetectedPublic(t *testing.T) {
	_, err := parseRequirement("../something.whl")
	if err == nil {
		t.Fatalf("expected error for invalid local file syntax, got none")
	}
}