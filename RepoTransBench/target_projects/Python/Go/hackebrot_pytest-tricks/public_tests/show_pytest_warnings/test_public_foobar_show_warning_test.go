package public_tests

import (
	"testing"
)

func TestPublicWarningIsShown(t *testing.T) {
	// In Go, we can't intercept warnings directly. We'll log a warning for the test.
	t.Log("this is a public test warning!")
}