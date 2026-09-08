package public_tests

import (
	"testing"
)

func TestPlaceholderInitAndErrors(t *testing.T) {
	val := "error"
	if _, ok := interface{}(val).(string); !ok {
		t.Errorf("expected value to be string")
	}
}