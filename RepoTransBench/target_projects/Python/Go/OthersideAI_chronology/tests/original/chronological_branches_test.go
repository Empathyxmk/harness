package chronological_test

import (
	"testing"

	"github.com/othersideai/chronology/chronological"
)

func TestDummyPositive(t *testing.T) {
	if got := chronological.DummyPositive(5); got != true {
		t.Errorf("DummyPositive(5) = %v, want true", got)
	}
	if got := chronological.DummyPositive(-3); got != false {
		t.Errorf("DummyPositive(-3) = %v, want false", got)
	}
	if got := chronological.DummyPositive(0); got != false {
		t.Errorf("DummyPositive(0) = %v, want false", got)
	}
}