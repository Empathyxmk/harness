package public_tests

import (
	"testing"
	"bumpversion/version_part"
)

func TestPublicVersionPartHasValue(t *testing.T) {
	vp := version_part.NewVersionPartFromInterface("nonempty", nil, nil)
	if !vp.HasValue() {
		t.Errorf("Expected HasValue() true")
	}
}

func TestPublicVersionPartNotHasValueEmptyString(t *testing.T) {
	vp := version_part.NewVersionPartFromInterface("", nil, nil)
	if vp.HasValue() {
		t.Errorf("Expected HasValue() false")
	}
}

func TestPublicVersionPartIntCastZero(t *testing.T) {
	vp := version_part.NewVersionPartFromInterface("0", nil, nil)
	val, err := vp.ToInt()
	if err != nil || val != 0 {
		t.Errorf("Expected int(vp)==0, got %v (err: %v)", val, err)
	}
}

func TestPublicVersionPartIgnoreValue(t *testing.T) {
	vp := version_part.NewVersionPartFromInterface("ignored", nil, nil)
	if vp.Value() != "ignored" {
		t.Errorf("Expected value == 'ignored', got '%v'", vp.Value())
	}
}

func TestPublicVersionPartReprContainsClass(t *testing.T) {
	vp := version_part.NewVersionPartFromInterface("classy", nil, nil)
	if !contains(vp.Repr(), "VersionPart") {
		t.Errorf("Expected Repr() to contain 'VersionPart'")
	}
}

func contains(s, sub string) bool {
	return len(sub) == 0 || (len(s) >= len(sub) && string([]byte(s)[0:len(sub)]) == sub) || (len(s) >= len(sub) && string([]byte(s)[len(s)-len(sub):]) == sub)
}