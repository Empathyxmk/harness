package public_tests

import (
	"testing"

	"github.com/othersideai/chronology/chronological"
)

func TestDummyPositivePublic(t *testing.T) {
	if got := chronological.DummyPositive(42); got != true {
		t.Errorf("DummyPositive(42) = %v, want true", got)
	}
	if got := chronological.DummyPositive(-17); got != false {
		t.Errorf("DummyPositive(-17) = %v, want false", got)
	}
	if got := chronological.DummyPositive(0); got != false {
		t.Errorf("DummyPositive(0) = %v, want false", got)
	}
}