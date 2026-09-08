package original

import (
	"strings"
	"testing"
)

func TestHmacHashFunctionValueOf(t *testing.T) {
	if HmacHashFunction("HmacSHA1") != HmacSHA1 {
		t.Error("HmacSHA1 value mismatch")
	}
	if HmacHashFunction("HmacSHA256") != HmacSHA256 {
		t.Error("HmacSHA256 value mismatch")
	}
	if HmacHashFunction("HmacSHA512") != HmacSHA512 {
		t.Error("HmacSHA512 value mismatch")
	}
}

func TestHmacHashFunctionValuesArePresent(t *testing.T) {
	var allNames []string
	for _, fn := range []HmacHashFunction{HmacSHA1, HmacSHA256, HmacSHA512} {
		allNames = append(allNames, string(fn))
	}
	all := strings.Join(allNames, "")
	if !strings.Contains(all, "HmacSHA1") {
		t.Error("Should contain HmacSHA1")
	}
	if !strings.Contains(all, "HmacSHA256") {
		t.Error("Should contain HmacSHA256")
	}
	if !strings.Contains(all, "HmacSHA512") {
		t.Error("Should contain HmacSHA512")
	}
}