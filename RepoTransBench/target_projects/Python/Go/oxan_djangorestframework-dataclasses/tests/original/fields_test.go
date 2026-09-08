package original

import (
	"testing"
)

func TestFieldsInt(t *testing.T) {
	var value int = 42
	if value != 42 {
		t.Errorf("Expected int field value 42, got %d", value)
	}
}

func TestFieldsString(t *testing.T) {
	var value string = "hello"
	if value != "hello" {
		t.Errorf("Expected string field value 'hello', got %q", value)
	}
}