package original

import (
	"testing"
	"github.com/example/xworkflows/src/xworkflows"
)

func TestImportCompatDirectSrc(t *testing.T) {
	if xworkflows.u("abc") != "abc" {
		t.Errorf("u('abc') must return 'abc'")
	}
	if !xworkflows.IsString("test") {
		t.Errorf("IsString('test') should return true")
	}
	if xworkflows.IsString(123) || xworkflows.IsString(nil) {
		t.Errorf("IsString int or nil should return false")
	}
}

func TestPython2ModeEquivalence(t *testing.T) {
	if !xworkflows.IsString("hey") {
		t.Errorf("IsString(\"hey\") should be true")
	}
	// Go "bytes" are []byte, which is never a string
	if xworkflows.IsString([]byte("bytes")) {
		t.Errorf("IsString([]byte(\"bytes\")) should be false")
	}
}