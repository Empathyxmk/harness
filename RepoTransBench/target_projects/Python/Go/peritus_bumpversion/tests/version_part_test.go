package tests

import (
	"testing"
	"bumpversion/version_part"
)

func confvpc(t *testing.T, i int) version_part.VersionPartConfiguration {
	switch i {
	case 0:
		return version_part.NewNumericVersionPartConfiguration()
	case 1:
		return version_part.NewConfiguredVersionPartConfiguration([]string{"0", "1", "2"})
	case 2:
		return version_part.NewConfiguredVersionPartConfiguration([]string{"0", "3"})
	default:
		t.Fatalf("Index out of range for confvpc")
		return nil
	}
}

func TestVersionPartInit(t *testing.T) {
	for i := 0; i < 3; i++ {
		conf := confvpc(t, i)
		v := version_part.NewVersionPart(conf.FirstValue(), conf)
		if v.Value() != conf.FirstValue() {
			t.Errorf("Expected value == first_value, got %v", v.Value())
		}
	}
}

func TestVersionPartCopy(t *testing.T) {
	for i := 0; i < 3; i++ {
		conf := confvpc(t, i)
		vp := version_part.NewVersionPart(conf.FirstValue(), conf)
		copy := vp.Copy()
		if vp.Value() != copy.Value() {
			t.Errorf("Copy should have the same value as original")
		}
		if &vp == &copy {
			t.Errorf("Copy should be a different object")
		}
	}
}

func TestVersionPartBump(t *testing.T) {
	for i := 0; i < 3; i++ {
		conf := confvpc(t, i)
		vp := version_part.NewVersionPart(conf.FirstValue(), conf)
		vc := vp.Bump()
		expected := conf.Bump(conf.FirstValue())
		if vc.Value() != expected {
			t.Errorf("Expected bump value == %v, got %v", expected, vc.Value())
		}
	}
}

func TestVersionPartCheckOptionalFalse(t *testing.T) {
	for i := 0; i < 3; i++ {
		conf := confvpc(t, i)
		vp := version_part.NewVersionPart(conf.FirstValue(), conf)
		if vp.Bump().IsOptional() {
			t.Errorf("Expected bump().IsOptional() == false")
		}
	}
}

func TestVersionPartCheckOptionalTrue(t *testing.T) {
	for i := 0; i < 3; i++ {
		conf := confvpc(t, i)
		vp := version_part.NewVersionPart(conf.FirstValue(), conf)
		if !vp.IsOptional() {
			t.Errorf("Expected IsOptional() == true")
		}
	}
}

func TestVersionPartFormat(t *testing.T) {
	for i := 0; i < 3; i++ {
		conf := confvpc(t, i)
		vp := version_part.NewVersionPart(conf.FirstValue(), conf)
		formatted := vp.String()
		if formatted != conf.FirstValue() {
			t.Errorf("Expected String() == %v, got %v", conf.FirstValue(), formatted)
		}
	}
}

func TestVersionPartEquality(t *testing.T) {
	for i := 0; i < 3; i++ {
		conf := confvpc(t, i)
		a := version_part.NewVersionPart(conf.FirstValue(), conf)
		b := version_part.NewVersionPart(conf.FirstValue(), conf)
		if !a.Equal(b) {
			t.Errorf("Expected VersionPart equality")
		}
	}
}

func TestVersionPartNull(t *testing.T) {
	for i := 0; i < 3; i++ {
		conf := confvpc(t, i)
		a := version_part.NewVersionPart(conf.FirstValue(), conf)
		nullV := a.Null()
		if !nullV.Equal(a) {
			t.Errorf("Expected Null() == original VersionPart")
		}
	}
}