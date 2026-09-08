package original

import (
	"testing"
)

func TestTypeAssertionString(t *testing.T) {
	var val interface{} = "hello"
	s, ok := val.(string)
	if !ok || s != "hello" {
		t.Errorf("Expected string type assertion to 'hello', got %v", val)
	}
}

func TestTypeAssertionIntFail(t *testing.T) {
	var val interface{} = "not an int"
	_, ok := val.(int)
	if ok {
		t.Errorf("Expected failed type assertion to int")
	}
}