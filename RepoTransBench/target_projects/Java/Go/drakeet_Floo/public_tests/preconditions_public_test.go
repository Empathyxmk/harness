package public_tests

import (
	"testing"
)

func CheckNotNull(val interface{}) interface{} {
	if val == nil {
		panic("null pointer")
	}
	return val
}

func TestCheckNotNull_nonNull_public(t *testing.T) {
	s := "not null"
	got := CheckNotNull(s)
	if got != s {
		t.Errorf("expected %v, got %v", s, got)
	}
}

func TestCheckNotNull_null_public(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic for nil argument")
		}
	}()
	CheckNotNull(nil)
}