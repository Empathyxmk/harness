package public_tests

import (
	"testing"
)

func TestSampleLogicPublic_SanityTestDifferentAssertion(t *testing.T) {
	if 123 != 123 {
		t.Error("Sample public test, 123 equals 123")
	}
}