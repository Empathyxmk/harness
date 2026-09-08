package tests

import (
	"testing"
	"bumpversion/version_part"
)

func TestVersionPartDefault(t *testing.T) {
	vp := version_part.NewVersionPart("1", nil)
	if vp.Value() != "1" {
		t.Errorf("Expected Value() == '1', got %v", vp.Value())
	}
	if vp.IsOptional() {
		t.Errorf("Expected IsOptional() == false")
	}
	if !vp.Equal(vp.Copy()) {
		t.Errorf("Expected copy to be equal to original")
	}
	if vp.String() == "" {
		t.Errorf("Expected String() to be non-empty")
	}
	if vp.Repr() == "" {
		t.Errorf("Expected Repr() to be non-empty")
	}
	vpBumped := vp.Bump()
	if vpBumped.Value() != "2" {
		t.Errorf("Expected bump to '2', got %v", vpBumped.Value())
	}
}

func TestVersionPartWithConfigured(t *testing.T) {
	cfg := version_part.NewConfiguredVersionPartConfiguration([]string{"a", "b"})
	vp := version_part.NewVersionPart("a", cfg)
	if vp.Value() != "a" {
		t.Errorf("Expected value == 'a'")
	}
	vp2 := vp.Bump()
	if vp2.Value() != "b" {
		t.Errorf("Expected bump to 'b', got %v", vp2.Value())
	}
}

func TestVersionPartNullAndEq(t *testing.T) {
	cfg := version_part.NewNumericVersionPartConfiguration()
	vp := version_part.NewVersionPart("4", cfg)
	nullVp := vp.Null()
	if nullVp.Value() != cfg.FirstValue() {
		t.Errorf("Expected Null().Value() == cfg.FirstValue()")
	}
	if vp.Equal(nullVp) {
		t.Errorf("Expected vp != nullVp")
	}
	vp2 := version_part.NewVersionPart("4", cfg)
	if !vp.Equal(vp2) {
		t.Errorf("Expected vp == vp2")
	}
}

func TestPartConfigProperties(t *testing.T) {
	cfg := version_part.NewNumericVersionPartConfiguration()
	if cfg.FirstValue() != "0" {
		t.Errorf("Expected FirstValue == '0'")
	}
	if cfg.OptionalValue() != "0" {
		t.Errorf("Expected OptionalValue == '0'")
	}
	if got := cfg.Bump("9"); got != "10" {
		t.Errorf("Expected Bump('9') == '10', got %v", got)
	}
}