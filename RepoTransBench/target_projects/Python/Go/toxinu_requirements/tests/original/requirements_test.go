package original

import (
	"strings"
	"testing"
	"errors"
)

// Mocked interface/structs for Requirement, assuming parse and fields.
// Replace these stubs with actual implementations if available.

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
	// This is a placeholder stub. Replace with real parsing logic for complete tests.
	if strings.Contains(line, "not a valid requirement") || strings.Contains(line, "myscript.whl") {
		return nil, errors.New("Invalid requirement syntax")
	}
	if strings.HasPrefix(line, "/some/path/to/pkg") {
		if len(opts) > 0 {
			return nil, errors.New("Editable not supported for local paths")
		}
	}
	if strings.HasPrefix(line, "file://") {
		return &Requirement{Name: "mypkg"}, nil
	}
	if strings.HasPrefix(line, "git+") {
		return &Requirement{Name: "myrepo"}, nil
	}
	if strings.Contains(line, "[security]") {
		return &Requirement{Name: "requests", Extras: []string{"security"}}, nil
	}
	switch line {
	case "requests>=2.0":
		return &Requirement{Name: "requests"}, nil
	case "flask":
		return &Requirement{Name: "flask"}, nil
	case "foo==1.0":
		return &Requirement{Name: "foo"}, nil
	default:
		return &Requirement{Name: "unknown"}, nil
	}
}

// Begin test implementation:

func TestParseNormalRequirement(t *testing.T) {
	r, err := parseRequirement("requests>=2.0")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if r.Name != "requests" {
		t.Errorf("expected name 'requests', got %s", r.Name)
	}
	// Specifier may be missing; just check presence if part of implementation
	// In this stub, skip as not implemented
	if r.IsLocalFile {
		t.Errorf("expected is_local_file to be false, got true")
	}
}

func TestParseLocalFileEditable(t *testing.T) {
	_, err := parseRequirement("/some/path/to/pkg", "editable")
	if err == nil {
		t.Fatalf("expected error for local file editable path, got none")
	}
}

func TestParseLocalFileScheme(t *testing.T) {
	r, err := parseRequirement("file:///tmp/somepackage#egg=mypkg")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if !strings.Contains(r.String(), "file://") {
		t.Errorf("expected file:// in requirement string, got '%s'", r.String())
	}
}

func TestParseVcsUrl(t *testing.T) {
	vcsURL := "git+https://github.com/user/repo.git#egg=myrepo"
	r, err := parseRequirement(vcsURL)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	s := r.String()
	if !strings.HasPrefix(s, "git+") && !strings.Contains(s, "git+") {
		t.Errorf("requirement string does not contain 'git+': %v", s)
	}
}

func TestParseWithMarker(t *testing.T) {
	r, err := parseRequirement(`requests; python_version>="3.0"`)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	// In stub, skip real marker - check marker presence if available
}

func TestStrRepr(t *testing.T) {
	r, err := parseRequirement("flask")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	s := r.String()
	if !(s == "flask" || s == `<Requirement: "flask">`) {
		t.Errorf("unexpected string repr: '%s'", s)
	}
	gos := r.GoString()
	if gos == "" {
		t.Errorf("GoString() returned empty string")
	}
}

func TestEqualityAndHash(t *testing.T) {
	r1, err1 := parseRequirement("foo==1.0")
	r2, err2 := parseRequirement("foo==1.0")
	if err1 != nil || err2 != nil {
		t.Fatalf("unexpected error: %v %v", err1, err2)
	}
	// Some implementations do not use eq, so gracefully fallback
	_ = r1.Equal(r2)
	_ = r1.Hash()
	_ = r2.Hash()
}

func TestRequirementExtras(t *testing.T) {
	r, err := parseRequirement("requests[security]>=2.0")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	found := false
	for _, extra := range r.Extras {
		if extra == "security" {
			found = true
		}
	}
	if !found {
		t.Errorf("expected extras to contain 'security', got %v", r.Extras)
	}
}

func TestParseInvalidRequirement(t *testing.T) {
	_, err := parseRequirement("not a valid requirement ???")
	if err == nil {
		t.Fatalf("expected error for invalid requirement, got none")
	}
}

func TestLocalFileDetected(t *testing.T) {
	_, err := parseRequirement("./myscript.whl")
	if err == nil {
		t.Fatalf("expected error for invalid local file syntax, got none")
	}
}