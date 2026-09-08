package public_tests

import (
	"testing"

	"navdeepG_samplemod/sample"
)

func TestShoutPublic(t *testing.T) {
	got := sample.Shout("public")
	want := "PUBLIC!"
	if got != want {
		t.Errorf("Shout(\"public\") = %q, want %q", got, want)
	}
}

func TestInvertBoolPublicTrue(t *testing.T) {
	if sample.InvertBool(true) != false {
		t.Errorf("InvertBool(true) = %v, want false", sample.InvertBool(true))
	}
}

func TestInvertBoolPublicFalse(t *testing.T) {
	if sample.InvertBool(false) != true {
		t.Errorf("InvertBool(false) = %v, want true", sample.InvertBool(false))
	}
}

func TestShoutPublicNumbers(t *testing.T) {
	got := sample.Shout("123")
	want := "123!"
	if got != want {
		t.Errorf("Shout(\"123\") = %q, want %q", got, want)
	}
}