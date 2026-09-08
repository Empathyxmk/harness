package public_tests

import (
	"testing"
	"bumpversion/version_part"
)

func TestPublicVersionPartValueSetting(t *testing.T) {
	vp := version_part.NewVersionPartFromInterface("7", nil, nil)
	if vp.String() != "7" {
		t.Errorf("Expected String() == '7', got '%v'", vp.String())
	}
}

func TestPublicVersionPartCompareDifferentValues(t *testing.T) {
	vp1 := version_part.NewVersionPartFromInterface("3", nil, nil)
	vp2 := version_part.NewVersionPartFromInterface("10", nil, nil)
	if vp1.Equal(vp2) {
		t.Errorf("Expected vp1 != vp2")
	}
}

func TestPublicVersionPartEqualityWithSameValue(t *testing.T) {
	vp1 := version_part.NewVersionPartFromInterface("hello", nil, nil)
	vp2 := version_part.NewVersionPartFromInterface("hello", nil, nil)
	if !vp1.Equal(vp2) {
		t.Errorf("Expected vp1 == vp2")
	}
}

func TestPublicVersionPartRepr(t *testing.T) {
	vp := version_part.NewVersionPartFromInterface("2024", nil, nil)
	if !contains(vp.Repr(), "2024") {
		t.Errorf("Expected Repr() to contain '2024', got %v", vp.Repr())
	}
}

func TestPublicVersionPartStrCast(t *testing.T) {
	vp := version_part.NewVersionPartFromInterface(543, nil, nil)
	if vp.String() != "543" {
		t.Errorf("Expected String() == '543', got '%v'", vp.String())
	}
}

func TestPublicVersionPartIntCast(t *testing.T) {
	vp := version_part.NewVersionPartFromInterface("8", nil, nil)
	val, err := vp.ToInt()
	if err != nil || val != 8 {
		t.Errorf("Expected int(vp) == 8, got %v (err: %v)", val, err)
	}
}

func TestPublicVersionPartIntCastNonNumeric(t *testing.T) {
	vp := version_part.NewVersionPartFromInterface("xyz", nil, nil)
	_, err := vp.ToInt()
	if err == nil {
		t.Errorf("Expected error when casting non-numeric value to int")
	}
}

func contains(s, sub string) bool {
	return len(sub) == 0 || (len(s) >= len(sub) && string([]byte(s)[0:len(sub)]) == sub) || (len(s) >= len(sub) && string([]byte(s)[len(s)-len(sub):]) == sub)
}