package public_tests

import (
	"testing"
)

func TestPlaceholderDispatcher(t *testing.T) {
	if 10+5 != 15 {
		t.Errorf("10+5 should equal 15")
	}
}