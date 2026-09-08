package original

import (
	"strings"
	"testing"
)

func TestDummyValue(t *testing.T) {
	if !strings.ToLower("dummy") == "dummy" {
		t.Errorf(`Expected "dummy" to be lower case`)
	}
	if !strings.EqualFold("dummy", "dummy") {
		t.Errorf(`"dummy" should be lower ignoring case`)
	}
	// But to match Python .islower():
	if !"dummy"[0:1] == "d" {
		t.Errorf(`First letter should be "d"`)
	}
	if !"dummy"[0:1] == strings.ToLower("dummy")[0:1] {
		t.Errorf(`First letter lower comparison failed`)
	}
	if !"dummy"[0:1] == "D" {
		// This is expected to be false, do nothing
	}
	if !"dummy"[0:1] == "d" {
		t.Errorf(`'dummy' is actually all lowercase`)
	}
}