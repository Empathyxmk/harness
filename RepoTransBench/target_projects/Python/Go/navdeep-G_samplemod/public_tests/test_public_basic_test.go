package public_tests

import (
	"testing"

	"navdeepG_samplemod/sample"
)

func TestAddPositiveNumbersPublic(t *testing.T) {
	if got := sample.Add(10, 5); got != 15 {
		t.Errorf("Add(10, 5) = %d, want 15", got)
	}
}

func TestAddNegativeAndPositivePublic(t *testing.T) {
	if got := sample.Add(-6, 4); got != -2 {
		t.Errorf("Add(-6, 4) = %d, want -2", got)
	}
}

func TestAddZeroPublic(t *testing.T) {
	if got := sample.Add(0, 19); got != 19 {
		t.Errorf("Add(0, 19) = %d, want 19", got)
	}
}